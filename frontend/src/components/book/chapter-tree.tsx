"use client";

import { memo, useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { useTranslations } from "next-intl";
import {
  ArrowUpRight,
  BookOpen,
  CheckCircle,
  ChevronRight,
  Lightbulb,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { Chapter, Section } from "@/lib/types";

const difficultyKey: Record<number, string> = {
  1: "difficulty_basic",
  2: "difficulty_simple",
  3: "difficulty_moderate",
  4: "difficulty_complex",
  5: "difficulty_advanced",
};

const difficultyTone: Record<
  number,
  "success" | "primary" | "warning" | "destructive" | "mono"
> = {
  1: "success",
  2: "primary",
  3: "warning",
  4: "warning",
  5: "destructive",
};

const SectionItem = memo(function SectionItem({ section }: { section: Section }) {
  const [expanded, setExpanded] = useState(false);
  const t = useTranslations("book.tree");
  const kpCount = section.knowledge_points.length;

  return (
    <div className="ml-4 border-l border-border/60 pl-3">
      <button
        onClick={() => setExpanded(!expanded)}
        className="group flex w-full items-center gap-2 rounded-lg px-3 py-1.5 text-left transition-colors hover:bg-subtle/60"
      >
        <ChevronRight
          className={cn(
            "h-3 w-3 text-muted-foreground transition-transform",
            expanded && "rotate-90",
          )}
        />
        <BookOpen className="h-3.5 w-3.5 text-muted-foreground" />
        <span className="flex-1 truncate text-[13px] font-medium">
          {section.title}
        </span>
        <span className="font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground tabular-nums">
          {t("concept_count", { count: kpCount })}
          {section.progress > 0 && (
            <span className="ml-1 text-primary">
              · {Math.round(section.progress * 100)}%
            </span>
          )}
        </span>
      </button>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            {section.summary && (
              <p className="mx-3 mb-2 text-[12px] leading-relaxed text-muted-foreground">
                {section.summary}
              </p>
            )}
            <div className="space-y-1 pb-2">
              {section.knowledge_points.map((kp) => (
                <div
                  key={kp.id}
                  className="ml-2 flex items-start gap-2 rounded-md px-3 py-1.5"
                >
                  {kp.mastery_level > 0 ? (
                    <CheckCircle className="mt-0.5 h-3 w-3 shrink-0 text-primary" />
                  ) : (
                    <Lightbulb className="mt-0.5 h-3 w-3 shrink-0 text-muted-foreground" />
                  )}
                  <div className="min-w-0 flex-1">
                    <p className="text-[12px] font-medium">{kp.concept}</p>
                    <p className="mt-0.5 line-clamp-2 text-[11px] leading-relaxed text-muted-foreground">
                      {kp.explanation}
                    </p>
                  </div>
                  <Badge
                    variant={difficultyTone[kp.difficulty] || "mono"}
                    className="shrink-0"
                  >
                    {t(
                      difficultyKey[kp.difficulty] as
                        | "difficulty_basic"
                        | "difficulty_simple"
                        | "difficulty_moderate"
                        | "difficulty_complex"
                        | "difficulty_advanced",
                    )}
                  </Badge>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
});

interface ChapterTreeProps {
  chapters: Chapter[];
  bookId?: string;
}

export function ChapterTree({ chapters, bookId }: ChapterTreeProps) {
  const t = useTranslations("book.tree");
  const [expandedChapters, setExpandedChapters] = useState<Set<string>>(
    () => new Set(chapters.length > 0 ? [chapters[0].id] : []),
  );

  const toggleChapter = (id: string) => {
    setExpandedChapters((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  if (chapters.length === 0) {
    return (
      <p className="px-3 py-6 text-center text-[13px] text-muted-foreground">
        {t("empty")}
      </p>
    );
  }

  return (
    <div className="space-y-0.5">
      {chapters.map((chapter) => {
        const isExpanded = expandedChapters.has(chapter.id);
        const totalKPs = chapter.sections.reduce(
          (sum, s) => sum + s.knowledge_points.length,
          0,
        );

        return (
          <div key={chapter.id}>
            <div className="group flex items-center gap-1 rounded-lg pr-1 transition-colors hover:bg-subtle/60">
              <button
                onClick={() => toggleChapter(chapter.id)}
                className="flex flex-1 items-center gap-2 px-3 py-2 text-left"
              >
                <ChevronRight
                  className={cn(
                    "h-3.5 w-3.5 text-muted-foreground transition-transform",
                    isExpanded && "rotate-90",
                  )}
                />
                <span className="flex-1 truncate font-heading text-[14px] font-semibold tracking-tight">
                  {chapter.title}
                </span>
                <span className="font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground tabular-nums">
                  {t("section_count", { count: chapter.sections.length })}
                  {" · "}
                  {t("concept_count", { count: totalKPs })}
                </span>
              </button>
              {bookId && (
                <Link
                  href={`/book/${bookId}/read?chapter=${chapter.id}`}
                  className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md text-muted-foreground opacity-0 transition-all hover:bg-background hover:text-foreground group-hover:opacity-100 focus-visible:opacity-100"
                  aria-label={t("open_in_reader")}
                  title={t("open_in_reader")}
                >
                  <ArrowUpRight className="h-3.5 w-3.5" />
                </Link>
              )}
            </div>

            <AnimatePresence>
              {isExpanded && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.2 }}
                  className="overflow-hidden"
                >
                  <div className="space-y-0.5 pb-2">
                    {chapter.sections.map((section) => (
                      <SectionItem key={section.id} section={section} />
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        );
      })}
    </div>
  );
}
