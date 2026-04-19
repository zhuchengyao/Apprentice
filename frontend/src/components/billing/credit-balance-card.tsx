"use client";

import { useTranslations } from "next-intl";
import { Coins, ShoppingCart } from "lucide-react";
import { Button } from "@/components/ui/button";

interface CreditBalanceCardProps {
  balance: number | null;
  onBuyCredits: () => void;
}

export function CreditBalanceCard({
  balance,
  onBuyCredits,
}: CreditBalanceCardProps) {
  const t = useTranslations("billing.balance");
  return (
    <div className="rounded-2xl bg-card p-6 ring-1 ring-border/60">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary ring-1 ring-primary/20">
            <Coins className="h-5 w-5" />
          </div>
          <div>
            <p className="eyebrow">{t("eyebrow")}</p>
            <p className="mt-1 font-display text-3xl font-semibold leading-none tracking-tight tabular-nums">
              {balance !== null ? balance.toLocaleString() : "—"}
            </p>
          </div>
        </div>
        <Button
          variant="primary"
          onClick={onBuyCredits}
          className="gap-2 rounded-full"
        >
          <ShoppingCart className="h-4 w-4" />
          {t("buy_more")}
        </Button>
      </div>
      <p className="mt-4 text-[12.5px] leading-relaxed text-muted-foreground">
        {t("explainer")}
      </p>
    </div>
  );
}
