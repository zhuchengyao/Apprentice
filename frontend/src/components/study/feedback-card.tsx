"use client";

import { motion } from "framer-motion";
import { useTranslations } from "next-intl";
import { ArrowRight, Loader2, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

function encouragementKey(ratio: number): string {
  if (ratio >= 1) return "encouragement_perfect";
  if (ratio >= 0.75) return "encouragement_strong";
  if (ratio >= 0.4) return "encouragement_mixed";
  return "encouragement_struggle";
}

interface Props {
  correct: number;
  total: number;
  isLastScope: boolean;
  working: boolean;
  onAdvance: () => Promise<void> | void;
}

export function FeedbackCard({
  correct,
  total,
  isLastScope,
  working,
  onAdvance,
}: Props) {
  const t = useTranslations("study");
  const ratio = total > 0 ? correct / total : 0;
  const encouragement = t(encouragementKey(ratio));

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className={cn(
        "rounded-2xl border p-4 shadow-editorial-sm ring-1",
        ratio >= 0.75
          ? "border-emerald-500/40 bg-emerald-50/40 ring-emerald-500/10 dark:bg-emerald-500/5"
          : ratio >= 0.4
            ? "border-amber-400/40 bg-amber-50/40 ring-amber-400/10 dark:bg-amber-400/5"
            : "border-sky-500/40 bg-sky-50/40 ring-sky-500/10 dark:bg-sky-500/5",
      )}
    >
      <div className="flex items-start gap-3">
        <motion.div
          initial={{ rotate: -20, scale: 0.7 }}
          animate={{ rotate: 0, scale: 1 }}
          transition={{ type: "spring", stiffness: 300, damping: 18 }}
          className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary/15 text-primary ring-1 ring-primary/25"
        >
          <Sparkles className="h-4 w-4" />
        </motion.div>
        <div className="min-w-0 flex-1">
          <div className="font-mono text-[9.5px] uppercase tracking-[0.1em] text-muted-foreground">
            {t("phase.feedback")}
          </div>
          <h3 className="mt-0.5 font-heading text-[14px] font-semibold tracking-tight">
            {t("scope_recap")}
          </h3>
        </div>
      </div>

      <div className="mt-3 flex items-baseline gap-3">
        <motion.div
          initial={{ scale: 0.7 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 260, damping: 18 }}
          className="font-heading text-[28px] font-semibold tabular-nums leading-none tracking-tight"
        >
          {correct}
          <span className="text-muted-foreground">/{total}</span>
        </motion.div>
        <div className="min-w-0 flex-1">
          <div className="h-1.5 overflow-hidden rounded-full bg-subtle ring-1 ring-inset ring-border/50">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${Math.round(ratio * 100)}%` }}
              transition={{ duration: 0.5, ease: "easeOut" }}
              className={cn(
                "h-full rounded-full",
                ratio >= 0.75
                  ? "bg-emerald-500"
                  : ratio >= 0.4
                    ? "bg-amber-400"
                    : "bg-sky-500",
              )}
            />
          </div>
          <p className="mt-1.5 font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground tabular-nums">
            {t("scope_score", { correct, total })}
          </p>
        </div>
      </div>

      <p className="mt-3 rounded-xl bg-background/50 px-3 py-2 text-[12.5px] leading-relaxed text-foreground/90 ring-1 ring-border/50">
        {encouragement}
      </p>

      <div className="mt-3 flex justify-end">
        <Button
          size="sm"
          variant="primary"
          className="h-8 gap-1.5 rounded-full px-3 text-[12px]"
          disabled={working}
          onClick={() => onAdvance()}
        >
          {working ? (
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
          ) : (
            <>
              {isLastScope ? t("finish_session_cta") : t("next_scope_cta")}
              <ArrowRight className="h-3.5 w-3.5" />
            </>
          )}
        </Button>
      </div>
    </motion.div>
  );
}
