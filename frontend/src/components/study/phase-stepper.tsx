"use client";

import { motion } from "framer-motion";
import { useTranslations } from "next-intl";
import { BookOpen, CheckCircle2, Lightbulb, ListChecks, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";
import type { StudyPhase } from "@/lib/types";

const PHASES: Array<{ key: Exclude<StudyPhase, "done">; icon: typeof BookOpen }> = [
  { key: "read", icon: BookOpen },
  { key: "explain", icon: Lightbulb },
  { key: "practice", icon: ListChecks },
  { key: "feedback", icon: Sparkles },
];

function phaseIndex(phase: StudyPhase): number {
  switch (phase) {
    case "read": return 0;
    case "explain": return 1;
    case "practice": return 2;
    case "feedback": return 3;
    case "done": return 4;
  }
}

interface Props {
  phase: StudyPhase;
  scopeIndex: number;
  totalScopes: number;
  /** Called when the user clicks a step they've already passed. */
  onNavigate?: (phase: Exclude<StudyPhase, "done">) => void;
}

export function PhaseStepper({ phase, scopeIndex, totalScopes, onNavigate }: Props) {
  const t = useTranslations("study");
  const active = phaseIndex(phase);
  const done = phase === "done";

  return (
    <div className="flex items-center gap-3">
      <div className="shrink-0 whitespace-nowrap font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground tabular-nums">
        {totalScopes > 0
          ? t("scope_progress", {
              current: Math.min(scopeIndex + 1, totalScopes),
              total: totalScopes,
            })
          : null}
      </div>
      <div className="flex flex-1 items-center">
        {PHASES.map((p, i) => {
          const Icon = p.icon;
          const state: "pending" | "current" | "passed" =
            done || i < active
              ? "passed"
              : i === active
                ? "current"
                : "pending";
          const navigable = state === "passed" && !!onNavigate;
          const handleClick = navigable ? () => onNavigate(p.key) : undefined;
          return (
            <div key={p.key} className="flex flex-1 items-center last:flex-none">
              <motion.button
                type="button"
                onClick={handleClick}
                disabled={!navigable}
                aria-label={navigable ? t(`phase.${p.key}`) : undefined}
                initial={false}
                animate={{
                  scale: state === "current" ? 1.06 : 1,
                  backgroundColor:
                    state === "current"
                      ? "var(--color-primary)"
                      : state === "passed"
                        ? "rgb(34 197 94 / 0.15)"
                        : "var(--color-subtle)",
                }}
                transition={{ type: "spring", stiffness: 280, damping: 22 }}
                className={cn(
                  "relative flex h-8 w-8 shrink-0 items-center justify-center rounded-full ring-1",
                  state === "current"
                    ? "ring-primary/30 text-primary-foreground shadow-editorial-sm"
                    : state === "passed"
                      ? "ring-emerald-500/20 text-emerald-600 dark:text-emerald-400"
                      : "ring-border/60 text-muted-foreground",
                  navigable
                    ? "cursor-pointer hover:ring-emerald-500/40 hover:bg-emerald-500/20"
                    : "cursor-default",
                )}
              >
                {state === "passed" ? (
                  <CheckCircle2 className="h-4 w-4" />
                ) : (
                  <Icon className="h-3.5 w-3.5" />
                )}
              </motion.button>
              <div className="mx-2 hidden flex-col sm:flex">
                <span
                  className={cn(
                    "whitespace-nowrap font-mono text-[9.5px] uppercase tracking-[0.08em]",
                    state === "current"
                      ? "text-foreground"
                      : "text-muted-foreground",
                  )}
                >
                  {t(`phase.${p.key}`)}
                </span>
              </div>
              {i < PHASES.length - 1 && (
                <div className="relative mx-1 h-px flex-1 overflow-hidden bg-border/60">
                  <motion.div
                    initial={false}
                    animate={{
                      width: state === "passed" ? "100%" : "0%",
                    }}
                    transition={{ duration: 0.35, ease: "easeOut" }}
                    className="absolute inset-y-0 left-0 bg-emerald-500/40"
                  />
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
