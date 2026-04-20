"use client";

import { motion } from "framer-motion";
import { useTranslations } from "next-intl";
import { ArrowRight, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { PhaseShell, type PhaseState } from "./phase-shell";

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
  state: PhaseState;
  onExpand?: () => void;
}

function MasteryDial({ score }: { score: number }) {
  const size = 64;
  const r = 26;
  const c = 2 * Math.PI * r;
  const offset = c * (1 - score / 100);
  return (
    <div className="relative h-16 w-16 shrink-0">
      <svg
        viewBox="0 0 64 64"
        width={size}
        height={size}
        className="-rotate-90"
      >
        <circle
          cx={32}
          cy={32}
          r={r}
          fill="none"
          strokeWidth={5}
          className="stroke-emerald-500/20"
        />
        <motion.circle
          cx={32}
          cy={32}
          r={r}
          fill="none"
          strokeWidth={5}
          strokeLinecap="round"
          strokeDasharray={c}
          initial={{ strokeDashoffset: c }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1, ease: [0.22, 0.61, 0.36, 1] }}
          className="stroke-emerald-500"
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="font-heading text-[18px] font-semibold tabular-nums tracking-tight">
          {score}
          <span className="font-mono text-[9px] font-medium text-muted-foreground">
            %
          </span>
        </span>
      </div>
    </div>
  );
}

export function FeedbackCard({
  correct,
  total,
  isLastScope,
  working,
  onAdvance,
  state,
  onExpand,
}: Props) {
  const t = useTranslations("study");
  const ratio = total > 0 ? correct / total : 0;
  const score = Math.round(ratio * 100);
  const encouragement = t(encouragementKey(ratio));

  if (state === "pending") {
    return <PhaseShell phase="feedback" state="pending" />;
  }

  if (state === "done") {
    return (
      <PhaseShell
        phase="feedback"
        state="done"
        meta={`${correct} / ${total}`}
        compactSummary={encouragement}
        onExpand={onExpand}
      />
    );
  }

  const headline =
    ratio >= 0.75
      ? t("encouragement_strong").split("—")[0].trim() || t("scope_recap")
      : t("scope_recap");

  return (
    <PhaseShell
      phase="feedback"
      state="active"
      meta={t("scope_complete_meta")}
      accent="success"
    >
      <div className="flex flex-col gap-3.5">
        <div className="flex items-center gap-3.5">
          <MasteryDial score={score} />
          <div className="min-w-0 flex-1">
            <div className="font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground">
              {t("mastery")}
            </div>
            <div className="font-heading text-[22px] font-semibold leading-tight tracking-tight">
              {headline}
            </div>
            <div className="mt-1 text-[12.5px] leading-[1.45] text-subtle-foreground">
              {t("scope_score", { correct, total })}
            </div>
          </div>
        </div>

        <div className="flex flex-col gap-2">
          <div
            className={cn(
              "rounded-xl border px-3 py-2.5",
              "border-emerald-500/22 bg-emerald-500/6",
            )}
          >
            <div className="mb-0.5 font-mono text-[9.5px] font-semibold uppercase tracking-[0.1em] text-emerald-600 dark:text-emerald-400">
              ✓ {t("landed")}
            </div>
            <div className="text-[12.5px] leading-[1.5]">{encouragement}</div>
          </div>
          {ratio < 1 && total > 0 && (
            <div
              className={cn(
                "rounded-xl border px-3 py-2.5",
                "border-amber-400/25 bg-amber-400/6",
              )}
            >
              <div className="mb-0.5 font-mono text-[9.5px] font-semibold uppercase tracking-[0.1em] text-amber-600 dark:text-amber-400">
                ~ {t("revisit")}
              </div>
              <div className="text-[12.5px] leading-[1.5] text-subtle-foreground">
                {t("missed_it_reassure")}
              </div>
            </div>
          )}
        </div>

        <Button
          size="default"
          variant="primary"
          disabled={working}
          onClick={() => onAdvance()}
          className="h-9 w-full justify-center gap-1.5 rounded-full text-[12.5px]"
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
    </PhaseShell>
  );
}
