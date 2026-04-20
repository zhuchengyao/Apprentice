import os
import re
import uuid
from dataclasses import dataclass, field

import fitz  # PyMuPDF

from app.config import settings


class PdfParseError(Exception):
    """Raised when a PDF cannot be parsed.

    ``reason`` is a stable machine-readable tag (``encrypted``, ``corrupt``,
    ``missing``) so upstream callers can branch on it; ``str(exc)`` carries
    a human-readable message suitable for ``book.error_message``.
    """

    def __init__(self, reason: str, message: str | None = None):
        self.reason = reason
        super().__init__(message or reason)


def _open_pdf(file_path: str) -> fitz.Document:
    """Open a PDF, converting encryption + malformed-file conditions to PdfParseError.

    PyMuPDF raises ``FileDataError`` for corrupt files and ``FileNotFoundError``
    for missing ones. Password-protected PDFs open *successfully* but every
    subsequent read (``get_text``, ``get_toc``) returns empty data — callers
    would silently produce a 0-chapter book. We detect that here via
    ``needs_pass`` and fail loudly instead.
    """
    try:
        doc = fitz.open(file_path)
    except fitz.FileDataError as e:
        raise PdfParseError("corrupt", "PDF is corrupt or unreadable") from e
    except fitz.FileNotFoundError as e:
        raise PdfParseError("missing", "PDF file not found") from e
    if doc.needs_pass:
        doc.close()
        raise PdfParseError("encrypted", "PDF is password-protected")
    return doc


@dataclass
class PageImage:
    """An image extracted from a PDF page."""
    image_path: str       # absolute path on disk
    image_url: str        # relative URL for serving, e.g. /api/images/<book_id>/<filename>
    page_number: int
    index_on_page: int    # 0-based index among images on this page
    width: int
    height: int


@dataclass
class ParsedPage:
    page_number: int
    text: str
    images: list[PageImage] = field(default_factory=list)


@dataclass
class ParsedBook:
    title: str
    author: str
    total_pages: int
    pages: list[ParsedPage]
    toc: list[tuple[int, str, int]]  # (level, title, page)
    images: list[PageImage] = field(default_factory=list)


# Minimum dimensions to filter out tiny decorative images (icons, bullets, etc.)
MIN_IMAGE_WIDTH = 50
MIN_IMAGE_HEIGHT = 50
# Minimum byte size to skip trivial images
MIN_IMAGE_BYTES = 2048
# Raster image covering more than this fraction of the page is a background, not a figure
PAGE_COVER_THRESHOLD = 0.6
# Proximity threshold for clustering nearby raster images into one figure (PDF points)
RASTER_CLUSTER_GAP = 25

# Vector figure extraction thresholds
MIN_VECTOR_PATHS = 4             # cluster needs at least this many drawing paths
MIN_VECTOR_WIDTH = 60            # min cluster bbox width (PDF points)
MIN_VECTOR_HEIGHT = 40           # min cluster bbox height (PDF points)
MIN_VECTOR_AREA = 5000           # min area in square PDF points (~70x70)
MAX_VECTOR_ASPECT_RATIO = 15.0   # reject elongated shapes (separators/underlines)
VECTOR_RENDER_SCALE = 3          # 3x = ~216 DPI
CLUSTER_TOLERANCE = 5            # grouping distance for nearby drawings (PDF points)
OVERLAP_IOU_THRESHOLD = 0.3      # dedup threshold against raster images
PAGE_MARGIN_FRACTION = 0.02      # ignore clusters in outer 2% of page

_CAPTION_PATTERN = re.compile(
    r'(?:Figure|Fig\.?)\s+\d+(?:\.\d+)*',
    re.IGNORECASE,
)


def _cluster_rects(rects: list[fitz.Rect], gap: float) -> list[fitz.Rect]:
    """Merge overlapping or nearby rectangles into clusters.

    Two rects are in the same cluster if they overlap or are within `gap` points.
    Uses iterative union until no more merges happen.
    """
    if not rects:
        return []
    # Expand each rect by gap, then merge overlapping expanded rects
    clusters = list(rects)
    changed = True
    while changed:
        changed = False
        merged: list[fitz.Rect] = []
        used = [False] * len(clusters)
        for i in range(len(clusters)):
            if used[i]:
                continue
            current = clusters[i]
            expanded_i = fitz.Rect(
                current.x0 - gap, current.y0 - gap,
                current.x1 + gap, current.y1 + gap,
            )
            for j in range(i + 1, len(clusters)):
                if used[j]:
                    continue
                if not (expanded_i & clusters[j]).is_empty:
                    current = current | clusters[j]
                    expanded_i = fitz.Rect(
                        current.x0 - gap, current.y0 - gap,
                        current.x1 + gap, current.y1 + gap,
                    )
                    used[j] = True
                    changed = True
            merged.append(current)
            used[i] = True
        clusters = merged
    return clusters


def _extract_page_images(
    doc: fitz.Document,
    page: fitz.Page,
    page_number: int,
    image_dir: str,
    book_id: str,
) -> list[PageImage]:
    """Extract meaningful images from a single PDF page.

    Clusters overlapping/nearby images and renders each cluster as a single
    screenshot to avoid splitting one visual figure into multiple fragments.
    """
    image_list = page.get_images(full=True)
    if not image_list:
        return []

    page_rect = page.rect
    page_area = page_rect.width * page_rect.height

    # Collect rects for all non-trivial images
    figure_rects: list[fitz.Rect] = []
    for img_info in image_list:
        xref = img_info[0]
        try:
            base_image = doc.extract_image(xref)
        except Exception:
            continue
        if not base_image or not base_image.get("image"):
            continue

        width = base_image.get("width", 0)
        height = base_image.get("height", 0)
        if width < MIN_IMAGE_WIDTH or height < MIN_IMAGE_HEIGHT:
            continue
        if len(base_image["image"]) < MIN_IMAGE_BYTES:
            continue

        # Get placement rect(s) on page
        try:
            for rect in page.get_image_rects(xref):
                if rect.is_empty or rect.is_infinite:
                    continue
                # Skip full-page background images
                if rect.width * rect.height > page_area * PAGE_COVER_THRESHOLD:
                    continue
                figure_rects.append(rect)
        except Exception:
            continue

    if not figure_rects:
        return []

    # Cluster nearby rects into figure groups
    clusters = _cluster_rects(figure_rects, gap=RASTER_CLUSTER_GAP)

    # Render each cluster as a single screenshot
    images: list[PageImage] = []
    for idx, cluster_rect in enumerate(clusters):
        # Filter out tiny clusters
        if cluster_rect.width < MIN_IMAGE_WIDTH or cluster_rect.height < MIN_IMAGE_HEIGHT:
            continue

        # Add padding and clip to page
        padding = 5
        render_rect = fitz.Rect(
            max(cluster_rect.x0 - padding, page_rect.x0),
            max(cluster_rect.y0 - padding, page_rect.y0),
            min(cluster_rect.x1 + padding, page_rect.x1),
            min(cluster_rect.y1 + padding, page_rect.y1),
        )
        mat = fitz.Matrix(VECTOR_RENDER_SCALE, VECTOR_RENDER_SCALE)
        pix = page.get_pixmap(clip=render_rect, matrix=mat)

        filename = f"p{page_number}_img{idx}_{uuid.uuid4().hex[:8]}.png"
        image_path = os.path.join(image_dir, filename)
        pix.save(image_path)

        image_url = f"/api/images/{book_id}/{filename}"
        images.append(PageImage(
            image_path=image_path,
            image_url=image_url,
            page_number=page_number,
            index_on_page=idx,
            width=pix.width,
            height=pix.height,
        ))

    return images


def _get_raster_image_rects(page: fitz.Page) -> list[fitz.Rect]:
    """Return bounding boxes of non-background raster Image XObjects on the page."""
    page_area = page.rect.width * page.rect.height
    rects = []
    for img_info in page.get_images(full=True):
        xref = img_info[0]
        try:
            for rect in page.get_image_rects(xref):
                if rect.is_empty or rect.is_infinite:
                    continue
                if rect.width * rect.height > page_area * PAGE_COVER_THRESHOLD:
                    continue
                rects.append(rect)
        except Exception:
            continue
    return rects


def _rects_iou(r1: fitz.Rect, r2: fitz.Rect) -> float:
    """Return intersection-over-union of two rectangles."""
    inter = r1 & r2
    if inter.is_empty:
        return 0.0
    inter_area = inter.width * inter.height
    union_area = r1.width * r1.height + r2.width * r2.height - inter_area
    if union_area <= 0:
        return 0.0
    return inter_area / union_area


def _is_margin_cluster(rect: fitz.Rect, page_rect: fitz.Rect) -> bool:
    """Return True if the cluster sits entirely in the page margin zone."""
    margin_x = page_rect.width * PAGE_MARGIN_FRACTION
    margin_y = page_rect.height * PAGE_MARGIN_FRACTION
    inner = fitz.Rect(
        page_rect.x0 + margin_x, page_rect.y0 + margin_y,
        page_rect.x1 - margin_x, page_rect.y1 - margin_y,
    )
    return (rect & inner).is_empty


def _find_figure_captions(page: fitz.Page) -> list[fitz.Rect]:
    """Find bounding boxes of figure caption lines on the page."""
    captions = []
    text_dict = page.get_text("dict")
    for block in text_dict.get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            line_text = "".join(span["text"] for span in line.get("spans", []))
            if _CAPTION_PATTERN.search(line_text):
                captions.append(fitz.Rect(line["bbox"]))
    return captions


def _extract_vector_figures(
    page: fitz.Page,
    page_number: int,
    image_dir: str,
    book_id: str,
    raster_start_index: int,
) -> list[PageImage]:
    """Extract vector-based figures by clustering drawing paths and rendering as raster."""
    drawings = page.get_drawings()
    if len(drawings) < MIN_VECTOR_PATHS:
        return []

    clusters = page.cluster_drawings(
        x_tolerance=CLUSTER_TOLERANCE,
        y_tolerance=CLUSTER_TOLERANCE,
        drawings=drawings,
    )
    if not clusters:
        return []

    raster_rects = _get_raster_image_rects(page)
    caption_rects = _find_figure_captions(page)
    page_rect = page.rect
    figures: list[PageImage] = []

    for cluster_rect in clusters:
        w, h = cluster_rect.width, cluster_rect.height

        # Basic geometry filters
        if w < MIN_VECTOR_WIDTH or h < MIN_VECTOR_HEIGHT:
            continue
        if w * h < MIN_VECTOR_AREA:
            continue
        aspect = max(w, h) / max(min(w, h), 0.1)
        if aspect > MAX_VECTOR_ASPECT_RATIO:
            continue
        if _is_margin_cluster(cluster_rect, page_rect):
            continue

        # Dedup against raster images
        if any(_rects_iou(cluster_rect, rr) > OVERLAP_IOU_THRESHOLD for rr in raster_rects):
            continue

        # Caption proximity: relax path threshold and expand rect
        min_paths_needed = MIN_VECTOR_PATHS
        for cap_rect in caption_rects:
            vert_dist = min(
                abs(cluster_rect.y1 - cap_rect.y0),
                abs(cap_rect.y1 - cluster_rect.y0),
            )
            horiz_overlap = cluster_rect.x0 < cap_rect.x1 and cap_rect.x0 < cluster_rect.x1
            if vert_dist < 30 and horiz_overlap:
                min_paths_needed = 2
                cluster_rect = cluster_rect | cap_rect
                break

        # Count drawing paths in this cluster
        path_count = sum(
            1 for d in drawings
            if not (fitz.Rect(d["rect"]) & cluster_rect).is_empty
        )
        if path_count < min_paths_needed:
            continue

        # Render with padding
        padding = 5
        render_rect = fitz.Rect(
            max(cluster_rect.x0 - padding, page_rect.x0),
            max(cluster_rect.y0 - padding, page_rect.y0),
            min(cluster_rect.x1 + padding, page_rect.x1),
            min(cluster_rect.y1 + padding, page_rect.y1),
        )
        mat = fitz.Matrix(VECTOR_RENDER_SCALE, VECTOR_RENDER_SCALE)
        pix = page.get_pixmap(clip=render_rect, matrix=mat)

        img_idx = raster_start_index + len(figures)
        filename = f"p{page_number}_vec{img_idx}_{uuid.uuid4().hex[:8]}.png"
        image_path = os.path.join(image_dir, filename)
        pix.save(image_path)

        image_url = f"/api/images/{book_id}/{filename}"
        figures.append(PageImage(
            image_path=image_path,
            image_url=image_url,
            page_number=page_number,
            index_on_page=img_idx,
            width=pix.width,
            height=pix.height,
        ))

    return figures


@dataclass
class PdfMetadata:
    """Lightweight metadata extracted without processing page content."""
    title: str
    author: str
    total_pages: int
    toc: list[tuple[int, str, int]]  # (level, title, page)


def parse_pdf_metadata(file_path: str) -> PdfMetadata:
    """Fast metadata-only parse: title, author, page count, TOC. No image extraction."""
    doc = _open_pdf(file_path)
    title = doc.metadata.get("title", "") or ""
    author = doc.metadata.get("author", "") or ""
    toc = [(level, t, page) for level, t, page in doc.get_toc()]
    total_pages = len(doc)
    doc.close()
    return PdfMetadata(title=title, author=author, total_pages=total_pages, toc=toc)


def parse_pdf_pages(
    file_path: str,
    book_id: str,
    start_page: int = 1,
    end_page: int | None = None,
) -> list[ParsedPage]:
    """Parse a range of pages with text + image extraction.

    Args:
        file_path: path to the PDF file
        book_id: used for image output directory
        start_page: 1-based start page (inclusive)
        end_page: 1-based end page (inclusive), None = last page
    """
    doc = _open_pdf(file_path)
    if end_page is None:
        end_page = len(doc)

    image_dir = os.path.join(settings.upload_dir, "images", book_id)
    os.makedirs(image_dir, exist_ok=True)

    pages: list[ParsedPage] = []
    for i in range(start_page - 1, min(end_page, len(doc))):
        page = doc[i]
        page_number = i + 1
        text = page.get_text("text")

        page_images = _extract_page_images(doc, page, page_number, image_dir, book_id)
        vector_images = _extract_vector_figures(
            page, page_number, image_dir, book_id,
            raster_start_index=len(page_images),
        )
        page_images.extend(vector_images)

        if text.strip() or page_images:
            pages.append(ParsedPage(page_number=page_number, text=text, images=page_images))

    doc.close()
    return pages


def parse_pdf(file_path: str, book_id: str | None = None) -> ParsedBook:
    doc = _open_pdf(file_path)

    title = doc.metadata.get("title", "") or ""
    author = doc.metadata.get("author", "") or ""

    # Set up image output directory
    if book_id:
        image_dir = os.path.join(settings.upload_dir, "images", book_id)
        os.makedirs(image_dir, exist_ok=True)
    else:
        image_dir = None

    all_images: list[PageImage] = []
    pages = []
    for i, page in enumerate(doc):
        page_number = i + 1
        text = page.get_text("text")

        # Extract images if we have an output directory
        page_images: list[PageImage] = []
        if image_dir:
            page_images = _extract_page_images(doc, page, page_number, image_dir, book_id)
            vector_images = _extract_vector_figures(
                page, page_number, image_dir, book_id,
                raster_start_index=len(page_images),
            )
            page_images.extend(vector_images)
            all_images.extend(page_images)

        if text.strip() or page_images:
            pages.append(ParsedPage(page_number=page_number, text=text, images=page_images))

    toc = [(level, title, page) for level, title, page in doc.get_toc()]
    total_pages = len(doc)
    doc.close()

    return ParsedBook(
        title=title,
        author=author,
        total_pages=total_pages,
        pages=pages,
        toc=toc,
        images=all_images,
    )
