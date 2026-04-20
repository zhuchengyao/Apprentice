"use client";

import { useEffect } from "react";
import { useTranslations } from "next-intl";
import { ArrowRight, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Markdown } from "@/components/ui/markdown";
import type {
  HighlightController,
  HighlightVariant,
} from "@/components/tutor/use-tutor-highlight";
import type { KPHighlight } from "@/components/tutor/tutor-popover";
import type { ScopeView } from "@/lib/types";
import { PhaseShell, type PhaseState } from "./phase-shell";

interface Props {
  scope: ScopeView;
  highlight: HighlightController;
  onFinishReading: () => Promise<void> | void;
  working: boolean;
  state: PhaseState;
  onExpand?: () => void;
}

const SCOPE_VARIANT: HighlightVariant = "scope";

export function ReadingScopePanel({
  scope,
  highlight,
  onFinishReading,
  working,
  state,
  onExpand,
}: Props) {
  const t = useTranslations("study");

  // Only paint highlights while this phase is actually active — a collapsed
  // "done" row shouldn't re-decorate the book page.
  useEffect(() => {
    if (state !== "active") return;
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
  }, [
    state,
    highlight,
    scope.anchor_hint,
    scope.index,
    scope.kp_ids,
    scope.source_anchors,
    scope.title,
  ]);

  if (state === "pending") {
    return <PhaseShell phase="read" state="pending" />;
  }

  if (state === "done") {
    return (
      <PhaseShell
        phase="read"
        state="done"
        meta={t("read_meta")}
        compactSummary={scope.title}
        onExpand={onExpand}
      />
    );
  }

  return (
    <PhaseShell phase="read" state="active" meta={t("read_meta")}>
      <div className="flex flex-col gap-3.5">
        <h3 className="font-heading text-[16px] font-semibold leading-tight tracking-tight">
          {scope.title ? (
            <Markdown inline>{scope.title}</Markdown>
          ) : (
            t("scope_default_title")
          )}
        </h3>

        {scope.anchor_hint && (
          <div className="relative rounded-xl bg-primary/5 py-3 pl-4 pr-3.5">
            <div className="absolute inset-y-2.5 left-0 w-[2px] rounded-full bg-primary" />
            <p className="font-heading text-[13px] italic leading-snug text-subtle-foreground">
              <Markdown inline>{scope.anchor_hint}</Markdown>
            </p>
            <div className="mt-2 flex items-center gap-1.5 text-[11px] text-muted-foreground">
              <ArrowRight className="h-3 w-3" />
              <span className="font-mono tracking-[0.05em]">
                {t("scope_kp_count", { count: scope.kp_ids.length })}
              </span>
            </div>
          </div>
        )}

        <div className="flex items-center gap-2 text-[11.5px] text-muted-foreground">
          <span
            aria-hidden
            className="inline-block h-[6px] w-[6px] flex-shrink-0 animate-pulse rounded-full bg-primary"
          />
          <span>{t("passage_in_book")}</span>
        </div>

        <div className="flex items-center justify-between gap-2">
          <span className="font-mono text-[10px] uppercase tracking-[0.08em] tabular-nums text-muted-foreground">
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
      </div>
    </PhaseShell>
  );
}
