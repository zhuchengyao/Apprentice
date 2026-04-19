"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { useTranslations } from "next-intl";
import { CreditBalanceCard } from "@/components/billing/credit-balance-card";
import { PlanSelector } from "@/components/billing/plan-selector";
import { TransactionHistory } from "@/components/billing/transaction-history";
import { UsageChart } from "@/components/billing/usage-chart";
import { CreditPurchaseDialog } from "@/components/billing/credit-purchase-dialog";
import { useBillingStore } from "@/stores/billing-store";
import { api } from "@/lib/api-client";

export default function BillingPage() {
  return (
    <Suspense fallback={null}>
      <BillingPageInner />
    </Suspense>
  );
}

function BillingPageInner() {
  const searchParams = useSearchParams();
  const t = useTranslations("billing");
  const tPurchase = useTranslations("billing.purchase");
  const {
    balance,
    transactions,
    subscription,
    plans,
    isLoading,
    hasFetched,
    fetchAll,
  } = useBillingStore();

  const [showPurchase, setShowPurchase] = useState(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  useEffect(() => {
    fetchAll();
  }, [fetchAll]);

  useEffect(() => {
    const success = searchParams.get("success");
    if (success === "credits") {
      setSuccessMsg(t("success_credits"));
      useBillingStore.getState().fetchBalance();
    } else if (success === "subscription") {
      setSuccessMsg(t("success_subscription"));
      useBillingStore.getState().fetchAll();
    }
  }, [searchParams, t]);

  async function handleSelectPlan(planId: string) {
    try {
      const data = await api.post<{ checkout_url: string }>(
        "/billing/subscription/checkout",
        { plan_id: planId },
      );
      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      }
    } catch {
      alert(tPurchase("checkout_failed"));
    }
  }

  async function handleManageBilling() {
    try {
      const data = await api.post<{ portal_url: string }>(
        "/billing/subscription/portal",
        {},
      );
      if (data.portal_url) {
        window.location.href = data.portal_url;
      }
    } catch {
      alert(tPurchase("portal_failed"));
    }
  }

  const showSkeleton = !hasFetched && isLoading;

  return (
    <div className="mx-auto w-full max-w-4xl px-5 py-10 sm:px-8 sm:py-12">
      <div>
        <p className="eyebrow">{t("eyebrow")}</p>
        <h1 className="mt-3 font-display text-4xl font-semibold tracking-tight sm:text-5xl">
          {t("heading")}
        </h1>
        <p className="mt-3 max-w-xl text-[14.5px] leading-relaxed text-muted-foreground">
          {t("lede")}
        </p>
      </div>

      {successMsg && (
        <div className="mt-6 rounded-2xl bg-primary/8 px-4 py-3 text-[13.5px] text-primary ring-1 ring-primary/20">
          {successMsg}
        </div>
      )}

      <div className="mt-10 space-y-5">
        {showSkeleton ? (
          [...Array(3)].map((_, i) => (
            <div
              key={i}
              className="h-40 overflow-hidden rounded-2xl ring-1 ring-border/60"
            >
              <div className="shimmer h-full w-full" />
            </div>
          ))
        ) : (
          <>
            <CreditBalanceCard
              balance={balance}
              onBuyCredits={() => setShowPurchase(true)}
            />
            <PlanSelector
              plans={plans}
              subscription={subscription}
              onSelectPlan={handleSelectPlan}
              onManageBilling={handleManageBilling}
            />
            <UsageChart />
            <TransactionHistory transactions={transactions} />
          </>
        )}
      </div>

      <CreditPurchaseDialog
        open={showPurchase}
        onClose={() => setShowPurchase(false)}
      />
    </div>
  );
}
