"use client";

import { BookOpen, Lightbulb, Layers, FileText } from "lucide-react";
import type { BookDetail } from "@/lib/types";

interface BookStatsProps {
  book: BookDetail;
}

export function BookStats({ book }: BookStatsProps) {
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
    { icon: Layers, label: "Chapters", value: book.chapters.length },
    { icon: BookOpen, label: "Sections", value: totalSections },
    { icon: Lightbulb, label: "Concepts", value: totalKPs },
    { icon: FileText, label: "Pages", value: book.total_pages },
  ];

  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
      {stats.map(({ icon: Icon, label, value }) => (
        <div
          key={label}
          className="flex flex-col items-center gap-1.5 rounded-xl border bg-card p-4"
        >
          <Icon className="h-5 w-5 text-muted-foreground" />
          <span className="text-2xl font-bold">{value}</span>
          <span className="text-xs text-muted-foreground">{label}</span>
        </div>
      ))}
    </div>
  );
}
