"use client";

import { useEffect } from "react";
import { motion } from "framer-motion";
import { useTranslations } from "next-intl";
import { ArrowRight, BookOpen, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Markdown } from "@/components/ui/markdown";
import type {
  HighlightController,
  HighlightVariant,
} from "@/components/tutor/use-tutor-highlight";
import type { KPHighlight } from "@/components/tutor/tutor-popover";
import type { ScopeView } from "@/lib/types";

interface Props {
  scope: ScopeView;
  highlight: HighlightController;
  onFinishReading: () => Promise<void> | void;
  working: boolean;
}

const SCOPE_VARIANT: HighlightVariant = "scope";

export function ReadingScopePanel({
  scope,
  highlight,
  onFinishReading,
  working,
}: Props) {
  const t = useTranslations("study");

  useEffect(() => {
    const kps: KPHighlight[] = scope.source_anchors.map((anchor, i) => ({
      id: scope.kp_ids[i] ?? `${scope.index}-${i}`,
      concept: scope.title,
      section_id: "",
      explanation: "",
      source_anchor: anchor,
    }));
    highlight.applyHighlight(kps, SCOPE_VARIANT);
    return () => {
      highlight.clearVariant(SCOPE_VARIANT);
    };
  }, [highlight, scope.anchor_hint, scope.index, scope.kp_ids, scope.source_anchors, scope.title]);

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -8 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className="rounded-2xl border border-border/70 bg-card/60 p-4 shadow-editorial-sm ring-1 ring-foreground/5"
    >
      <div className="flex items-start gap-3">
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary/12 text-primary ring-1 ring-primary/20">
          <BookOpen className="h-4 w-4" />
        </div>
        <div className="min-w-0 flex-1">
          <div className="font-mono text-[9.5px] uppercase tracking-[0.1em] text-muted-foreground">
            {t("phase.read")}
          </div>
          <h3 className="mt-0.5 font-heading text-[14px] font-semibold tracking-tight">
            {scope.title ? (
              <Markdown inline>{scope.title}</Markdown>
            ) : (
              t("scope_default_title")
            )}
          </h3>
          {scope.anchor_hint && (
            <p className="mt-1 text-[12.5px] leading-relaxed text-muted-foreground">
              <Markdown inline>{scope.anchor_hint}</Markdown>
            </p>
          )}
        </div>
      </div>

      <p className="mt-3 rounded-xl bg-primary/5 px-3 py-2 text-[12px] leading-relaxed text-muted-foreground ring-1 ring-primary/10">
        {t("read_instruction")}
      </p>

      <div className="mt-3 flex items-center justify-between gap-2">
        <span className="font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground tabular-nums">
          {t("scope_kp_count", { count: scope.kp_ids.length })}
        </span>
        <Button
          size="sm"
          variant="primary"
          className="h-8 gap-1.5 rounded-full px-3 text-[12px]"
          onClick={() => onFinishReading()}
          disabled={working}
        >
          {working ? (
            <>
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
              {t("preparing_explanation")}
            </>
          ) : (
            <>
              {t("read_cta")}
              <ArrowRight className="h-3.5 w-3.5" />
            </>
          )}
        </Button>
      </div>
    </motion.div>
  );
}
