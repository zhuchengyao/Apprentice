"use client";

import { useEffect, useState } from "react";
import { useTranslations } from "next-intl";
import { api } from "@/lib/api-client";
import type { UsageDailyEntry, UsageBreakdown } from "@/lib/types";

interface UsageData {
  period_days: number;
  total_calls: number;
  total_cost_usd: number;
  total_credits_used: number;
  breakdown: UsageBreakdown[];
  daily: UsageDailyEntry[];
}

export function UsageChart() {
  const t = useTranslations("billing.usage");
  const [data, setData] = useState<UsageData | null>(null);

  useEffect(() => {
    api
      .get<UsageData>("/billing/usage?days=30")
      .then(setData)
      .catch(() => {});
  }, []);

  if (!data) {
    return (
      <div className="rounded-2xl bg-card p-6 ring-1 ring-border/60">
        <p className="eyebrow">{t("eyebrow")}</p>
        <h2 className="mt-1 font-display text-2xl font-semibold tracking-tight">
          {t("heading")}
        </h2>
        <div className="mt-5 h-32 overflow-hidden rounded-xl ring-1 ring-border/60">
          <div className="shimmer h-full w-full" />
        </div>
      </div>
    );
  }

  const maxCredits = Math.max(1, ...data.daily.map((d) => d.credits_used));

  return (
    <div className="rounded-2xl bg-card p-6 ring-1 ring-border/60">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="eyebrow">{t("eyebrow")}</p>
          <h2 className="mt-1 font-display text-2xl font-semibold tracking-tight">
            {t("heading")}
          </h2>
        </div>
        <div className="text-right">
          <p className="font-display text-3xl font-semibold leading-none tracking-tight tabular-nums">
            {data.total_credits_used.toLocaleString()}
          </p>
          <p className="mt-1.5 font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground">
            {t("credits_used")}
          </p>
        </div>
      </div>

      {data.daily.length > 0 ? (
        <div
          className="mt-6 flex items-end gap-[2px] rounded-xl bg-subtle/60 p-3 ring-1 ring-border/40"
          style={{ height: 120 }}
        >
          {data.daily.map((d) => {
            const pct = (d.credits_used / maxCredits) * 100;
            return (
              <div
                key={d.date}
                className="flex-1 rounded-t bg-primary/40 transition-colors hover:bg-primary"
                style={{ height: `${Math.max(pct, 2)}%` }}
                title={t("bar_tooltip", {
                  date: d.date,
                  credits: d.credits_used,
                  calls: d.calls,
                })}
              />
            );
          })}
        </div>
      ) : (
        <p className="mt-6 text-[13.5px] text-muted-foreground">{t("empty")}</p>
      )}

      {data.breakdown.length > 0 && (
        <div className="mt-6 border-t border-border/60 pt-5">
          <h3 className="font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground">
            {t("breakdown")}
          </h3>
          <div className="mt-3 space-y-2">
            {data.breakdown.map((b) => (
              <div
                key={b.caller}
                className="flex items-center justify-between text-[13.5px]"
              >
                <span>{formatCaller(b.caller, t)}</span>
                <span className="tabular-nums text-muted-foreground">
                  {b.credits_used.toLocaleString()} · {b.calls}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

const KNOWN_CALLERS = new Set([
  "books",
  "pages",
  "knowledge",
  "teaching",
  "tutor",
  "vision",
  "other",
]);

function formatCaller(
  caller: string,
  t: ReturnType<typeof useTranslations>,
): string {
  const normalized = caller.toLowerCase();
  if (KNOWN_CALLERS.has(normalized)) {
    return t(`caller_${normalized}` as never);
  }
  return caller.replace(/_/g, " ");
}
