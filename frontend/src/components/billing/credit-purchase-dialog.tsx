"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import { Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api-client";
import { cn } from "@/lib/utils";

interface CreditPurchaseDialogProps {
  open: boolean;
  onClose: () => void;
}

const PACKS = [
  { key: "5000", credits: 5000, price: 5.0 },
  { key: "20000", credits: 20000, price: 18.0, popular: true },
  { key: "50000", credits: 50000, price: 40.0 },
];

export function CreditPurchaseDialog({
  open,
  onClose,
}: CreditPurchaseDialogProps) {
  const t = useTranslations("billing.purchase");
  const [selected, setSelected] = useState<string>("20000");
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  async function handlePurchase() {
    setLoading(true);
    try {
      const data = await api.post<{ checkout_url: string }>(
        "/billing/credits/checkout",
        { pack: selected },
      );
      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      }
    } catch {
      alert(t("checkout_failed"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="w-full max-w-md rounded-2xl bg-background p-6 ring-1 ring-border/60 shadow-editorial-lg">
        <p className="eyebrow">{t("title")}</p>
        <h2 className="mt-1 font-display text-2xl font-semibold tracking-tight">
          {t("title")}
        </h2>
        <p className="mt-2 text-[13.5px] leading-relaxed text-muted-foreground">
          {t("lede")}
        </p>

        <div className="mt-5 space-y-2.5">
          {PACKS.map((pack) => {
            const isSelected = selected === pack.key;
            return (
              <button
                key={pack.key}
                onClick={() => setSelected(pack.key)}
                className={cn(
                  "flex w-full items-center justify-between rounded-2xl p-4 text-left transition",
                  isSelected
                    ? "bg-primary/5 ring-1 ring-primary/30"
                    : "bg-subtle ring-1 ring-border/60 hover:ring-border",
                )}
              >
                <div className="flex items-center gap-2.5">
                  <span className="font-medium">
                    {t("pack_label", { count: pack.credits })}
                  </span>
                  {pack.popular && (
                    <span className="rounded-full bg-primary px-2 py-0.5 font-mono text-[10px] uppercase tracking-[0.1em] text-primary-foreground">
                      {t("popular")}
                    </span>
                  )}
                </div>
                <span className="font-display text-xl font-semibold tabular-nums">
                  ${pack.price.toFixed(2)}
                </span>
              </button>
            );
          })}
        </div>

        <div className="mt-6 flex gap-3">
          <Button
            variant="outline"
            className="flex-1 rounded-full"
            onClick={onClose}
          >
            {t("cancel")}
          </Button>
          <Button
            variant="primary"
            className="flex-1 gap-2 rounded-full"
            onClick={handlePurchase}
            disabled={loading}
          >
            {loading && <Loader2 className="h-4 w-4 animate-spin" />}
            {t("confirm")}
          </Button>
        </div>
      </div>
    </div>
  );
}
