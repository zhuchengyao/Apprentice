"use client";

import { useTranslations } from "next-intl";
import { cn } from "@/lib/utils";

interface StreakDay {
  date: string;
  minutes_studied: number;
  points_mastered: number;
}

interface StreakCalendarProps {
  days: StreakDay[];
  currentStreak: number;
  totalMinutes: number;
}

export function StreakCalendar({
  days,
  totalMinutes,
}: StreakCalendarProps) {
  const t = useTranslations("dashboard.streaks");
  const activeDates = new Map(days.map((d) => [d.date, d]));

  const cells: { date: string; active: boolean; minutes: number }[] = [];
  const today = new Date();
  for (let i = 29; i >= 0; i--) {
    const d = new Date(today);
    d.setDate(d.getDate() - i);
    const iso = d.toISOString().split("T")[0];
    const entry = activeDates.get(iso);
    cells.push({
      date: iso,
      active: !!entry,
      minutes: entry?.minutes_studied || 0,
    });
  }

  const hours = Math.floor(totalMinutes / 60);
  const mins = totalMinutes % 60;
  const totalLabel =
    hours > 0
      ? t("hours_minutes", { hours, minutes: mins })
      : t("minutes_only", { minutes: mins });

  return (
    <div className="rounded-2xl bg-card p-6 ring-1 ring-border/60">
      <div className="flex items-start justify-between gap-6">
        <div>
          <p className="eyebrow">{t("eyebrow")}</p>
          <h2 className="mt-1 font-heading text-base font-semibold tracking-tight">
            {t("heading")}
          </h2>
        </div>
        <div className="text-right">
          <p className="font-display text-2xl font-semibold leading-none tracking-tight tabular-nums">
            {totalLabel}
          </p>
          <p className="mt-1.5 font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground">
            {t("total_time")}
          </p>
        </div>
      </div>

      <div className="mt-5 flex gap-1">
        {cells.map((cell) => (
          <div
            key={cell.date}
            className={cn(
              "h-6 flex-1 rounded-sm transition-colors",
              cell.active
                ? cell.minutes >= 30
                  ? "bg-primary"
                  : "bg-primary/30"
                : "bg-subtle ring-1 ring-inset ring-border/50",
            )}
            title={`${cell.date} · ${
              cell.active
                ? t("minutes_short", { count: cell.minutes })
                : t("no_activity")
            }`}
          />
        ))}
      </div>
      <div className="mt-2.5 flex items-center justify-between font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground">
        <span>{t("thirty_days_ago")}</span>
        <span>{t("today")}</span>
      </div>
    </div>
  );
}
