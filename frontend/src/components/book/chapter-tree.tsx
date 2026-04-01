"use client";

import { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import {
  ChevronRight,
  BookOpen,
  Lightbulb,
  GraduationCap,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { Chapter, Section } from "@/lib/types";

const difficultyLabels: Record<number, string> = {
  1: "Basic",
  2: "Simple",
  3: "Moderate",
  4: "Complex",
  5: "Advanced",
};

const difficultyColors: Record<number, string> = {
  1: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
  2: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400",
  3: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400",
  4: "bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400",
  5: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
};

function SectionItem({
  section,
  bookId,
}: {
  section: Section;
  bookId: string;
}) {
  const [expanded, setExpanded] = useState(false);
  const kpCount = section.knowledge_points.length;

  return (
    <div className="border-l-2 border-border ml-3 pl-4">
      <button
        onClick={() => setExpanded(!expanded)}
        className="group flex w-full items-center gap-2 rounded-lg px-3 py-2 text-left text-sm transition-colors hover:bg-accent/50"
      >
        <ChevronRight
          className={cn(
            "h-3.5 w-3.5 text-muted-foreground transition-transform",
            expanded && "rotate-90",
          )}
        />
        <BookOpen className="h-3.5 w-3.5 text-muted-foreground" />
        <span className="flex-1 truncate font-medium">{section.title}</span>
        <span className="text-xs text-muted-foreground">
          {kpCount} concept{kpCount !== 1 ? "s" : ""}
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
              <p className="mx-3 mb-2 text-xs text-muted-foreground leading-relaxed">
                {section.summary}
              </p>
            )}

            <div className="space-y-1 pb-2">
              {section.knowledge_points.map((kp) => (
                <div
                  key={kp.id}
                  className="flex items-start gap-2 rounded-md px-3 py-1.5 ml-2"
                >
                  <Lightbulb className="mt-0.5 h-3 w-3 shrink-0 text-muted-foreground" />
                  <div className="min-w-0 flex-1">
                    <p className="text-xs font-medium">{kp.concept}</p>
                    <p className="mt-0.5 text-[11px] text-muted-foreground line-clamp-2">
                      {kp.explanation}
                    </p>
                  </div>
                  <Badge
                    variant="secondary"
                    className={cn(
                      "shrink-0 text-[10px] px-1.5 py-0",
                      difficultyColors[kp.difficulty],
                    )}
                  >
                    {difficultyLabels[kp.difficulty] || "?"}
                  </Badge>
                </div>
              ))}
            </div>

            <Link
              href={`/book/${bookId}/study/${section.id}`}
              className="mx-3 mb-3 flex items-center gap-1.5 rounded-lg bg-foreground px-3 py-1.5 text-xs font-medium text-background transition-opacity hover:opacity-90 w-fit"
            >
              <GraduationCap className="h-3.5 w-3.5" />
              Study this section
            </Link>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

interface ChapterTreeProps {
  chapters: Chapter[];
  bookId: string;
}

export function ChapterTree({ chapters, bookId }: ChapterTreeProps) {
  const [expandedChapters, setExpandedChapters] = useState<Set<string>>(
    new Set(chapters.length <= 3 ? chapters.map((c) => c.id) : []),
  );

  const toggleChapter = (id: string) => {
    setExpandedChapters((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  return (
    <div className="space-y-1">
      {chapters.map((chapter) => {
        const isExpanded = expandedChapters.has(chapter.id);
        const totalKPs = chapter.sections.reduce(
          (sum, s) => sum + s.knowledge_points.length,
          0,
        );

        return (
          <div key={chapter.id}>
            <button
              onClick={() => toggleChapter(chapter.id)}
              className="group flex w-full items-center gap-2 rounded-lg px-3 py-2.5 text-left transition-colors hover:bg-accent/50"
            >
              <ChevronRight
                className={cn(
                  "h-4 w-4 text-muted-foreground transition-transform",
                  isExpanded && "rotate-90",
                )}
              />
              <span className="flex-1 text-sm font-semibold">
                {chapter.title}
              </span>
              <span className="text-xs text-muted-foreground">
                {chapter.sections.length} section{chapter.sections.length !== 1 ? "s" : ""}
                {" · "}
                {totalKPs} concept{totalKPs !== 1 ? "s" : ""}
              </span>
            </button>

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
                      <SectionItem
                        key={section.id}
                        section={section}
                        bookId={bookId}
                      />
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
