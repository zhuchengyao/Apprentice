"use client";

import { motion } from "framer-motion";
import { ChevronDown } from "lucide-react";
import { useTranslations } from "next-intl";
import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

export type PhaseState = "active" | "done" | "pending";
export type PhaseKey = "read" | "explain" | "practice" | "feedback";

const PHASE_INDEX: Record<PhaseKey, number> = {
  read: 1,
  explain: 2,
  practice: 3,
  feedback: 4,
};

interface Props {
  phase: PhaseKey;
  state: PhaseState;
  children?: ReactNode;
  meta?: string;
  compactSummary?: string;
  onExpand?: () => void;
  accent?: "primary" | "success";
}

export function PhaseShell({
  phase,
  state,
  children,
  meta,
  compactSummary,
  onExpand,
  accent = "primary",
}: Props) {
  const t = useTranslations("study");
  const label = t(`phase.${phase}`);
  const idx = PHASE_INDEX[phase];

  if (state === "pending") {
    return (
      <div className="flex items-center gap-3 px-1 py-2.5 text-muted-foreground/75">
        <div className="flex h-[22px] w-[22px] shrink-0 items-center justify-center rounded-full border border-dashed border-border/70 bg-subtle/50">
          <span className="font-mono text-[9.5px] tabular-nums text-muted-foreground/70">
            {idx}
          </span>
        </div>
        <span className="shrink-0 font-mono text-[10.5px] font-medium uppercase tracking-[0.1em]">
          {label}
        </span>
        <span className="h-px flex-1 bg-border/50" />
        <span className="font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground/70">
          {t("phase_waiting")}
        </span>
      </div>
    );
  }

  if (state === "done") {
    return (
      <button
        type="button"
        onClick={onExpand}
        className={cn(
          "group flex w-full items-center gap-3 rounded-xl border px-3 py-2.5 text-left transition-colors",
          "border-emerald-500/20 bg-emerald-500/5 hover:bg-emerald-500/10",
          "dark:border-emerald-500/25 dark:bg-emerald-500/[0.06]",
        )}
      >
        <div className="flex h-[22px] w-[22px] shrink-0 items-center justify-center rounded-full border border-emerald-500/30 bg-emerald-500/15 text-emerald-600 dark:text-emerald-400">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.25"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="h-2.5 w-2.5"
            aria-hidden
          >
            <path d="M20 6 9 17l-5-5" />
          </svg>
        </div>
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2">
            <span className="font-mono text-[10.5px] font-medium uppercase tracking-[0.1em] text-emerald-600 dark:text-emerald-400">
              {label}
            </span>
            {meta && (
              <span className="font-mono text-[10px] tabular-nums text-muted-foreground">
                · {meta}
              </span>
            )}
          </div>
          {compactSummary && (
            <div className="mt-0.5 truncate text-[12px] leading-snug text-subtle-foreground/90">
              {compactSummary}
            </div>
          )}
        </div>
        <ChevronDown className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
      </button>
    );
  }

  const accentClasses =
    accent === "success"
      ? {
          ring: "border-emerald-500/25 shadow-editorial",
          header: "bg-emerald-500/5 border-emerald-500/15",
          pill: "bg-emerald-500/15 text-emerald-600 ring-emerald-500/30 dark:text-emerald-400",
          labelColor: "text-emerald-600 dark:text-emerald-400",
        }
      : {
          ring: "border-primary/25 shadow-editorial",
          header: "bg-primary/5 border-primary/15",
          pill: "bg-primary/15 text-primary ring-primary/30",
          labelColor: "text-primary",
        };

  return (
    <motion.section
      layout
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className={cn(
        "overflow-hidden rounded-2xl border bg-card",
        accentClasses.ring,
      )}
    >
      <header
        className={cn(
          "flex items-center gap-2.5 border-b px-3.5 py-2.5",
          accentClasses.header,
        )}
      >
        <div
          className={cn(
            "flex h-[22px] w-[22px] shrink-0 items-center justify-center rounded-full ring-1",
            accentClasses.pill,
          )}
        >
          <span className="font-mono text-[10px] font-semibold tabular-nums">
            {idx}
          </span>
        </div>
        <span
          className={cn(
            "font-mono text-[10.5px] font-semibold uppercase tracking-[0.1em]",
            accentClasses.labelColor,
          )}
        >
          {label}
        </span>
        {meta && (
          <span className="ml-auto font-mono text-[10px] tracking-[0.06em] text-muted-foreground">
            {meta}
          </span>
        )}
      </header>
      <div className="p-3.5">{children}</div>
    </motion.section>
  );
}
