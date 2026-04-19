"use client";

import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { useTranslations } from "next-intl";
import {
  ArrowRight,
  Check,
  CheckCircle2,
  ListChecks,
  Loader2,
  X,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Markdown } from "@/components/ui/markdown";
import { cn } from "@/lib/utils";
import type { QuizQuestion } from "@/lib/types";
import type { QuestionFeedback } from "@/lib/stores/study-session";

interface Props {
  question: QuizQuestion;
  index: number;
  total: number;
  feedback: QuestionFeedback | null;
  submitting: boolean;
  onSubmit: (chosenOption: string, timeSpentMs: number) => Promise<void> | void;
  onNext: () => void;
}

export function QuizCard({
  question,
  index,
  total,
  feedback,
  submitting,
  onSubmit,
  onNext,
}: Props) {
  const t = useTranslations("study");
  const [selected, setSelected] = useState<string | null>(null);
  const [startedAt] = useState<number>(() => Date.now());

  const answered = feedback?.question_id === question.id;

  const submit = async () => {
    if (!selected || answered || submitting) return;
    const elapsed = Date.now() - startedAt;
    await onSubmit(selected, elapsed);
  };

  return (
    <motion.div
      layout
      key={question.id}
      initial={{ opacity: 0, y: 10 }}
      animate={
        answered && feedback?.correct
          ? {
              opacity: 1,
              y: 0,
              scale: [1, 1.02, 1],
              transition: { duration: 0.45, times: [0, 0.4, 1] },
            }
          : answered && feedback && !feedback.correct
            ? {
                opacity: 1,
                y: 0,
                x: [0, -6, 6, -4, 4, 0],
                transition: { duration: 0.45 },
              }
            : { opacity: 1, y: 0 }
      }
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className={cn(
        "min-w-0 rounded-2xl border p-4 shadow-editorial-sm ring-1 transition-colors",
        answered && feedback?.correct
          ? "border-emerald-500/40 bg-emerald-50/40 ring-emerald-500/10 dark:bg-emerald-500/5"
          : answered && feedback && !feedback.correct
            ? "border-rose-500/40 bg-rose-50/40 ring-rose-500/10 dark:bg-rose-500/5"
            : "border-border/70 bg-card/60 ring-foreground/5",
      )}
    >
      <div className="flex items-start gap-3">
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary/12 text-primary ring-1 ring-primary/20">
          <ListChecks className="h-4 w-4" />
        </div>
        <div className="min-w-0 flex-1">
          <div className="flex items-center justify-between gap-2">
            <div className="font-mono text-[9.5px] uppercase tracking-[0.1em] text-muted-foreground">
              {t("phase.practice")}
            </div>
            <div className="font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground tabular-nums">
              {t("quiz_question_progress", { current: index + 1, total })}
            </div>
          </div>
          <div className="prose prose-sm dark:prose-invert mt-1.5 max-w-none text-[13.5px] leading-relaxed [&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
            <Markdown>{question.stem}</Markdown>
          </div>
        </div>
      </div>

      <div className="mt-3 flex flex-col gap-1.5">
        {question.options.map((opt) => {
          const isChosen = answered
            ? feedback?.chosen_option === opt.key
            : selected === opt.key;
          const isCorrect = answered && opt.key === feedback?.correct_option;
          const showAsCorrect = answered && isCorrect;
          const showAsWrong =
            answered && isChosen && !feedback?.correct;

          return (
            <button
              key={opt.key}
              type="button"
              onClick={() => !answered && !submitting && setSelected(opt.key)}
              disabled={answered || submitting}
              className={cn(
                "group flex items-start gap-2.5 rounded-xl border px-3 py-2 text-left text-[13px] transition-all",
                !answered &&
                  (isChosen
                    ? "border-primary/60 bg-primary/8 ring-1 ring-primary/20"
                    : "border-border/60 bg-background hover:border-border/80 hover:bg-subtle/40"),
                showAsCorrect &&
                  "border-emerald-500/60 bg-emerald-500/10 ring-1 ring-emerald-500/25",
                showAsWrong &&
                  "border-rose-500/60 bg-rose-500/10 ring-1 ring-rose-500/25",
                answered && !showAsCorrect && !showAsWrong && "opacity-70",
              )}
            >
              <span
                className={cn(
                  "mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-md font-mono text-[10.5px] font-semibold",
                  !answered &&
                    (isChosen
                      ? "bg-primary text-primary-foreground"
                      : "bg-subtle text-muted-foreground group-hover:bg-subtle/70"),
                  showAsCorrect && "bg-emerald-500 text-white",
                  showAsWrong && "bg-rose-500 text-white",
                  answered && !showAsCorrect && !showAsWrong &&
                    "bg-subtle text-muted-foreground",
                )}
              >
                {showAsCorrect ? (
                  <Check className="h-3 w-3" />
                ) : showAsWrong ? (
                  <X className="h-3 w-3" />
                ) : (
                  opt.key
                )}
              </span>
              <span className="prose prose-sm dark:prose-invert min-w-0 max-w-none flex-1 text-[13px] [&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
                <Markdown>{opt.text}</Markdown>
              </span>
            </button>
          );
        })}
      </div>

      <AnimatePresence initial={false}>
        {answered && feedback && (
          <motion.div
            key="feedback"
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -4 }}
            transition={{ duration: 0.2 }}
            className="mt-3 space-y-1.5"
          >
            <div
              className={cn(
                "flex items-center gap-2 font-mono text-[10.5px] uppercase tracking-[0.08em]",
                feedback.correct
                  ? "text-emerald-600 dark:text-emerald-400"
                  : "text-rose-600 dark:text-rose-400",
              )}
            >
              {feedback.correct ? (
                <CheckCircle2 className="h-3.5 w-3.5" />
              ) : (
                <X className="h-3.5 w-3.5" />
              )}
              <span>{feedback.correct ? t("correct") : t("incorrect")}</span>
            </div>
            {!feedback.correct && (
              <p className="text-[12px] text-muted-foreground">
                {t("correct_answer_was", { option: feedback.correct_option })}
              </p>
            )}
            <div className="prose prose-sm dark:prose-invert max-w-none text-[12.5px] leading-relaxed text-foreground/90 [&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
              <Markdown>{feedback.explanation}</Markdown>
            </div>
            {!feedback.correct && (
              <p className="text-[11.5px] italic text-muted-foreground">
                {t("missed_it_reassure")}
              </p>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      <div className="mt-3 flex items-center justify-end gap-2">
        {!answered ? (
          <Button
            size="sm"
            variant="primary"
            disabled={!selected || submitting}
            onClick={submit}
            className="h-8 gap-1.5 rounded-full px-3 text-[12px]"
          >
            {submitting ? (
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
            ) : (
              <>
                {t("quiz_submit")}
                <ArrowRight className="h-3.5 w-3.5" />
              </>
            )}
          </Button>
        ) : (
          <Button
            size="sm"
            variant="primary"
            onClick={onNext}
            className="h-8 gap-1.5 rounded-full px-3 text-[12px]"
          >
            {t("quiz_next")}
            <ArrowRight className="h-3.5 w-3.5" />
          </Button>
        )}
      </div>

    </motion.div>
  );
}
