"use client";

import { motion } from "framer-motion";
import { useTranslations } from "next-intl";
import { Check, Lock } from "lucide-react";
import type { ScopeSummary } from "@/lib/types";
import { cn } from "@/lib/utils";

interface Props {
  scopes: ScopeSummary[];
  currentScopeIndex: number;
  maxScopeReached: number;
  working: boolean;
  onSelect: (scopeIndex: number) => void | Promise<void>;
}

/**
 * Horizontal strip of scope pills. Past and reached scopes are clickable —
 * selecting one drops the session into the target scope's feedback view so
 * the learner can review read/explain/practice via the phase stepper.
 */
export function ScopeSelector({
  scopes,
  currentScopeIndex,
  maxScopeReached,
  working,
  onSelect,
}: Props) {
  const t = useTranslations("study");
  if (scopes.length <= 1) return null;

  return (
    <div className="flex min-w-0 items-center gap-2">
      <div className="shrink-0 whitespace-nowrap font-mono text-[9.5px] uppercase tracking-[0.1em] text-muted-foreground">
        {t.has("scope_selector_label") ? t("scope_selector_label") : "Scopes"}
      </div>
      <div className="flex min-w-0 flex-1 items-center gap-1.5 overflow-x-auto py-0.5">
        {scopes.map((scope) => {
          const isCurrent = scope.index === currentScopeIndex;
          const reached = scope.index <= maxScopeReached;
          const clickable = reached && !isCurrent && !working;
          return (
            <motion.button
              key={scope.index}
              type="button"
              disabled={!clickable}
              onClick={clickable ? () => onSelect(scope.index) : undefined}
              title={scope.title}
              aria-label={scope.title}
              initial={false}
              animate={{ scale: isCurrent ? 1.04 : 1 }}
              transition={{ type: "spring", stiffness: 300, damping: 22 }}
              className={cn(
                "flex shrink-0 items-center gap-1 whitespace-nowrap rounded-full border px-2.5 py-1 font-mono text-[10px] uppercase tracking-[0.06em] tabular-nums transition-colors",
                isCurrent &&
                  "border-primary/40 bg-primary/12 text-primary ring-1 ring-primary/20",
                !isCurrent &&
                  reached &&
                  "border-emerald-500/30 bg-emerald-500/10 text-emerald-700 hover:bg-emerald-500/20 dark:text-emerald-300",
                !reached &&
                  "border-border/60 bg-subtle/60 text-muted-foreground",
                clickable ? "cursor-pointer" : "cursor-default",
              )}
            >
              <span>{scope.index + 1}</span>
              {!isCurrent && reached && <Check className="h-3 w-3" />}
              {!reached && <Lock className="h-2.5 w-2.5" />}
            </motion.button>
          );
        })}
      </div>
    </div>
  );
}
