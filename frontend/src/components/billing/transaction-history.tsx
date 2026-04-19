"use client";

import { useTranslations } from "next-intl";
import type { CreditTransaction, TransactionType } from "@/lib/types";
import { cn } from "@/lib/utils";

const TYPE_KEYS: Record<TransactionType, string> = {
  signup_bonus: "type_signup_bonus",
  subscription_refill: "type_subscription_refill",
  topup_purchase: "type_topup_purchase",
  ai_usage: "type_ai_usage",
  admin_adjustment: "type_admin_adjustment",
};

interface TransactionHistoryProps {
  transactions: CreditTransaction[];
}

export function TransactionHistory({ transactions }: TransactionHistoryProps) {
  const t = useTranslations("billing.transactions");

  if (transactions.length === 0) {
    return (
      <div className="rounded-2xl bg-card p-6 ring-1 ring-border/60">
        <p className="eyebrow">{t("eyebrow")}</p>
        <h2 className="mt-1 font-display text-2xl font-semibold tracking-tight">
          {t("heading")}
        </h2>
        <p className="mt-5 text-[13.5px] text-muted-foreground">{t("empty")}</p>
      </div>
    );
  }

  return (
    <div className="rounded-2xl bg-card p-6 ring-1 ring-border/60">
      <p className="eyebrow">{t("eyebrow")}</p>
      <h2 className="mt-1 font-display text-2xl font-semibold tracking-tight">
        {t("heading")}
      </h2>
      <div className="mt-5 overflow-x-auto">
        <table className="w-full text-[13.5px]">
          <thead>
            <tr className="border-b border-border/60 text-left">
              <th className="pb-2 pr-4 font-mono text-[10px] font-normal uppercase tracking-[0.1em] text-muted-foreground">
                {t("col_date")}
              </th>
              <th className="pb-2 pr-4 font-mono text-[10px] font-normal uppercase tracking-[0.1em] text-muted-foreground">
                {t("col_type")}
              </th>
              <th className="pb-2 pr-4 font-mono text-[10px] font-normal uppercase tracking-[0.1em] text-muted-foreground">
                {t("col_description")}
              </th>
              <th className="pb-2 pr-4 text-right font-mono text-[10px] font-normal uppercase tracking-[0.1em] text-muted-foreground">
                {t("col_amount")}
              </th>
              <th className="pb-2 text-right font-mono text-[10px] font-normal uppercase tracking-[0.1em] text-muted-foreground">
                {t("col_balance")}
              </th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((tx) => {
              const typeKey = TYPE_KEYS[tx.transaction_type];
              return (
                <tr
                  key={tx.id}
                  className="border-b border-border/40 last:border-0"
                >
                  <td className="py-2.5 pr-4 tabular-nums text-muted-foreground">
                    {new Date(tx.created_at).toLocaleDateString()}
                  </td>
                  <td className="py-2.5 pr-4">
                    {typeKey ? t(typeKey as never) : tx.transaction_type}
                  </td>
                  <td className="py-2.5 pr-4 text-muted-foreground">
                    {tx.description || "—"}
                  </td>
                  <td
                    className={cn(
                      "py-2.5 pr-4 text-right font-medium tabular-nums",
                      tx.amount > 0 ? "text-success" : "text-destructive",
                    )}
                  >
                    {tx.amount > 0 ? "+" : ""}
                    {tx.amount.toLocaleString()}
                  </td>
                  <td className="py-2.5 text-right tabular-nums">
                    {tx.balance_after.toLocaleString()}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
