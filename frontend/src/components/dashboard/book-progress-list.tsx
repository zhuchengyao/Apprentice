"use client";

import Link from "next/link";
import { useTranslations } from "next-intl";
import { ArrowRight, BookOpen } from "lucide-react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

interface BookProgress {
  id: string;
  title: string;
  status: string;
  total_pages: number;
  total_kps: number;
  mastered_kps: number;
  progress: number;
}

interface BookProgressListProps {
  books: BookProgress[];
}

export function BookProgressList({ books }: BookProgressListProps) {
  const t = useTranslations("dashboard.progress_list");
  return (
    <div className="flex h-full flex-col rounded-2xl bg-card ring-1 ring-border/60">
      <div className="flex items-center justify-between border-b border-border/60 px-5 py-4">
        <div>
          <p className="eyebrow">{t("eyebrow")}</p>
          <h2 className="mt-1 font-heading text-base font-semibold tracking-tight">
            {t("heading")}
          </h2>
        </div>
        <Link
          href="/library"
          className="group flex items-center gap-1 font-mono text-[10px] uppercase tracking-[0.12em] text-muted-foreground transition-colors hover:text-foreground"
        >
          {t("library_link")}
          <ArrowRight className="h-3 w-3 transition-transform group-hover:translate-x-0.5" />
        </Link>
      </div>

      {books.length === 0 ? (
        <div className="flex flex-1 flex-col items-center justify-center gap-3 p-10 text-center">
          <BookOpen className="h-6 w-6 text-muted-foreground/50" />
          <p className="text-[13px] text-muted-foreground">{t("empty")}</p>
        </div>
      ) : (
        <ul className="divide-y divide-border/50">
          {books.map((book) => {
            const pct = Math.round(book.progress * 100);
            return (
              <li key={book.id}>
                <Link
                  href={`/book/${book.id}`}
                  className="group flex items-center gap-4 px-5 py-4 transition-colors hover:bg-subtle/50"
                >
                  <div className="min-w-0 flex-1">
                    <p className="truncate font-heading text-[14.5px] font-medium text-foreground">
                      {book.title}
                    </p>
                    <div className="mt-2 flex items-center gap-3">
                      <div className="h-1 flex-1 overflow-hidden rounded-full bg-subtle ring-1 ring-inset ring-border/60">
                        <div
                          className={cn(
                            "h-full rounded-full transition-all duration-500",
                            pct === 100
                              ? "bg-success"
                              : pct > 0
                                ? "bg-primary"
                                : "bg-transparent",
                          )}
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                      <span className="shrink-0 font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground tabular-nums">
                        {book.mastered_kps}/{book.total_kps}
                      </span>
                    </div>
                  </div>
                  <div className="flex shrink-0 items-center gap-3">
                    <StatusBadge status={book.status} />
                    <ArrowRight className="h-3.5 w-3.5 text-muted-foreground/60 transition-transform group-hover:translate-x-0.5 group-hover:text-foreground" />
                  </div>
                </Link>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const t = useTranslations("library.status");
  const known = ["uploading", "parsing", "extracting", "ready", "error"];
  const key = known.includes(status) ? status : "ready";
  if (status === "ready") return <Badge variant="success">{t(key)}</Badge>;
  if (status === "error") return <Badge variant="destructive">{t(key)}</Badge>;
  return <Badge variant="mono">{known.includes(status) ? t(key) : status}</Badge>;
}
