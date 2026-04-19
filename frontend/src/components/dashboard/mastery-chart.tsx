"use client";

import { useTranslations } from "next-intl";

interface MasteryEntry {
  date: string;
  points_mastered: number;
}

interface MasteryChartProps {
  data: MasteryEntry[];
  totalMastered: number;
  totalKPs: number;
}

export function MasteryChart({
  data,
  totalMastered,
  totalKPs,
}: MasteryChartProps) {
  const t = useTranslations("dashboard.mastery");
  const max = Math.max(1, ...data.map((d) => d.points_mastered));
  const progress =
    totalKPs > 0 ? Math.round((totalMastered / totalKPs) * 100) : 0;

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
          <span className="font-display text-3xl font-semibold leading-none tracking-tight tabular-nums">
            {progress}
            <span className="text-muted-foreground">%</span>
          </span>
          <p className="mt-1.5 font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground">
            {t("overall")}
          </p>
        </div>
      </div>

      <div className="mt-5 h-1.5 overflow-hidden rounded-full bg-subtle ring-1 ring-inset ring-border/60">
        <div
          className="h-full rounded-full bg-primary transition-all duration-700"
          style={{ width: `${progress}%` }}
        />
      </div>
      <p className="mt-2 font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground tabular-nums">
        {t("mastered_of", { mastered: totalMastered, total: totalKPs })}
      </p>

      {data.length > 0 && (
        <>
          <h3 className="mt-6 font-mono text-[10px] uppercase tracking-[0.12em] text-muted-foreground">
            {t("per_day")}
          </h3>
          <div
            className="mt-3 flex items-end gap-[3px]"
            style={{ height: 80 }}
          >
            {data.map((d) => {
              const pct = (d.points_mastered / max) * 100;
              return (
                <div
                  key={d.date}
                  className="flex-1 rounded-sm bg-primary/30 transition-colors hover:bg-primary"
                  style={{ height: `${Math.max(pct, 3)}%` }}
                  title={`${d.date}: ${d.points_mastered}`}
                />
              );
            })}
          </div>
        </>
      )}
    </div>
  );
}
