"use client";

import { useEffect, useState, useCallback, useMemo } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { useFormatter, useTranslations } from "next-intl";
import {
  AlertCircle,
  ArrowRight,
  BookOpen,
  Loader2,
  Plus,
  Search,
  Trash2,
  X,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { BookGrid } from "@/components/library/book-grid";
import { UploadDialog } from "@/components/upload/upload-dialog";
import { api } from "@/lib/api-client";
import type { Book } from "@/lib/types";

const PROCESSING_STATUSES = ["uploading", "parsing", "extracting"] as const;

export default function LibraryPage() {
  const t = useTranslations("library");
  const format = useFormatter();
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);
  const [selectMode, setSelectMode] = useState(false);
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [deleting, setDeleting] = useState(false);
  const [uploadOpen, setUploadOpen] = useState(false);
  const [query, setQuery] = useState("");

  const refresh = useCallback(async () => {
    try {
      const data = await api.get<{ books: Book[] }>("/books");
      setBooks(data.books);
      setLoadError(false);
      return data.books;
    } catch {
      setLoadError(true);
      return null;
    }
  }, []);

  useEffect(() => {
    refresh().finally(() => setLoading(false));
  }, [refresh]);

  // Poll while any book is processing. Re-arms whenever a new processing book
  // appears (e.g. an upload started from the side-nav while we're on this page).
  const hasProcessing = books.some((b) =>
    (PROCESSING_STATUSES as readonly string[]).includes(b.status),
  );

  useEffect(() => {
    if (!hasProcessing) return;
    const interval = setInterval(refresh, 4000);
    return () => clearInterval(interval);
  }, [hasProcessing, refresh]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return books;
    return books.filter(
      (b) =>
        b.title.toLowerCase().includes(q) ||
        (b.author ?? "").toLowerCase().includes(q),
    );
  }, [books, query]);

  // Selected ids that are also visible — this is what delete operates on.
  // Without this, a user could select books, type a query that hides them,
  // then delete books they can no longer see.
  const visibleSelectedIds = useMemo(() => {
    if (selectedIds.size === 0) return selectedIds;
    const visible = new Set<string>();
    for (const b of filtered) {
      if (selectedIds.has(b.id)) visible.add(b.id);
    }
    return visible;
  }, [filtered, selectedIds]);

  const toggleSelect = useCallback((id: string) => {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }, []);

  const exitSelectMode = useCallback(() => {
    setSelectMode(false);
    setSelectedIds(new Set());
  }, []);

  const handleDeleteSelected = useCallback(async () => {
    if (visibleSelectedIds.size === 0) return;
    const count = visibleSelectedIds.size;
    if (!confirm(t("delete_confirm", { count }))) return;

    setDeleting(true);
    try {
      await Promise.all(
        Array.from(visibleSelectedIds).map((id) => api.delete(`/books/${id}`)),
      );
      setBooks((prev) => prev.filter((b) => !visibleSelectedIds.has(b.id)));
      exitSelectMode();
    } catch {
      alert(t("delete_partial_failure"));
    } finally {
      setDeleting(false);
    }
  }, [visibleSelectedIds, exitSelectMode, t]);

  const ready = books.filter((b) => b.status === "ready").length;
  const active = books.filter((b) =>
    (PROCESSING_STATUSES as readonly string[]).includes(b.status),
  ).length;

  // Most-recently-opened in-progress book — anchors the "continue" banner.
  // Hidden during search so it doesn't fight with filtered results.
  const continueBook = useMemo(() => {
    if (query.trim()) return null;
    const candidates = books.filter(
      (b) => b.status === "ready" && b.progress > 0 && b.progress < 100,
    );
    if (candidates.length === 0) return null;
    return candidates.reduce((latest, b) =>
      new Date(b.updated_at) > new Date(latest.updated_at) ? b : latest,
    );
  }, [books, query]);

  return (
    <div className="mx-auto w-full max-w-6xl px-5 py-10 sm:px-8 sm:py-12">
      {/* Hero */}
      <div className="flex flex-wrap items-end justify-between gap-6">
        <div>
          <p className="eyebrow">{t("eyebrow")}</p>
          <h1 className="mt-3 font-display text-4xl font-semibold tracking-tight sm:text-5xl">
            {t("heading")}
          </h1>
          <p className="mt-3 max-w-xl text-[14.5px] leading-relaxed text-muted-foreground">
            {books.length > 0 ? (
              <>
                <span className="font-mono tabular-nums">
                  {t("book_count", { count: books.length })}
                </span>{" · "}
                <span>{t("ready_to_study", { count: ready })}</span>
                {active > 0 && (
                  <>
                    {" · "}
                    <span>{t("in_progress", { count: active })}</span>
                  </>
                )}
              </>
            ) : (
              t("empty_lede")
            )}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {selectMode ? (
            <>
              <span className="font-mono text-[11px] uppercase tracking-[0.12em] text-muted-foreground">
                {t("selected", { count: visibleSelectedIds.size })}
              </span>
              <Button
                size="sm"
                variant="destructive"
                className="gap-1.5"
                disabled={visibleSelectedIds.size === 0 || deleting}
                onClick={handleDeleteSelected}
              >
                {deleting ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Trash2 className="h-4 w-4" />
                )}
                {t("delete")}
              </Button>
              <Button size="icon-sm" variant="ghost" onClick={exitSelectMode}>
                <X className="h-4 w-4" />
              </Button>
            </>
          ) : (
            <>
              {books.length > 0 && (
                <Button
                  size="sm"
                  variant="outline"
                  className="gap-1.5 rounded-full"
                  onClick={() => setSelectMode(true)}
                >
                  <Trash2 className="h-3.5 w-3.5" />
                  {t("select")}
                </Button>
              )}
              <Button
                size="sm"
                variant="primary"
                className="gap-1.5 rounded-full"
                onClick={() => setUploadOpen(true)}
              >
                <Plus className="h-3.5 w-3.5" />
                {t("new_book")}
              </Button>
            </>
          )}
        </div>
      </div>

      {/* Search */}
      {books.length > 4 && (
        <div className="mt-8 max-w-sm">
          <div className="relative">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-muted-foreground" />
            <Input
              type="search"
              placeholder={t("search_placeholder")}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="pl-9"
            />
          </div>
        </div>
      )}

      {/* Continue reading — single signature card, only when a book is in progress */}
      {continueBook && !selectMode && !loading && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="relative mt-8 overflow-hidden rounded-2xl bg-card ring-1 ring-border/60 shadow-editorial"
        >
          <div aria-hidden className="aurora pointer-events-none absolute inset-0" />
          <div className="relative flex flex-wrap items-center gap-5 p-6 sm:p-7">
            <div className="min-w-0 flex-1">
              <p className="eyebrow text-primary">{t("continue.eyebrow")}</p>
              <h2 className="mt-2 font-heading text-[22px] font-semibold leading-tight tracking-tight">
                {continueBook.total_knowledge_points > 0 ? (
                  <>
                    <span className="italic text-primary tabular-nums">
                      {continueBook.mastered_knowledge_points}
                    </span>
                    <span className="text-muted-foreground">
                      {" / "}
                      {continueBook.total_knowledge_points}
                    </span>{" "}
                    <span className="text-foreground/90">
                      {t("book_card.concepts_suffix")}
                    </span>
                  </>
                ) : (
                  t("continue.heading_no_count")
                )}
              </h2>
              <p className="mt-1 truncate font-mono text-[11px] uppercase tracking-[0.12em] text-muted-foreground">
                {continueBook.title}
                {" · "}
                {t("continue.subtitle", {
                  percent: Math.round(continueBook.progress),
                  when: format.relativeTime(new Date(continueBook.updated_at)),
                })}
              </p>
            </div>
            <Link href={`/book/${continueBook.id}`} className="shrink-0">
              <Button size="lg" variant="primary" className="gap-2 rounded-full">
                {t("continue.cta")}
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
          </div>
        </motion.div>
      )}

      {/* Grid / empty / error */}
      <div className="mt-10">
        {loadError && books.length === 0 && !loading ? (
          <div className="flex flex-col items-center justify-center rounded-3xl border border-destructive/30 bg-destructive/5 px-6 py-16 text-center">
            <AlertCircle className="h-9 w-9 text-destructive" />
            <p className="mt-4 text-[14px] text-foreground">
              {t("load_failed")}
            </p>
            <Button
              size="sm"
              variant="outline"
              className="mt-5 rounded-full"
              onClick={() => {
                setLoading(true);
                refresh().finally(() => setLoading(false));
              }}
            >
              {t("retry")}
            </Button>
          </div>
        ) : loading ? (
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
            {[...Array(4)].map((_, i) => (
              <div
                key={i}
                className="overflow-hidden rounded-2xl ring-1 ring-border/60 bg-card"
              >
                <div className="shimmer aspect-[4/3]" />
                <div className="space-y-2 p-4">
                  <div className="shimmer h-3 w-3/4 rounded" />
                  <div className="shimmer h-3 w-1/2 rounded" />
                </div>
              </div>
            ))}
          </div>
        ) : filtered.length > 0 ? (
          <BookGrid
            books={filtered}
            selectedIds={selectMode ? selectedIds : undefined}
            onToggleSelect={selectMode ? toggleSelect : undefined}
          />
        ) : books.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="relative flex flex-col items-center justify-center overflow-hidden rounded-3xl border border-dashed border-border/80 bg-subtle/40 px-6 py-24 text-center"
          >
            <div
              aria-hidden
              className="aurora pointer-events-none absolute inset-0 opacity-40"
            />
            <div className="relative flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10 text-primary ring-1 ring-primary/15">
              <BookOpen className="h-6 w-6" />
            </div>
            <h3 className="relative mt-6 font-heading text-2xl font-semibold tracking-tight">
              {t("empty_title")}
            </h3>
            <p className="relative mt-2 max-w-sm text-[14px] leading-relaxed text-muted-foreground">
              {t("empty_body")}
            </p>
            <Button
              size="lg"
              variant="primary"
              className="relative mt-7 gap-1.5 rounded-full"
              onClick={() => setUploadOpen(true)}
            >
              <Plus className="h-4 w-4" />
              {t("empty_cta")}
            </Button>
          </motion.div>
        ) : (
          <div className="py-16 text-center">
            <p className="font-mono text-[11px] uppercase tracking-[0.14em] text-muted-foreground">
              {t("no_matches_title")}
            </p>
            <p className="mt-2 text-sm text-muted-foreground">
              {t("no_matches_body", { query })}
            </p>
          </div>
        )}
      </div>

      <UploadDialog open={uploadOpen} onClose={() => setUploadOpen(false)} />
    </div>
  );
}
