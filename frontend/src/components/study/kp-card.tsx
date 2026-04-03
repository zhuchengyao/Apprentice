"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Send, CheckCircle, ChevronDown, ChevronRight, BookOpen, Lightbulb, MessageSquare, Loader2, Image as ImageIcon } from "lucide-react";
import { Markdown } from "@/components/ui/markdown";
import type { KnowledgePointDetail, KPCardState } from "@/lib/types";

interface KPCardProps {
  index: number;
  kp: KnowledgePointDetail;
  cardState: KPCardState;
  isActive: boolean;
  streamContent: string;
  streamTarget: "illustration" | "question" | "deepen" | "secondQuestion" | null;
  isStreaming: boolean;
  onExpand: (index: number) => void;
  onSendAnswer: (answer: string) => void;
}

const STATUS_LABELS: Record<string, string> = {
  pending: "Not started",
  illustrating: "Illustrating...",
  checking: "Generating question...",
  answering: "Your turn",
  evaluating: "Evaluating...",
  deepening: "Deepening...",
  completed: "Completed",
};

export function KPCard({
  index,
  kp,
  cardState,
  isActive,
  streamContent,
  streamTarget,
  isStreaming,
  onExpand,
  onSendAnswer,
}: KPCardProps) {
  const [answer, setAnswer] = useState("");
  const isExpanded = isActive;
  const isPending = cardState.status === "pending";
  const isCompleted = cardState.status === "completed";

  const handleSend = () => {
    const trimmed = answer.trim();
    if (!trimmed) return;
    onSendAnswer(trimmed);
    setAnswer("");
  };

  // Folded card — just title
  if (!isExpanded) {
    return (
      <button
        onClick={() => onExpand(index)}
        className={cn(
          "w-full text-left rounded-lg border px-4 py-3 transition-colors",
          isCompleted
            ? "border-green-200 bg-green-50 dark:border-green-900 dark:bg-green-950"
            : "border-border bg-card hover:bg-accent",
        )}
      >
        <div className="flex items-center gap-3">
          {isCompleted ? (
            <CheckCircle className="h-4 w-4 text-green-600 shrink-0" />
          ) : (
            <ChevronRight className="h-4 w-4 text-muted-foreground shrink-0" />
          )}
          <span className="font-medium text-sm truncate">
            {index + 1}. {kp.concept}
          </span>
          <Badge variant="secondary" className="ml-auto text-xs shrink-0">
            {STATUS_LABELS[cardState.status]}
          </Badge>
        </div>
      </button>
    );
  }

  // Expanded card
  // Show first answer input when question is ready and user hasn't answered yet
  const waitingForAnswer =
    cardState.question && !isStreaming && !cardState.userAnswer && cardState.status !== "completed";
  // Show second answer input after deepen + second question
  const waitingForSecondAnswer =
    cardState.feedback && cardState.feedback.quality < 3 && cardState.secondQuestion && !isStreaming && !cardState.secondAnswer && cardState.status !== "completed";

  return (
    <div className="rounded-xl border-2 border-primary/30 bg-card overflow-hidden">
      {/* Header */}
      <button
        onClick={() => onExpand(index)}
        className="w-full text-left px-5 py-4 flex items-center gap-3 border-b bg-muted/30"
      >
        <ChevronDown className="h-4 w-4 text-muted-foreground shrink-0" />
        <span className="font-semibold text-sm">
          {index + 1}. {kp.concept}
        </span>
        <Badge variant="secondary" className="ml-auto text-xs">
          {STATUS_LABELS[cardState.status]}
        </Badge>
      </button>

      <div className="px-5 py-4 space-y-5">
        {/* Original curriculum content */}
        <div className="space-y-1.5">
          <div className="flex items-center gap-1.5 text-xs font-medium text-muted-foreground uppercase tracking-wide">
            <BookOpen className="h-3.5 w-3.5" />
            Curriculum
          </div>
          <div className="text-sm leading-relaxed text-foreground/80 prose prose-sm dark:prose-invert max-w-none">
            <Markdown>{kp.explanation}</Markdown>
          </div>
        </div>

        {/* Associated Figures */}
        {kp.image_urls && kp.image_urls.length > 0 && (
          <div className="space-y-1.5">
            <div className="flex items-center gap-1.5 text-xs font-medium text-muted-foreground uppercase tracking-wide">
              <ImageIcon className="h-3.5 w-3.5" />
              Figures
            </div>
            <div className="flex flex-wrap gap-2">
              {kp.image_urls.map((url, i) => (
                <img
                  key={i}
                  src={url}
                  alt={`Figure ${i + 1} for ${kp.concept}`}
                  className="rounded-lg border max-h-64 object-contain bg-white"
                />
              ))}
            </div>
          </div>
        )}

        {/* AI Illustration */}
        {(cardState.illustration || (isStreaming && streamTarget === "illustration")) && (
          <div className="space-y-1.5">
            <div className="flex items-center gap-1.5 text-xs font-medium text-muted-foreground uppercase tracking-wide">
              <Lightbulb className="h-3.5 w-3.5" />
              Illustration
            </div>
            <div className="text-sm leading-relaxed rounded-lg bg-blue-50 dark:bg-blue-950/30 p-3 prose prose-sm dark:prose-invert max-w-none">
              {isStreaming && streamTarget === "illustration" ? (
                <span className="whitespace-pre-wrap">
                  {(cardState.illustration || "") + streamContent}
                  <span className="inline-block w-1.5 h-4 ml-0.5 bg-foreground/50 animate-pulse" />
                </span>
              ) : (
                <Markdown>{cardState.illustration}</Markdown>
              )}
            </div>
          </div>
        )}

        {/* Comprehension Question */}
        {(cardState.question || (isStreaming && streamTarget === "question")) && (
          <div className="space-y-1.5">
            <div className="flex items-center gap-1.5 text-xs font-medium text-muted-foreground uppercase tracking-wide">
              <MessageSquare className="h-3.5 w-3.5" />
              Comprehension Check
            </div>
            <div className="text-sm leading-relaxed rounded-lg bg-amber-50 dark:bg-amber-950/30 p-3 prose prose-sm dark:prose-invert max-w-none">
              {isStreaming && streamTarget === "question" ? (
                <span className="whitespace-pre-wrap">
                  {(cardState.question || "") + streamContent}
                  <span className="inline-block w-1.5 h-4 ml-0.5 bg-foreground/50 animate-pulse" />
                </span>
              ) : (
                <Markdown>{cardState.question}</Markdown>
              )}
            </div>
          </div>
        )}

        {/* Answer input (first round) */}
        {waitingForAnswer && !waitingForSecondAnswer && !cardState.userAnswer && (
          <div className="flex items-end gap-2">
            <textarea
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder="Type your answer..."
              rows={2}
              className="flex-1 resize-none rounded-lg border bg-background px-3 py-2 text-sm outline-none placeholder:text-muted-foreground focus:ring-2 focus:ring-ring"
            />
            <Button size="icon" onClick={handleSend} disabled={!answer.trim()}>
              <Send className="h-4 w-4" />
            </Button>
          </div>
        )}

        {/* User's first answer */}
        {cardState.userAnswer && (
          <div className="text-sm rounded-lg bg-primary/10 p-3">
            <span className="text-xs font-medium text-muted-foreground">Your answer:</span>
            <p className="mt-1">{cardState.userAnswer}</p>
          </div>
        )}

        {/* First feedback */}
        {cardState.feedback && (
          <div className={cn(
            "text-sm rounded-lg p-3",
            cardState.feedback.quality >= 3
              ? "bg-green-50 dark:bg-green-950/30"
              : "bg-orange-50 dark:bg-orange-950/30",
          )}>
            <span className="text-xs font-medium text-muted-foreground">
              Score: {cardState.feedback.quality}/5
            </span>
            <div className="mt-1 prose prose-sm dark:prose-invert max-w-none">
              <Markdown>{cardState.feedback.feedback}</Markdown>
            </div>
          </div>
        )}

        {/* Deepen text */}
        {(cardState.deepenText || (isStreaming && streamTarget === "deepen")) && (
          <div className="space-y-1.5">
            <div className="flex items-center gap-1.5 text-xs font-medium text-muted-foreground uppercase tracking-wide">
              <Lightbulb className="h-3.5 w-3.5" />
              Let&apos;s try another approach
            </div>
            <div className="text-sm leading-relaxed rounded-lg bg-purple-50 dark:bg-purple-950/30 p-3 prose prose-sm dark:prose-invert max-w-none">
              {isStreaming && streamTarget === "deepen" ? (
                <span className="whitespace-pre-wrap">
                  {(cardState.deepenText || "") + streamContent}
                  <span className="inline-block w-1.5 h-4 ml-0.5 bg-foreground/50 animate-pulse" />
                </span>
              ) : (
                <Markdown>{cardState.deepenText}</Markdown>
              )}
            </div>
          </div>
        )}

        {/* Second question */}
        {(cardState.secondQuestion || (isStreaming && streamTarget === "secondQuestion")) && (
          <div className="space-y-1.5">
            <div className="flex items-center gap-1.5 text-xs font-medium text-muted-foreground uppercase tracking-wide">
              <MessageSquare className="h-3.5 w-3.5" />
              Let&apos;s try again
            </div>
            <div className="text-sm leading-relaxed rounded-lg bg-amber-50 dark:bg-amber-950/30 p-3 prose prose-sm dark:prose-invert max-w-none">
              {isStreaming && streamTarget === "secondQuestion" ? (
                <span className="whitespace-pre-wrap">
                  {(cardState.secondQuestion || "") + streamContent}
                  <span className="inline-block w-1.5 h-4 ml-0.5 bg-foreground/50 animate-pulse" />
                </span>
              ) : (
                <Markdown>{cardState.secondQuestion}</Markdown>
              )}
            </div>
          </div>
        )}

        {/* Second answer input */}
        {waitingForSecondAnswer && (
          <div className="flex items-end gap-2">
            <textarea
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder="Try again..."
              rows={2}
              className="flex-1 resize-none rounded-lg border bg-background px-3 py-2 text-sm outline-none placeholder:text-muted-foreground focus:ring-2 focus:ring-ring"
            />
            <Button size="icon" onClick={handleSend} disabled={!answer.trim()}>
              <Send className="h-4 w-4" />
            </Button>
          </div>
        )}

        {/* Second answer + feedback */}
        {cardState.secondAnswer && (
          <div className="text-sm rounded-lg bg-primary/10 p-3">
            <span className="text-xs font-medium text-muted-foreground">Your answer:</span>
            <p className="mt-1">{cardState.secondAnswer}</p>
          </div>
        )}
        {cardState.secondFeedback && (
          <div className={cn(
            "text-sm rounded-lg p-3",
            cardState.secondFeedback.quality >= 3
              ? "bg-green-50 dark:bg-green-950/30"
              : "bg-orange-50 dark:bg-orange-950/30",
          )}>
            <span className="text-xs font-medium text-muted-foreground">
              Score: {cardState.secondFeedback.quality}/5
            </span>
            <div className="mt-1 prose prose-sm dark:prose-invert max-w-none">
              <Markdown>{cardState.secondFeedback.feedback}</Markdown>
            </div>
          </div>
        )}

        {/* Loading indicator during evaluate */}
        {cardState.status === "evaluating" && (
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Loader2 className="h-4 w-4 animate-spin" />
            Evaluating your answer...
          </div>
        )}

        {/* Completed marker */}
        {isCompleted && (
          <div className="flex items-center gap-2 text-sm text-green-600 dark:text-green-400 pt-2 border-t">
            <CheckCircle className="h-4 w-4" />
            Knowledge point mastered
          </div>
        )}
      </div>
    </div>
  );
}
