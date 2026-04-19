"use client";

import { useEffect, useState, use } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import {
  ArrowLeft,
  Loader2,
  BookOpen,
  AlertCircle,
  Trash2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ChapterTree } from "@/components/book/chapter-tree";
import { BookStats } from "@/components/book/book-stats";
import { ProcessingAnimation } from "@/components/upload/processing-animation";
import { api } from "@/lib/api-client";
import type { BookDetail } from "@/lib/types";
import type { BookStatus } from "@/lib/constants";

export default function BookOverviewPage({
  params,
}: {
  params: Promise<{ bookId: string }>;
}) {
  const { bookId } = use(params);
  const router = useRouter();
  const t = useTranslations("book");
  const tStatus = useTranslations("library.status");
  const [book, setBook] = useState<BookDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState(false);

  const handleDelete = async () => {
    if (!confirm(t("delete_confirm"))) return;
    setDeleting(true);
    try {
      await api.delete(`/books/${bookId}`);
      router.push("/library");
    } catch {
      setDeleting(false);
      alert(t("delete_failed"));
    }
  };

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;

    async function fetchBook() {
      try {
        const data = await api.get<BookDetail>(`/books/${bookId}`);
        setBook(data);
        setLoading(false);

        if (
          data.status === "uploading" ||
          data.status === "parsing" ||
          data.status === "extracting"
        ) {
          interval = setInterval(async () => {
            try {
              const updated = await api.get<BookDetail>(`/books/${bookId}`);
              setBook(updated);
              if (updated.status === "ready" || updated.status === "error") {
                if (interval) clearInterval(interval);
              }
            } catch {
              // ignore polling errors
            }
          }, 3000);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : t("not_found"));
        setLoading(false);
      }
    }

    fetchBook();
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [bookId, t]);

  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (error || !book) {
    return (
      <div className="mx-auto max-w-5xl px-6 py-10">
        <Link href="/library">
          <Button variant="ghost" size="sm" className="mb-6 gap-1.5">
            <ArrowLeft className="h-4 w-4" />
            {t("back_to_library")}
          </Button>
        </Link>
        <div className="flex flex-col items-center justify-center py-24">
          <AlertCircle className="h-10 w-10 text-destructive" />
          <p className="mt-4 text-sm text-muted-foreground">
            {error || t("not_found")}
          </p>
        </div>
      </div>
    );
  }

  const isProcessing = ["uploading", "parsing", "extracting"].includes(
    book.status,
  );
  const statusKey = ["uploading", "parsing", "extracting", "ready", "error"].includes(
    book.status,
  )
    ? book.status
    : "ready";
  const statusVariant =
    book.status === "ready"
      ? "success"
      : book.status === "error"
        ? "destructive"
        : "mono";

  return (
    <div className="mx-auto w-full max-w-5xl px-5 py-10 sm:px-8 sm:py-12">
      <Link href="/library">
        <Button
          variant="ghost"
          size="sm"
          className="mb-7 gap-1.5 rounded-full text-muted-foreground"
        >
          <ArrowLeft className="h-3.5 w-3.5" />
          {t("back_to_library")}
        </Button>
      </Link>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="flex flex-wrap items-start justify-between gap-6">
          <div className="min-w-0">
            <p className="eyebrow">{t("eyebrow")}</p>
            <h1 className="mt-3 font-display text-4xl font-semibold tracking-tight sm:text-5xl">
              {book.title}
            </h1>
            {book.author && book.author !== "Unknown" && (
              <p className="mt-3 font-mono text-[11px] uppercase tracking-[0.12em] text-muted-foreground">
                {t("by_author", { author: book.author })}
              </p>
            )}
          </div>
          <div className="flex items-center gap-2">
            <Badge variant={statusVariant}>{tStatus(statusKey)}</Badge>
            <Button
              variant="ghost"
              size="icon"
              className="text-muted-foreground hover:text-destructive"
              onClick={handleDelete}
              disabled={deleting}
            >
              {deleting ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Trash2 className="h-4 w-4" />
              )}
            </Button>
          </div>
        </div>

        {isProcessing && (
          <div className="mt-10">
            <ProcessingAnimation status={book.status as BookStatus} />
            <p className="mt-6 text-center text-[13px] text-muted-foreground">
              {t("processing_note")}
            </p>
          </div>
        )}

        {book.status === "error" && (
          <div className="mt-8 rounded-2xl border border-destructive/25 bg-destructive/5 px-5 py-4">
            <p className="text-[13.5px] text-destructive">
              {t("error_processing")}
            </p>
          </div>
        )}

        {book.status === "ready" && (
          <>
            <div className="mt-10">
              <BookStats book={book} />
            </div>

            <div className="mt-8 flex gap-3">
              <Link href={`/book/${bookId}/read`}>
                <Button size="lg" variant="primary" className="gap-2 rounded-full px-6">
                  <BookOpen className="h-4 w-4" />
                  {t("start_reading")}
                </Button>
              </Link>
            </div>

            <div className="mt-12">
              <p className="eyebrow">{t("tree.eyebrow")}</p>
              <div className="mt-4 rounded-2xl bg-card p-2 ring-1 ring-border/60">
                <ChapterTree chapters={book.chapters} bookId={bookId} />
              </div>
            </div>
          </>
        )}
      </motion.div>
    </div>
  );
}
