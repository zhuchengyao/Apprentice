"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import {
  Users,
  BookOpen,
  DollarSign,
  TrendingUp,
  TrendingDown,
  Activity,
  Loader2,
} from "lucide-react";
import { cn } from "@/lib/utils";

type Overview = {
  period_days: number;
  users: {
    total: number;
    active: number;
    new_today: number;
    new_in_period: number;
    active_in_period: number;
  };
  books: { total: number; ready: number; failed: number };
  revenue: { total_usd: number; by_type: Record<string, number> };
  cost: {
    total_usd: number;
    total_calls: number;
    input_tokens: number;
    output_tokens: number;
    by_caller: { caller: string; calls: number; cost_usd: number }[];
    by_model: { model: string; calls: number; cost_usd: number }[];
  };
  profit: { total_usd: number };
  daily: { date: string; cost_usd: number; revenue_usd: number }[];
  top_consumers: {
    user_id: string;
    email: string;
    name: string;
    calls: number;
    cost_usd: number;
  }[];
  subscriptions: { plan_name: string; display_name: string; count: number }[];
  tutor: { total_conversations: number; messages_in_period: number };
};

const PERIOD_OPTIONS = [
  { days: 7, key: "period_7" },
  { days: 30, key: "period_30" },
  { days: 90, key: "period_90" },
] as const;

export default function AdminOverviewPage() {
  const t = useTranslations("admin.overview");
  const tCommon = useTranslations("admin");
  const [days, setDays] = useState(30);
  const [data, setData] = useState<Overview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    fetch(`/api/admin/overview?days=${days}`)
      .then(async (res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((d) => {
        if (!cancelled) setData(d);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [days]);

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="p-8">
        <p className="text-sm text-destructive">
          {error || tCommon("failed_load")}
        </p>
      </div>
    );
  }

  const profitPositive = data.profit.total_usd >= 0;
  const maxDaily = Math.max(
    1,
    ...data.daily.map((d) => Math.max(d.cost_usd, d.revenue_usd)),
  );

  return (
    <div className="space-y-6 p-8">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="eyebrow">{t("eyebrow")}</p>
          <h1 className="mt-2 font-display text-4xl font-semibold tracking-tight">
            {t("heading")}
          </h1>
          <p className="mt-2 text-[13.5px] text-muted-foreground">
            {t("lede", { days })}
          </p>
        </div>
        <div className="flex gap-0.5 rounded-full bg-subtle p-0.5 ring-1 ring-border/60">
          {PERIOD_OPTIONS.map((opt) => (
            <button
              key={opt.days}
              onClick={() => setDays(opt.days)}
              className={cn(
                "rounded-full px-3 py-1.5 font-mono text-[10px] uppercase tracking-[0.08em] transition-colors",
                days === opt.days
                  ? "bg-background text-foreground shadow-sm ring-1 ring-border/70"
                  : "text-muted-foreground hover:text-foreground",
              )}
            >
              {t(opt.key)}
            </button>
          ))}
        </div>
      </header>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          icon={Users}
          label={t("kpi_total_users")}
          value={data.users.total.toString()}
          sub={t("kpi_total_users_sub", {
            active: data.users.active,
            new: data.users.new_in_period,
          })}
        />
        <StatCard
          icon={BookOpen}
          label={t("kpi_books")}
          value={data.books.total.toString()}
          sub={t("kpi_books_sub", {
            ready: data.books.ready,
            failed: data.books.failed,
          })}
        />
        <StatCard
          icon={DollarSign}
          label={t("kpi_revenue")}
          value={`$${data.revenue.total_usd.toFixed(2)}`}
          sub={formatRevenueBreakdown(data.revenue.by_type, t)}
        />
        <StatCard
          icon={profitPositive ? TrendingUp : TrendingDown}
          label={t("kpi_profit")}
          value={`$${data.profit.total_usd.toFixed(2)}`}
          sub={t("kpi_cost_prefix", { cost: data.cost.total_usd.toFixed(2) })}
          tone={profitPositive ? "positive" : "negative"}
        />
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <StatCard
          icon={Activity}
          label={t("kpi_ai_calls")}
          value={data.cost.total_calls.toLocaleString()}
          sub={t("kpi_ai_calls_sub", {
            in: formatTokens(data.cost.input_tokens),
            out: formatTokens(data.cost.output_tokens),
          })}
          compact
        />
        <StatCard
          icon={Users}
          label={t("kpi_active_in_period")}
          value={data.users.active_in_period.toString()}
          sub={t("kpi_active_in_period_sub", { today: data.users.new_today })}
          compact
        />
        <StatCard
          icon={Activity}
          label={t("kpi_tutor_messages")}
          value={data.tutor.messages_in_period.toLocaleString()}
          sub={t("kpi_tutor_messages_sub", {
            total: data.tutor.total_conversations,
          })}
          compact
        />
      </div>

      <section className="rounded-2xl bg-card p-6 ring-1 ring-border/60">
        <h2 className="font-display text-xl font-semibold tracking-tight">
          {t("revenue_vs_cost")}
        </h2>
        {data.daily.length === 0 ? (
          <p className="py-8 text-center text-sm text-muted-foreground">
            {t("no_data")}
          </p>
        ) : (
          <div className="mt-4 flex h-40 items-end gap-1">
            {data.daily.map((d) => {
              const costH = (d.cost_usd / maxDaily) * 100;
              const revH = (d.revenue_usd / maxDaily) * 100;
              return (
                <div
                  key={d.date}
                  className="group relative flex flex-1 flex-col items-center gap-0.5"
                  title={`${d.date}\n${t("legend_revenue")}: $${d.revenue_usd.toFixed(2)}\n${t("legend_cost")}: $${d.cost_usd.toFixed(2)}`}
                >
                  <div className="flex h-full w-full flex-col justify-end">
                    <div
                      className="w-full rounded-t bg-success/70"
                      style={{ height: `${revH}%` }}
                    />
                    <div
                      className="mt-0.5 w-full rounded-t bg-destructive/70"
                      style={{ height: `${costH}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        )}
        <div className="mt-4 flex gap-4 font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground">
          <span className="flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-sm bg-success/70" />{" "}
            {t("legend_revenue")}
          </span>
          <span className="flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-sm bg-destructive/70" />{" "}
            {t("legend_cost")}
          </span>
        </div>
      </section>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <section className="rounded-2xl bg-card p-6 ring-1 ring-border/60">
          <h2 className="mb-4 font-display text-xl font-semibold tracking-tight">
            {t("cost_by_caller")}
          </h2>
          <BreakdownTable
            emptyLabel={t("no_data")}
            rows={data.cost.by_caller.map((c) => ({
              label: c.caller,
              calls: c.calls,
              cost: c.cost_usd,
            }))}
          />
        </section>

        <section className="rounded-2xl bg-card p-6 ring-1 ring-border/60">
          <h2 className="mb-4 font-display text-xl font-semibold tracking-tight">
            {t("cost_by_model")}
          </h2>
          <BreakdownTable
            emptyLabel={t("no_data")}
            rows={data.cost.by_model.map((c) => ({
              label: c.model,
              calls: c.calls,
              cost: c.cost_usd,
            }))}
          />
        </section>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <section className="rounded-2xl bg-card p-6 ring-1 ring-border/60">
          <h2 className="mb-4 font-display text-xl font-semibold tracking-tight">
            {t("top_consumers")}
          </h2>
          {data.top_consumers.length === 0 ? (
            <p className="text-sm text-muted-foreground">{t("no_data")}</p>
          ) : (
            <table className="w-full text-sm">
              <thead className="font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground">
                <tr>
                  <th className="pb-2 text-left font-normal">
                    {t("col_user")}
                  </th>
                  <th className="pb-2 text-right font-normal">
                    {t("col_calls")}
                  </th>
                  <th className="pb-2 text-right font-normal">
                    {t("col_cost")}
                  </th>
                </tr>
              </thead>
              <tbody>
                {data.top_consumers.map((c) => (
                  <tr
                    key={c.user_id}
                    className="border-t border-border/40"
                  >
                    <td className="py-2.5">
                      <Link
                        href={`/admin/users/${c.user_id}`}
                        className="text-foreground hover:underline"
                      >
                        {c.email}
                      </Link>
                      <div className="text-xs text-muted-foreground">
                        {c.name}
                      </div>
                    </td>
                    <td className="py-2.5 text-right tabular-nums">
                      {c.calls.toLocaleString()}
                    </td>
                    <td className="py-2.5 text-right font-mono text-[12.5px] text-muted-foreground">
                      ${c.cost_usd.toFixed(4)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>

        <section className="rounded-2xl bg-card p-6 ring-1 ring-border/60">
          <h2 className="mb-4 font-display text-xl font-semibold tracking-tight">
            {t("subscriptions_heading")}
          </h2>
          {data.subscriptions.length === 0 ? (
            <p className="text-sm text-muted-foreground">{t("no_subs")}</p>
          ) : (
            <div className="space-y-2">
              {data.subscriptions.map((s) => (
                <div
                  key={s.plan_name}
                  className="flex items-center justify-between rounded-xl bg-subtle px-3.5 py-2.5 ring-1 ring-border/40"
                >
                  <span className="text-sm">{s.display_name}</span>
                  <span className="font-mono text-sm tabular-nums text-muted-foreground">
                    {s.count}
                  </span>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

function StatCard({
  icon: Icon,
  label,
  value,
  sub,
  tone,
  compact,
}: {
  icon: React.ElementType;
  label: string;
  value: string;
  sub?: string;
  tone?: "positive" | "negative";
  compact?: boolean;
}) {
  const toneClass =
    tone === "positive"
      ? "text-success"
      : tone === "negative"
        ? "text-destructive"
        : "text-foreground";
  return (
    <div className="rounded-2xl bg-card p-5 ring-1 ring-border/60">
      <div className="flex items-center justify-between">
        <span className="eyebrow">{label}</span>
        <Icon className="h-4 w-4 text-muted-foreground" />
      </div>
      <div
        className={cn(
          "mt-2 font-display font-semibold tracking-tight tabular-nums",
          compact ? "text-xl" : "text-3xl",
          toneClass,
        )}
      >
        {value}
      </div>
      {sub && (
        <div className="mt-1 text-xs text-muted-foreground">{sub}</div>
      )}
    </div>
  );
}

function BreakdownTable({
  rows,
  emptyLabel,
}: {
  rows: { label: string; calls: number; cost: number }[];
  emptyLabel: string;
}) {
  if (rows.length === 0) {
    return <p className="text-sm text-muted-foreground">{emptyLabel}</p>;
  }
  const max = Math.max(...rows.map((r) => r.cost)) || 1;
  return (
    <div className="space-y-3">
      {rows.map((r) => (
        <div key={r.label}>
          <div className="mb-1 flex items-baseline justify-between text-xs">
            <span>{r.label}</span>
            <span className="font-mono text-muted-foreground">
              {r.calls} · ${r.cost.toFixed(4)}
            </span>
          </div>
          <div className="h-1.5 overflow-hidden rounded-full bg-subtle">
            <div
              className="h-full rounded-full bg-primary/60"
              style={{ width: `${(r.cost / max) * 100}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}

function formatTokens(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
  return n.toString();
}

function formatRevenueBreakdown(
  by_type: Record<string, number>,
  t: ReturnType<typeof useTranslations>,
): string {
  const parts: string[] = [];
  if (by_type.subscription_refill !== undefined) {
    parts.push(
      t("revenue_subs", { amount: by_type.subscription_refill.toFixed(2) }),
    );
  }
  if (by_type.topup_purchase !== undefined) {
    parts.push(
      t("revenue_topups", { amount: by_type.topup_purchase.toFixed(2) }),
    );
  }
  return parts.join(" · ") || t("no_revenue");
}
