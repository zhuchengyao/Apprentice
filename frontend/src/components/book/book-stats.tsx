"use client";

import { useTranslations } from "next-intl";
import { BookOpen, Lightbulb, Layers, FileText } from "lucide-react";
import type { BookDetail } from "@/lib/types";

interface BookStatsProps {
  book: BookDetail;
}

export function BookStats({ book }: BookStatsProps) {
  const t = useTranslations("book.stats");

  const totalSections = book.chapters.reduce(
    (sum, ch) => sum + ch.sections.length,
    0,
  );
  const totalKPs = book.chapters.reduce(
    (sum, ch) =>
      sum +
      ch.sections.reduce((s, sec) => s + sec.knowledge_points.length, 0),
    0,
  );

  const stats = [
    { icon: Layers, label: t("chapters"), value: book.chapters.length },
    { icon: BookOpen, label: t("sections"), value: totalSections },
    { icon: Lightbulb, label: t("concepts"), value: totalKPs },
    { icon: FileText, label: t("pages"), value: book.total_pages },
  ];

  return (
    <div className="grid grid-cols-2 gap-px overflow-hidden rounded-2xl bg-border/60 ring-1 ring-border/60 sm:grid-cols-4">
      {stats.map(({ icon: Icon, label, value }, i) => (
        <div
          key={label}
          className="relative flex flex-col gap-3 bg-card p-5 transition-colors hover:bg-card/80"
        >
          <div className="flex items-center justify-between">
            <span className="eyebrow">{label}</span>
            <Icon className="h-3.5 w-3.5 text-muted-foreground/60" />
          </div>
          <p className="font-display text-3xl font-semibold leading-none tracking-tight tabular-nums">
            {value}
          </p>
          <span className="absolute top-3 right-3 font-mono text-[10px] tabular-nums text-muted-foreground/40">
            0{i + 1}
          </span>
        </div>
      ))}
    </div>
  );
}
