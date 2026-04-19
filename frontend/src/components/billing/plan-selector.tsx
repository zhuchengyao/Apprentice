"use client";

import { useTranslations } from "next-intl";
import { Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { SubscriptionPlan, UserSubscription } from "@/lib/types";

interface PlanSelectorProps {
  plans: SubscriptionPlan[];
  subscription: UserSubscription | null;
  onSelectPlan: (planId: string) => void;
  onManageBilling: () => void;
}

function featuresFor(
  planName: string,
  t: ReturnType<typeof useTranslations>,
): string[] {
  switch (planName) {
    case "free":
      return [
        t("feature_books", { count: 1 }),
        t("feature_models_basic"),
        t("feature_credits_monthly", { count: 500 }),
      ];
    case "basic":
      return [
        t("feature_books", { count: 5 }),
        t("feature_models_all"),
        t("feature_credits_monthly", { count: 15000 }),
      ];
    case "pro":
      return [
        t("feature_books_unlimited"),
        t("feature_models_all"),
        t("feature_credits_monthly", { count: 50000 }),
        t("feature_priority"),
      ];
    default:
      return [];
  }
}

export function PlanSelector({
  plans,
  subscription,
  onSelectPlan,
  onManageBilling,
}: PlanSelectorProps) {
  const t = useTranslations("billing.plan");
  const currentPlanName = subscription?.plan?.name || "free";
  const hasPaidSub = subscription?.status === "active" && currentPlanName !== "free";

  return (
    <div className="rounded-2xl bg-card p-6 ring-1 ring-border/60">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="eyebrow">{t("eyebrow")}</p>
          <h2 className="mt-1 font-display text-2xl font-semibold tracking-tight">
            {t("heading")}
          </h2>
        </div>
        {hasPaidSub && (
          <Button
            size="sm"
            variant="outline"
            onClick={onManageBilling}
            className="rounded-full"
          >
            {t("manage")}
          </Button>
        )}
      </div>

      {subscription?.cancel_at_period_end && (
        <p className="mt-4 rounded-xl bg-warning/8 px-3.5 py-2.5 text-[13px] leading-relaxed text-warning ring-1 ring-warning/20">
          {t("cancels_at", {
            date: new Date(
              subscription.current_period_end,
            ).toLocaleDateString(),
          })}
        </p>
      )}

      <div className="mt-6 grid gap-4 sm:grid-cols-3">
        {plans.map((plan) => {
          const isCurrent = plan.name === currentPlanName;
          const features = featuresFor(plan.name, t);

          return (
            <div
              key={plan.id}
              className={cn(
                "relative flex flex-col rounded-2xl p-5 transition",
                isCurrent
                  ? "bg-primary/5 ring-1 ring-primary/30"
                  : "bg-subtle ring-1 ring-border/60 hover:ring-border",
              )}
            >
              {isCurrent && (
                <span className="absolute -top-2.5 left-4 rounded-full bg-primary px-2.5 py-0.5 font-mono text-[10px] uppercase tracking-[0.1em] text-primary-foreground">
                  {t("current_plan")}
                </span>
              )}
              <h3 className="font-display text-lg font-semibold tracking-tight">
                {plan.display_name}
              </h3>
              <p className="mt-2 font-display text-3xl font-semibold leading-none tracking-tight tabular-nums">
                {plan.price_usd === 0
                  ? t("free")
                  : `$${plan.price_usd.toFixed(2)}`}
                {plan.price_usd > 0 && (
                  <span className="ml-1 font-sans text-sm font-normal text-muted-foreground">
                    {t("per_month")}
                  </span>
                )}
              </p>
              <ul className="mt-5 space-y-2 text-[13.5px] leading-relaxed text-muted-foreground">
                {features.map((f) => (
                  <li key={f} className="flex items-start gap-2">
                    <Check className="mt-0.5 h-3.5 w-3.5 flex-shrink-0 text-primary" />
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
              <div className="mt-auto pt-5">
                {!isCurrent && plan.price_usd > 0 && plan.stripe_price_id && (
                  <Button
                    size="sm"
                    variant="primary"
                    className="w-full rounded-full"
                    onClick={() => onSelectPlan(plan.id)}
                  >
                    {t("upgrade")}
                  </Button>
                )}
                {isCurrent && (
                  <Button
                    size="sm"
                    variant="outline"
                    className="w-full rounded-full"
                    disabled
                  >
                    {t("active")}
                  </Button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
