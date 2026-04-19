"use client";

import { useTranslations } from "next-intl";
import { BookOpen, Brain, MessageSquare, Flame } from "lucide-react";

interface StatCardsProps {
  totalBooks: number;
  totalKPs: number;
  masteredKPs: number;
  totalConversations: number;
  totalMessages: number;
  currentStreak: number;
}

export function StatCards({
  totalBooks,
  totalKPs,
  masteredKPs,
  totalConversations,
  totalMessages,
  currentStreak,
}: StatCardsProps) {
  const t = useTranslations("dashboard.stats");
  const stats = [
    {
      label: t("books"),
      value: totalBooks.toString(),
      icon: BookOpen,
      sub: t("books_sub"),
    },
    {
      label: t("concepts"),
      value: `${masteredKPs}`,
      icon: Brain,
      sub:
        totalKPs > 0
          ? t("concepts_of", {
              total: totalKPs,
              percent: Math.round((masteredKPs / totalKPs) * 100),
            })
          : t("concepts_none"),
    },
    {
      label: t("chats"),
      value: totalConversations.toString(),
      icon: MessageSquare,
      sub: t("chats_sub", { count: totalMessages }),
    },
    {
      label: t("streak"),
      value: currentStreak.toString(),
      icon: Flame,
      sub: t("streak_sub", { count: currentStreak }),
    },
  ];

  return (
    <div className="grid grid-cols-1 gap-px overflow-hidden rounded-2xl bg-border/60 ring-1 ring-border/60 sm:grid-cols-2 lg:grid-cols-4">
      {stats.map((s, i) => (
        <div
          key={s.label}
          className="relative flex flex-col gap-3 bg-card p-5 transition-colors hover:bg-card/80"
        >
          <div className="flex items-center justify-between">
            <span className="eyebrow">{s.label}</span>
            <s.icon className="h-3.5 w-3.5 text-muted-foreground/60" />
          </div>
          <div>
            <p className="font-display text-4xl font-semibold leading-none tracking-tight tabular-nums">
              {s.value}
            </p>
            <p className="mt-1.5 font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground">
              {s.sub}
            </p>
          </div>
          <span className="absolute top-3 right-3 font-mono text-[10px] tabular-nums text-muted-foreground/40">
            0{i + 1}
          </span>
        </div>
      ))}
    </div>
  );
}
