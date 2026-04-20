"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import type { ScopeSummary } from "@/lib/types";
import { cn } from "@/lib/utils";

interface Props {
  scopes: ScopeSummary[];
  currentScopeIndex: number;
  maxScopeReached: number;
  working: boolean;
  onSelect: (scopeIndex: number) => void | Promise<void>;
}

export function ScopeSelector({
  scopes,
  currentScopeIndex,
  maxScopeReached,
  working,
  onSelect,
}: Props) {
  const t = useTranslations("study");
  const [hoverIdx, setHoverIdx] = useState<number | null>(null);

  if (scopes.length <= 1) return null;

  const shownIdx = hoverIdx !== null ? hoverIdx : currentScopeIndex;
  const shownScope = scopes[shownIdx];
  const total = scopes.length;
  const hoverIsPast =
    hoverIdx !== null && hoverIdx !== currentScopeIndex && hoverIdx <= maxScopeReached;
  const hoverIsLocked =
    hoverIdx !== null && hoverIdx !== currentScopeIndex && hoverIdx > maxScopeReached;

  return (
    <div className="flex min-w-0 flex-col gap-2">
      <div
        role="group"
        aria-label={t("scope_selector_label")}
        onMouseLeave={() => setHoverIdx(null)}
        className="flex h-5 items-stretch gap-[2px] rounded-lg border border-border/50 bg-subtle/60 p-[2px]"
      >
        {scopes.map((scope, i) => {
          const isCurrent = i === currentScopeIndex;
          const isPast = i < currentScopeIndex;
          const reached = i <= maxScopeReached;
          const isLocked = i > maxScopeReached;
          const canClick = reached && !isCurrent && !working;
          const isHover = i === hoverIdx;

          return (
            <button
              key={scope.index}
              type="button"
              disabled={!canClick}
              onClick={canClick ? () => onSelect(i) : undefined}
              onMouseEnter={() => setHoverIdx(i)}
              onFocus={() => setHoverIdx(i)}
              onBlur={() => setHoverIdx(null)}
              aria-current={isCurrent ? "step" : undefined}
              aria-label={`${t("scope_progress", {
                current: i + 1,
                total,
              })}: ${scope.title}`}
              className={cn(
                "min-w-0 flex-1 rounded transition-all duration-150",
                canClick ? "cursor-pointer" : "cursor-default",
                isHover && canClick ? "scale-y-[1.15]" : "scale-y-100",
                isCurrent &&
                  "bg-primary ring-1 ring-inset ring-primary/50",
                !isCurrent && isPast && "bg-emerald-500/70",
                !isCurrent &&
                  !isPast &&
                  reached &&
                  "bg-emerald-500/40 hover:bg-emerald-500/60",
                isLocked && "bg-transparent",
                isHover && isLocked && "bg-muted-foreground/20",
                isHover && isPast && "!bg-emerald-500",
              )}
            />
          );
        })}
      </div>

      <div className="flex min-h-[34px] items-start gap-2.5">
        <span className="shrink-0 pt-[1px] font-mono text-[10.5px] uppercase tracking-[0.08em] tabular-nums text-muted-foreground">
          {String(shownIdx + 1).padStart(2, "0")}
          <span className="opacity-50"> / {String(total).padStart(2, "0")}</span>
        </span>
        <div
          title={shownScope.title}
          className={cn(
            "line-clamp-2 min-w-0 flex-1 font-heading text-[13.5px] font-semibold leading-[1.3] tracking-tight",
            hoverIsLocked ? "text-muted-foreground" : "text-foreground",
          )}
        >
          {shownScope.title}
        </div>
        {(hoverIsPast || hoverIsLocked) && (
          <span
            className={cn(
              "shrink-0 whitespace-nowrap pt-[2px] font-mono text-[9.5px] uppercase tracking-[0.08em]",
              hoverIsPast
                ? "text-emerald-600 dark:text-emerald-400"
                : "text-muted-foreground",
            )}
          >
            {hoverIsPast ? t("scope_jump_back") : t("scope_locked")}
          </span>
        )}
      </div>
    </div>
  );
}
