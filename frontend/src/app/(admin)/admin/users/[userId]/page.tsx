"use client";

import { useEffect, useState, useCallback, use } from "react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import {
  ArrowLeft,
  Loader2,
  Shield,
  BookOpen,
  MessageSquare,
  Activity,
  AlertCircle,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

type UserDetail = {
  user: {
    id: string;
    email: string;
    name: string;
    role: string;
    is_active: boolean;
    auth_provider: string;
    avatar_url: string | null;
    created_at: string | null;
  };
  balance: number;
  subscription: {
    id: string;
    status: string;
    current_period_end: string;
    cancel_at_period_end: boolean;
    plan: {
      name: string;
      display_name: string;
      monthly_credits: number;
      price_usd: number;
    };
  } | null;
  stats: {
    book_count: number;
    conversation_count: number;
    lifetime_ai_calls: number;
    lifetime_cost_usd: number;
  };
  recent_transactions: {
    id: string;
    amount: number;
    balance_after: number;
    transaction_type: string;
    description: string | null;
    created_at: string;
  }[];
};

export default function AdminUserDetailPage({
  params,
}: {
  params: Promise<{ userId: string }>;
}) {
  const { userId } = use(params);
  const t = useTranslations("admin.users");
  const tCommon = useTranslations("admin");
  const [data, setData] = useState<UserDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [actionMessage, setActionMessage] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/admin/users/${userId}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const d = await res.json();
      setData(d);
    } catch (err) {
      setError(err instanceof Error ? err.message : tCommon("failed_load"));
    } finally {
      setLoading(false);
    }
  }, [userId, tCommon]);

  useEffect(() => {
    load();
  }, [load]);

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
          {error || tCommon("not_found")}
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-5xl space-y-6 p-8">
      <div>
        <Link
          href="/admin/users"
          className="inline-flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground transition-colors hover:text-foreground"
        >
          <ArrowLeft className="h-3.5 w-3.5" />
          {t("back")}
        </Link>
      </div>

      <header className="rounded-2xl bg-card p-6 ring-1 ring-border/60">
        <div className="flex items-start justify-between">
          <div className="flex items-start gap-4">
            {data.user.avatar_url ? (
              <img
                src={data.user.avatar_url}
                alt={data.user.name}
                className="h-14 w-14 rounded-full"
              />
            ) : (
              <div className="flex h-14 w-14 items-center justify-center rounded-full bg-primary/10 font-display text-xl text-primary ring-1 ring-primary/20">
                {data.user.name.charAt(0).toUpperCase()}
              </div>
            )}
            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-display text-2xl font-semibold tracking-tight">
                  {data.user.name}
                </h1>
                {data.user.role === "admin" && (
                  <span className="flex items-center gap-1 rounded-full bg-primary/10 px-2.5 py-0.5 font-mono text-[10px] uppercase tracking-[0.08em] text-primary ring-1 ring-primary/20">
                    <Shield className="h-3 w-3" />
                    {t("admin_badge")}
                  </span>
                )}
                {!data.user.is_active && (
                  <span className="rounded-full bg-destructive/10 px-2.5 py-0.5 font-mono text-[10px] uppercase tracking-[0.08em] text-destructive ring-1 ring-destructive/20">
                    {t("disabled_badge")}
                  </span>
                )}
              </div>
              <p className="text-sm text-muted-foreground">
                {data.user.email}
              </p>
              <p className="mt-1 font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground">
                {data.user.auth_provider}
                {data.user.created_at && (
                  <>
                    {" · "}
                    {t("joined_on", {
                      date: new Date(data.user.created_at).toLocaleDateString(),
                    })}
                  </>
                )}
              </p>
            </div>
          </div>
          <div className="text-right">
            <div className="eyebrow">{t("balance_eyebrow")}</div>
            <div className="mt-1 font-display text-3xl font-semibold tracking-tight tabular-nums">
              {data.balance.toLocaleString()}
            </div>
            <div className="font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground">
              {t("credits_unit")}
            </div>
          </div>
        </div>
      </header>

      {actionError && (
        <div className="flex items-center gap-2 rounded-xl bg-destructive/8 px-4 py-3 text-sm text-destructive ring-1 ring-destructive/20">
          <AlertCircle className="h-4 w-4" />
          {actionError}
        </div>
      )}
      {actionMessage && (
        <div className="rounded-xl bg-primary/8 px-4 py-3 text-sm text-primary ring-1 ring-primary/20">
          {actionMessage}
        </div>
      )}

      <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <StatBox
          icon={BookOpen}
          label={t("stat_books")}
          value={data.stats.book_count.toString()}
        />
        <StatBox
          icon={MessageSquare}
          label={t("stat_conversations")}
          value={data.stats.conversation_count.toString()}
        />
        <StatBox
          icon={Activity}
          label={t("stat_ai_calls")}
          value={data.stats.lifetime_ai_calls.toLocaleString()}
        />
        <StatBox
          icon={Activity}
          label={t("stat_lifetime_cost")}
          value={`$${data.stats.lifetime_cost_usd.toFixed(4)}`}
        />
      </div>

      <section className="rounded-2xl bg-card p-6 ring-1 ring-border/60">
        <h2 className="font-display text-xl font-semibold tracking-tight">
          {t("subscription_heading")}
        </h2>
        {data.subscription ? (
          <div className="mt-3">
            <div className="text-sm">
              {data.subscription.plan.display_name}
              <span className="ml-2 text-xs text-muted-foreground">
                {t("per_mo", {
                  price: data.subscription.plan.price_usd.toFixed(2),
                  credits:
                    data.subscription.plan.monthly_credits.toLocaleString(),
                })}
              </span>
            </div>
            <div className="mt-1 font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground">
              {t("sub_status", {
                status: data.subscription.status,
                date: new Date(
                  data.subscription.current_period_end,
                ).toLocaleDateString(),
              })}
              {data.subscription.cancel_at_period_end && t("sub_canceling")}
            </div>
          </div>
        ) : (
          <p className="mt-3 text-sm text-muted-foreground">
            {t("no_subscription")}
          </p>
        )}
      </section>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <CreditAdjustmentCard
          userId={userId}
          onSuccess={(msg) => {
            setActionError(null);
            setActionMessage(msg);
            load();
          }}
          onError={(msg) => {
            setActionMessage(null);
            setActionError(msg);
          }}
        />
        <ToggleActiveCard
          userId={userId}
          currentActive={data.user.is_active}
          onSuccess={(msg) => {
            setActionError(null);
            setActionMessage(msg);
            load();
          }}
          onError={(msg) => {
            setActionMessage(null);
            setActionError(msg);
          }}
        />
      </div>

      <section className="rounded-2xl bg-card p-6 ring-1 ring-border/60">
        <h2 className="font-display text-xl font-semibold tracking-tight">
          {t("recent_transactions")}
        </h2>
        {data.recent_transactions.length === 0 ? (
          <p className="mt-3 text-sm text-muted-foreground">
            {t("no_transactions")}
          </p>
        ) : (
          <table className="mt-4 w-full text-sm">
            <thead className="font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground">
              <tr>
                <th className="pb-2 text-left font-normal">{t("col_when")}</th>
                <th className="pb-2 text-left font-normal">{t("col_type")}</th>
                <th className="pb-2 text-left font-normal">
                  {t("col_description")}
                </th>
                <th className="pb-2 text-right font-normal">
                  {t("col_amount")}
                </th>
                <th className="pb-2 text-right font-normal">
                  {t("col_balance_after")}
                </th>
              </tr>
            </thead>
            <tbody>
              {data.recent_transactions.map((tx) => (
                <tr key={tx.id} className="border-t border-border/40">
                  <td className="py-2.5 text-xs text-muted-foreground">
                    {new Date(tx.created_at).toLocaleString()}
                  </td>
                  <td className="py-2.5 text-xs text-muted-foreground">
                    {tx.transaction_type}
                  </td>
                  <td className="max-w-xs truncate py-2.5 text-xs text-muted-foreground">
                    {tx.description || "—"}
                  </td>
                  <td
                    className={cn(
                      "py-2.5 text-right font-mono text-sm tabular-nums",
                      tx.amount >= 0 ? "text-success" : "text-destructive",
                    )}
                  >
                    {tx.amount >= 0 ? "+" : ""}
                    {tx.amount.toLocaleString()}
                  </td>
                  <td className="py-2.5 text-right font-mono text-sm tabular-nums text-muted-foreground">
                    {tx.balance_after.toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}

function StatBox({
  icon: Icon,
  label,
  value,
}: {
  icon: React.ElementType;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl bg-card p-4 ring-1 ring-border/60">
      <div className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground">
        <Icon className="h-3.5 w-3.5" />
        {label}
      </div>
      <div className="mt-1.5 font-display text-xl font-semibold tracking-tight tabular-nums">
        {value}
      </div>
    </div>
  );
}

function CreditAdjustmentCard({
  userId,
  onSuccess,
  onError,
}: {
  userId: string;
  onSuccess: (msg: string) => void;
  onError: (msg: string) => void;
}) {
  const t = useTranslations("admin.users");
  const [amount, setAmount] = useState("");
  const [reason, setReason] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    const n = parseInt(amount, 10);
    if (!Number.isFinite(n) || n === 0) {
      onError(t("amount_error"));
      return;
    }
    if (reason.trim().length < 3) {
      onError(t("reason_error"));
      return;
    }
    setSubmitting(true);
    try {
      const res = await fetch(`/api/admin/users/${userId}/credits`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ amount: n, reason: reason.trim() }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail || `HTTP ${res.status}`);
      }
      setAmount("");
      setReason("");
      onSuccess(
        t("adjust_success", { amount: n > 0 ? `+${n}` : `${n}` }),
      );
    } catch (err) {
      onError(err instanceof Error ? err.message : t("action_failed"));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form
      onSubmit={submit}
      className="space-y-3 rounded-2xl bg-card p-5 ring-1 ring-border/60"
    >
      <div>
        <h3 className="font-display text-lg font-semibold tracking-tight">
          {t("adjust_credits")}
        </h3>
        <p className="mt-1 text-xs text-muted-foreground">
          {t("adjust_credits_help")}
        </p>
      </div>
      <input
        type="number"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        placeholder={t("amount_placeholder")}
        className="w-full rounded-xl bg-background px-3.5 py-2.5 text-sm ring-1 ring-border/60 outline-none transition-colors focus:ring-2 focus:ring-primary/30"
      />
      <input
        type="text"
        value={reason}
        onChange={(e) => setReason(e.target.value)}
        placeholder={t("reason_placeholder")}
        className="w-full rounded-xl bg-background px-3.5 py-2.5 text-sm ring-1 ring-border/60 outline-none transition-colors focus:ring-2 focus:ring-primary/30"
      />
      <Button
        type="submit"
        variant="primary"
        disabled={submitting}
        className="w-full gap-2 rounded-full"
      >
        {submitting && <Loader2 className="h-4 w-4 animate-spin" />}
        {t("apply_adjustment")}
      </Button>
    </form>
  );
}

function ToggleActiveCard({
  userId,
  currentActive,
  onSuccess,
  onError,
}: {
  userId: string;
  currentActive: boolean;
  onSuccess: (msg: string) => void;
  onError: (msg: string) => void;
}) {
  const t = useTranslations("admin.users");
  const [reason, setReason] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const target = !currentActive;

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (reason.trim().length < 3) {
      onError(t("reason_error"));
      return;
    }
    setSubmitting(true);
    try {
      const res = await fetch(`/api/admin/users/${userId}/active`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ is_active: target, reason: reason.trim() }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail || `HTTP ${res.status}`);
      }
      setReason("");
      onSuccess(target ? t("enable_success") : t("disable_success"));
    } catch (err) {
      onError(err instanceof Error ? err.message : t("action_failed"));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form
      onSubmit={submit}
      className="space-y-3 rounded-2xl bg-card p-5 ring-1 ring-border/60"
    >
      <div>
        <h3 className="font-display text-lg font-semibold tracking-tight">
          {target ? t("enable_account") : t("disable_account")}
        </h3>
        <p className="mt-1 text-xs text-muted-foreground">
          {target ? t("enable_help") : t("disable_help")}
        </p>
      </div>
      <input
        type="text"
        value={reason}
        onChange={(e) => setReason(e.target.value)}
        placeholder={t("reason_placeholder")}
        className="w-full rounded-xl bg-background px-3.5 py-2.5 text-sm ring-1 ring-border/60 outline-none transition-colors focus:ring-2 focus:ring-primary/30"
      />
      <Button
        type="submit"
        disabled={submitting}
        className={cn(
          "w-full gap-2 rounded-full",
          target
            ? "bg-success text-white hover:bg-success/90"
            : "bg-destructive text-white hover:bg-destructive/90",
        )}
      >
        {submitting && <Loader2 className="h-4 w-4 animate-spin" />}
        {target ? t("enable_user") : t("disable_user")}
      </Button>
    </form>
  );
}
