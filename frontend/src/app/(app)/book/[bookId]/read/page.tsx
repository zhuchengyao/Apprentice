"use client";

import { useEffect, useState, useCallback, useRef, useMemo, memo } from "react";
import { use } from "react";
import "katex/dist/katex.min.css";
import DOMPurify from "dompurify";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useTranslations } from "next-intl";
import {
  ArrowLeft,
  BookOpen,
  CheckCircle2,
  Circle,
  Loader2,
  AlertCircle,
  PanelLeftClose,
  PanelLeftOpen,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { TutorPopover, type KPHighlight } from "@/components/tutor/tutor-popover";
import { useTutorHighlight } from "@/components/tutor/use-tutor-highlight";
import { api } from "@/lib/api-client";
import { cn } from "@/lib/utils";
import type {
  BookDetail,
  BookPage,
  BookPagesResponse,
  Chapter,
  ChapterProgress,
} from "@/lib/types";

const ChapterContent = memo(
  function ChapterContent({ pages }: { pages: BookPage[] }) {
    const containerRef = useRef<HTMLDivElement>(null);

    const sanitized = useMemo(
      () =>
        pages.map((page) => ({
          page_number: page.page_number,
          html: DOMPurify.sanitize(page.html_content, {
            ADD_TAGS: [
              "figure", "figcaption", "svg", "rect", "circle", "ellipse",
              "line", "polyline", "polygon", "path", "text", "tspan", "g",
              "defs", "marker", "use", "foreignObject",
            ],
            ADD_ATTR: [
              "loading", "viewBox", "xmlns", "fill", "stroke", "stroke-width",
              "d", "x", "y", "x1", "y1", "x2", "y2", "cx", "cy", "r", "rx",
              "ry", "width", "height", "points", "transform", "text-anchor",
              "dominant-baseline", "font-size", "font-weight", "font-family",
              "opacity", "stroke-dasharray", "marker-end", "marker-start",
              "refX", "refY", "markerWidth", "markerHeight", "orient",
              "preserveAspectRatio", "style",
            ],
          }),
        })),
      [pages],
    );

    useEffect(() => {
      const el = containerRef.current;
      if (!el || sanitized.length === 0) return;
      if (el.querySelector(".katex")) return;
      import("katex/contrib/auto-render").then((mod) => {
        mod.default(el, {
          delimiters: [
            { left: "\\[", right: "\\]", display: true },
            { left: "\\(", right: "\\)", display: false },
          ],
          throwOnError: false,
          ignoredClasses: ["katex"],
        });
      });
    }, [sanitized]);

    return (
      <div ref={containerRef} className="space-y-2">
        {sanitized.map((page) => (
          <div
            key={page.page_number}
            className="book-page prose prose-base max-w-none dark:prose-invert prose-headings:font-heading prose-headings:tracking-tight prose-headings:font-semibold prose-img:rounded-lg prose-img:mx-auto prose-figure:text-center"
            dangerouslySetInnerHTML={{ __html: page.html }}
          />
        ))}
      </div>
    );
  },
  (prev, next) => {
    if (prev.pages === next.pages) return true;
    if (prev.pages.length !== next.pages.length) return false;
    for (let i = 0; i < prev.pages.length; i++) {
      if (
        prev.pages[i].page_number !== next.pages[i].page_number ||
        prev.pages[i].html_content !== next.pages[i].html_content
      ) {
        return false;
      }
    }
    return true;
  },
);

export default function ReadPage({
  params,
}: {
  params: Promise<{ bookId: string }>;
}) {
  const { bookId } = use(params);
  const router = useRouter();
  const searchParams = useSearchParams();
  const t = useTranslations("reader");
  const tBook = useTranslations("book");

  const [book, setBook] = useState<BookDetail | null>(null);
  const [activeChapterId, setActiveChapterId] = useState<string | null>(null);
  const [chapterPages, setChapterPages] = useState<BookPage[]>([]);
  const [loading, setLoading] = useState(true);
  const [contentLoading, setContentLoading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [progress, setProgress] = useState<{
    done: number;
    total: number;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [processError, setProcessError] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [scrollContainer, setScrollContainer] = useState<HTMLElement | null>(null);

  const eventSourceRef = useRef<EventSource | null>(null);
  const loadedChapterKeyRef = useRef<string | null>(null);

  const highlightContainerRef = useRef<HTMLElement | null>(null);
  const getHighlightContainer = useCallback(
    () => highlightContainerRef.current,
    [],
  );
  const { applyHighlight, clearAll: clearAllHighlights } = useTutorHighlight(
    getHighlightContainer,
  );

  const searchParamsRef = useRef(searchParams);
  searchParamsRef.current = searchParams;
  const routerRef = useRef(router);
  routerRef.current = router;

  useEffect(() => {
    return () => {
      eventSourceRef.current?.close();
    };
  }, []);

  useEffect(() => {
    async function fetchBook() {
      try {
        const data = await api.get<BookDetail>(`/books/${bookId}`);
        setBook(data);

        const chapterParam = searchParamsRef.current.get("chapter");
        if (chapterParam && data.chapters.some((ch) => ch.id === chapterParam)) {
          setActiveChapterId(chapterParam);
        } else if (data.chapters.length > 0) {
          setActiveChapterId(data.chapters[0].id);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : tBook("not_found"));
      }
      setLoading(false);
    }
    fetchBook();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [bookId]);

  const fetchChapterPages = useCallback(
    async (chapter: Chapter) => {
      setContentLoading(true);
      try {
        const data = await api.get<BookPagesResponse>(
          `/books/${bookId}/chapters/${chapter.id}/pages`,
        );
        setChapterPages(data.pages);
      } catch {
        setChapterPages([]);
        setProcessError(t("load_pages_failed"));
      }
      setContentLoading(false);
    },
    [bookId, t],
  );

  const loadChapter = useCallback(
    async (chapter: Chapter) => {
      setProcessError(null);

      if (!chapter.processed) {
        setProcessing(true);
        setProgress({ done: 0, total: chapter.end_page - chapter.start_page + 1 });

        api
          .post(`/books/${bookId}/chapters/${chapter.id}/process`, {})
          .catch(() => {});

        await new Promise<void>((resolve, reject) => {
          const es = new EventSource(
            `/api/books/${bookId}/chapters/${chapter.id}/progress/stream`,
          );
          eventSourceRef.current = es;

          es.addEventListener("progress", (e) => {
            try {
              const data: ChapterProgress = JSON.parse(e.data);
              setProgress({ done: data.pages_done, total: data.pages_total });
            } catch {
              // ignore parse errors
            }
          });

          es.addEventListener("done", async () => {
            es.close();
            eventSourceRef.current = null;
            try {
              const updated = await api.get<BookDetail>(`/books/${bookId}`);
              setBook(updated);
            } catch {
              // non-critical
            }
            setProcessing(false);
            setProgress(null);
            resolve();
          });

          es.onerror = () => {
            es.close();
            eventSourceRef.current = null;
            setProcessing(false);
            setProgress(null);
            setProcessError(t("connection_lost"));
            reject(new Error("SSE connection lost"));
          };
        }).catch(() => {
          return;
        });
      }

      await fetchChapterPages(chapter);
    },
    [bookId, fetchChapterPages, t],
  );

  useEffect(() => {
    if (!book || !activeChapterId) return;
    const chapter = book.chapters.find((ch) => ch.id === activeChapterId);
    if (!chapter) return;

    const key = `${book.id}:${chapter.id}:${chapter.processed}`;
    if (loadedChapterKeyRef.current === key) return;
    loadedChapterKeyRef.current = key;

    loadChapter(chapter);
  }, [book, activeChapterId, loadChapter]);

  useEffect(() => {
    if (activeChapterId) {
      routerRef.current.replace(
        `/book/${bookId}/read?chapter=${activeChapterId}`,
        { scroll: false },
      );
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [bookId, activeChapterId]);

  const selectChapter = useCallback((chapterId: string) => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    setActiveChapterId(chapterId);
    setChapterPages([]);
    setProcessing(false);
    setProgress(null);
    clearAllHighlights();
    document.getElementById("chapter-content")?.scrollTo({ top: 0 });
  }, [clearAllHighlights]);

  const handleHighlight = useCallback(
    (kps: KPHighlight[]) => applyHighlight(kps),
    [applyHighlight],
  );

  const handleKpsCovered = useCallback((_ids: string[]) => {
    // Reserved for future persistence of per-KP progress from the frontend.
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (error || !book) {
    return (
      <div className="mx-auto max-w-4xl px-6 py-10">
        <Link href={`/book/${bookId}`}>
          <Button variant="ghost" size="sm" className="mb-6 gap-1.5 rounded-full">
            <ArrowLeft className="h-4 w-4" />
            {t("back_to_book")}
          </Button>
        </Link>
        <div className="flex flex-col items-center justify-center py-24">
          <AlertCircle className="h-10 w-10 text-destructive" />
          <p className="mt-4 text-sm text-muted-foreground">
            {error || tBook("not_found")}
          </p>
        </div>
      </div>
    );
  }

  const activeChapter = book.chapters.find((ch) => ch.id === activeChapterId);
  const progressPct =
    progress && progress.total > 0
      ? Math.round((progress.done / progress.total) * 100)
      : 0;

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {sidebarOpen && (
        <aside className="flex w-72 shrink-0 flex-col border-r border-sidebar-border bg-sidebar">
          <div className="flex items-center gap-2 border-b border-sidebar-border/70 px-4 py-3">
            <Link href={`/book/${bookId}`}>
              <Button variant="ghost" size="icon-sm" className="rounded-full">
                <ArrowLeft className="h-3.5 w-3.5" />
              </Button>
            </Link>
            <h2 className="min-w-0 truncate font-heading text-[13.5px] font-semibold tracking-tight">
              {book.title}
            </h2>
          </div>
          <ScrollArea className="flex-1">
            <nav className="p-2">
              {book.chapters.map((chapter) => {
                const active = chapter.id === activeChapterId;
                return (
                  <button
                    key={chapter.id}
                    onClick={() => selectChapter(chapter.id)}
                    className={cn(
                      "group relative mb-0.5 flex w-full items-start gap-2 rounded-lg px-3 py-2 text-left text-[13px] transition-colors",
                      active
                        ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium"
                        : "text-muted-foreground hover:bg-sidebar-accent/60 hover:text-foreground",
                    )}
                  >
                    {active && (
                      <span className="absolute left-0 top-1/2 h-5 w-0.5 -translate-y-1/2 rounded-r-full bg-primary" />
                    )}
                    {chapter.processed ? (
                      <CheckCircle2 className="mt-0.5 h-3.5 w-3.5 shrink-0 text-primary" />
                    ) : (
                      <Circle className="mt-0.5 h-3.5 w-3.5 shrink-0 opacity-50" />
                    )}
                    <span className="line-clamp-2">{chapter.title}</span>
                  </button>
                );
              })}
            </nav>
          </ScrollArea>
        </aside>
      )}

      <main className="flex flex-1 flex-col overflow-hidden">
        <div className="flex items-center gap-3 border-b border-border/60 bg-background/75 px-4 py-2 backdrop-blur-xl">
          <Button
            variant="ghost"
            size="icon-sm"
            className="rounded-full"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label={t("toggle_sidebar")}
          >
            {sidebarOpen ? (
              <PanelLeftClose className="h-4 w-4" />
            ) : (
              <PanelLeftOpen className="h-4 w-4" />
            )}
          </Button>
          {activeChapter && (
            <span className="min-w-0 truncate font-heading text-[13px] font-medium">
              {activeChapter.title}
            </span>
          )}
        </div>

        <div
          id="chapter-content"
          ref={(el) => {
            highlightContainerRef.current = el;
            setScrollContainer(el);
          }}
          className="flex-1 overflow-y-auto"
        >
          <div className="mx-auto max-w-3xl px-8 py-10">
            {processing ? (
              <div className="flex flex-col items-center justify-center gap-4 py-32">
                <Loader2 className="h-7 w-7 animate-spin text-primary" />
                <p className="text-[13.5px] text-muted-foreground">
                  {t("processing_chapter")}
                </p>
                {progress && progress.total > 0 && (
                  <div className="w-64">
                    <div className="mb-1.5 flex justify-between font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground tabular-nums">
                      <span>
                        {t("page_progress", {
                          done: progress.done,
                          total: progress.total,
                        })}
                      </span>
                      <span>{progressPct}%</span>
                    </div>
                    <div className="h-1.5 overflow-hidden rounded-full bg-subtle ring-1 ring-inset ring-border/60">
                      <div
                        className="h-full rounded-full bg-primary transition-all duration-500 ease-out"
                        style={{ width: `${progressPct}%` }}
                      />
                    </div>
                  </div>
                )}
              </div>
            ) : processError ? (
              <div className="flex flex-col items-center justify-center gap-3 py-32">
                <AlertCircle className="h-7 w-7 text-destructive" />
                <p className="text-[13.5px] text-muted-foreground">
                  {processError}
                </p>
                {activeChapter && (
                  <Button
                    variant="outline"
                    size="sm"
                    className="rounded-full"
                    onClick={() => loadChapter(activeChapter)}
                  >
                    {t("retry")}
                  </Button>
                )}
              </div>
            ) : contentLoading ? (
              <div className="flex items-center justify-center py-32">
                <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
              </div>
            ) : chapterPages.length > 0 ? (
              <ChapterContent pages={chapterPages} />
            ) : (
              <div className="flex flex-col items-center justify-center py-32 text-muted-foreground">
                <BookOpen className="mb-3 h-9 w-9" />
                <p className="text-[13.5px]">{t("select_chapter")}</p>
              </div>
            )}
          </div>
        </div>
      </main>

      {activeChapterId && !processing && !contentLoading && chapterPages.length > 0 && (
        <TutorPopover
          key={activeChapterId}
          bookId={bookId}
          chapterId={activeChapterId}
          scrollContainer={scrollContainer}
          onHighlight={handleHighlight}
          onKpsCovered={handleKpsCovered}
        />
      )}
    </div>
  );
}
