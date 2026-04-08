"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import { use } from "react";
import "katex/dist/katex.min.css";
import DOMPurify from "dompurify";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import {
  ArrowLeft,
  BookOpen,
  CheckCircle2,
  Circle,
  Loader2,
  AlertCircle,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { api } from "@/lib/api-client";
import type {
  BookDetail,
  BookPage,
  BookPagesResponse,
  Chapter,
  ChapterProgress,
} from "@/lib/types";

export default function ReadPage({
  params,
}: {
  params: Promise<{ bookId: string }>;
}) {
  const { bookId } = use(params);
  const router = useRouter();
  const searchParams = useSearchParams();

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

  const contentRef = useRef<HTMLDivElement>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  // Cleanup SSE on unmount
  useEffect(() => {
    return () => {
      eventSourceRef.current?.close();
    };
  }, []);

  // Render KaTeX math after HTML content is injected
  useEffect(() => {
    const el = contentRef.current;
    if (!el || chapterPages.length === 0 || contentLoading || processing) return;
    import("katex/contrib/auto-render").then((mod) => {
      const renderMathInElement = mod.default;
      renderMathInElement(el, {
        delimiters: [
          { left: "\\[", right: "\\]", display: true },
          { left: "\\(", right: "\\)", display: false },
        ],
        throwOnError: false,
      });
    });
  }, [chapterPages, contentLoading, processing]);

  // Fetch book detail
  useEffect(() => {
    async function fetchBook() {
      try {
        const data = await api.get<BookDetail>(`/books/${bookId}`);
        setBook(data);

        const chapterParam = searchParams.get("chapter");
        if (chapterParam && data.chapters.some((ch) => ch.id === chapterParam)) {
          setActiveChapterId(chapterParam);
        } else if (data.chapters.length > 0) {
          setActiveChapterId(data.chapters[0].id);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load book");
      }
      setLoading(false);
    }
    fetchBook();
  }, [bookId, searchParams]);

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
        setProcessError("Failed to load chapter pages.");
      }
      setContentLoading(false);
    },
    [bookId],
  );

  // Load chapter content when active chapter changes
  const loadChapter = useCallback(
    async (chapter: Chapter) => {
      setProcessError(null);

      if (!chapter.processed) {
        setProcessing(true);
        setProgress({ done: 0, total: chapter.end_page - chapter.start_page + 1 });

        // Fire-and-forget: start background processing
        api
          .post(`/books/${bookId}/chapters/${chapter.id}/process`, {})
          .catch(() => {});

        // Stream progress via SSE
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
            setProcessError("Lost connection while processing chapter.");
            reject(new Error("SSE connection lost"));
          };
        }).catch(() => {
          // Error already surfaced via setProcessError
          return;
        });
      }

      await fetchChapterPages(chapter);
    },
    [bookId, fetchChapterPages],
  );

  // Trigger load when active chapter changes
  useEffect(() => {
    if (!book || !activeChapterId) return;
    const chapter = book.chapters.find((ch) => ch.id === activeChapterId);
    if (chapter) {
      loadChapter(chapter);
    }
  }, [book, activeChapterId, loadChapter]);

  // Update URL when chapter changes
  useEffect(() => {
    if (activeChapterId) {
      router.replace(`/book/${bookId}/read?chapter=${activeChapterId}`, {
        scroll: false,
      });
    }
  }, [bookId, activeChapterId, router]);

  const selectChapter = useCallback((chapterId: string) => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    setActiveChapterId(chapterId);
    setChapterPages([]);
    setProcessing(false);
    setProgress(null);
    document.getElementById("chapter-content")?.scrollTo({ top: 0 });
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
      <div className="mx-auto max-w-4xl px-6 py-8">
        <Link href={`/book/${bookId}`}>
          <Button variant="ghost" size="sm" className="mb-6 gap-1.5">
            <ArrowLeft className="h-4 w-4" />
            Back to book
          </Button>
        </Link>
        <div className="flex flex-col items-center justify-center py-24">
          <AlertCircle className="h-10 w-10 text-destructive" />
          <p className="mt-4 text-sm text-muted-foreground">
            {error || "Book not found"}
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
    <div className="flex h-[calc(100vh-4rem)] overflow-hidden">
      {/* Chapter Sidebar */}
      {sidebarOpen && (
        <aside className="w-72 shrink-0 border-r bg-muted/30">
          <div className="flex items-center gap-2 border-b px-4 py-3">
            <Link href={`/book/${bookId}`}>
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <ArrowLeft className="h-4 w-4" />
              </Button>
            </Link>
            <h2 className="truncate text-sm font-semibold">{book.title}</h2>
          </div>
          <ScrollArea className="h-[calc(100%-3.25rem)]">
            <nav className="p-2">
              {book.chapters.map((chapter) => (
                <button
                  key={chapter.id}
                  onClick={() => selectChapter(chapter.id)}
                  className={`flex w-full items-start gap-2 rounded-md px-3 py-2 text-left text-sm transition-colors ${
                    chapter.id === activeChapterId
                      ? "bg-primary/10 text-primary font-medium"
                      : "text-muted-foreground hover:bg-muted hover:text-foreground"
                  }`}
                >
                  {chapter.processed ? (
                    <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-green-500" />
                  ) : (
                    <Circle className="mt-0.5 h-4 w-4 shrink-0" />
                  )}
                  <span className="line-clamp-2">{chapter.title}</span>
                </button>
              ))}
            </nav>
          </ScrollArea>
        </aside>
      )}

      {/* Content Area */}
      <main className="flex-1 overflow-hidden">
        {/* Top bar */}
        <div className="flex items-center gap-3 border-b px-4 py-2">
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            <BookOpen className="h-4 w-4" />
          </Button>
          {activeChapter && (
            <span className="truncate text-sm font-medium">
              {activeChapter.title}
            </span>
          )}
        </div>

        {/* Scrollable content */}
        <div
          id="chapter-content"
          className="h-[calc(100%-2.75rem)] overflow-y-auto"
        >
          <div className="mx-auto max-w-3xl px-8 py-10">
            {processing ? (
              <div className="flex flex-col items-center justify-center py-32 gap-4">
                <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
                <p className="text-sm text-muted-foreground">
                  Processing chapter…
                </p>
                {progress && progress.total > 0 && (
                  <div className="w-64">
                    <div className="mb-1.5 flex justify-between text-xs text-muted-foreground">
                      <span>
                        Page {progress.done} / {progress.total}
                      </span>
                      <span>{progressPct}%</span>
                    </div>
                    <div className="h-2 overflow-hidden rounded-full bg-muted">
                      <div
                        className="h-full rounded-full bg-primary transition-all duration-500 ease-out"
                        style={{ width: `${progressPct}%` }}
                      />
                    </div>
                  </div>
                )}
              </div>
            ) : processError ? (
              <div className="flex flex-col items-center justify-center py-32 gap-3">
                <AlertCircle className="h-8 w-8 text-destructive" />
                <p className="text-sm text-muted-foreground">{processError}</p>
                {activeChapter && (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => loadChapter(activeChapter)}
                  >
                    Retry
                  </Button>
                )}
              </div>
            ) : contentLoading ? (
              <div className="flex items-center justify-center py-32">
                <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
              </div>
            ) : chapterPages.length > 0 ? (
              <div ref={contentRef} className="space-y-2">
                {chapterPages.map((page) => (
                  <div
                    key={page.page_number}
                    className="book-page prose prose-base max-w-none dark:prose-invert prose-headings:font-semibold prose-img:rounded-lg prose-img:mx-auto prose-figure:text-center"
                    dangerouslySetInnerHTML={{
                      __html: DOMPurify.sanitize(page.html_content, {
                        ADD_TAGS: ["figure", "figcaption", "svg", "rect", "circle", "ellipse", "line", "polyline", "polygon", "path", "text", "tspan", "g", "defs", "marker", "use", "foreignObject"],
                        ADD_ATTR: ["loading", "viewBox", "xmlns", "fill", "stroke", "stroke-width", "d", "x", "y", "x1", "y1", "x2", "y2", "cx", "cy", "r", "rx", "ry", "width", "height", "points", "transform", "text-anchor", "dominant-baseline", "font-size", "font-weight", "font-family", "opacity", "stroke-dasharray", "marker-end", "marker-start", "refX", "refY", "markerWidth", "markerHeight", "orient", "preserveAspectRatio", "style"],
                      }),
                    }}
                  />
                ))}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-32 text-muted-foreground">
                <BookOpen className="h-10 w-10 mb-3" />
                <p className="text-sm">Select a chapter to start reading.</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
