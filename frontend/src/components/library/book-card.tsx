"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { useTranslations } from "next-intl";
import { BookOpen, Loader2, Check } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { Book } from "@/lib/types";

interface BookCardProps {
  book: Book;
  index: number;
  selected?: boolean;
  onToggleSelect?: (id: string) => void;
}

function ProgressRing({
  progress,
  size = 42,
}: {
  progress: number;
  size?: number;
}) {
  const strokeWidth = 2.5;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  return (
    <svg width={size} height={size} className="-rotate-90">
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        stroke="currentColor"
        strokeWidth={strokeWidth}
        fill="none"
        className="text-border"
      />
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        stroke="currentColor"
        strokeWidth={strokeWidth}
        fill="none"
        strokeDasharray={circumference}
        strokeDashoffset={strokeDashoffset}
        strokeLinecap="round"
        className="text-primary transition-all duration-700"
      />
    </svg>
  );
}

const statusVariants: Record<
  string,
  "mono" | "success" | "warning" | "destructive" | "primary"
> = {
  uploading: "mono",
  parsing: "mono",
  extracting: "mono",
  ready: "success",
  error: "destructive",
};

// Deterministic gradient based on book id, indigo-adjacent palette
function coverGradient(id: string) {
  let hash = 0;
  for (let i = 0; i < id.length; i++) hash = (hash * 31 + id.charCodeAt(i)) | 0;
  const hue = 230 + (Math.abs(hash) % 90); // 230-320 (indigo → violet → rose)
  return `linear-gradient(135deg, oklch(0.52 0.15 ${hue}) 0%, oklch(0.42 0.13 ${(hue + 30) % 360}) 100%)`;
}

export function BookCard({
  book,
  index,
  selected,
  onToggleSelect,
}: BookCardProps) {
  const tStatus = useTranslations("library.status");
  const tCard = useTranslations("library.book_card");
  const statusKey = book.status in statusVariants ? book.status : "ready";
  const statusVariant = statusVariants[statusKey];
  const isProcessing = ["uploading", "parsing", "extracting"].includes(
    book.status,
  );
  const selectable = !!onToggleSelect;
  const gradient = coverGradient(book.id);

  const cardContent = (
    <motion.div
      whileHover={{ y: -2 }}
      transition={{ type: "spring", stiffness: 400, damping: 26 }}
      className={cn(
        "group relative flex flex-col overflow-hidden rounded-2xl bg-card ring-1 ring-border/60 transition-all",
        "hover:ring-border hover:shadow-editorial",
        selected && "ring-2 ring-primary ring-offset-2 ring-offset-background",
      )}
    >
      {selectable && (
        <button
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            onToggleSelect(book.id);
          }}
          className={cn(
            "absolute top-3 left-3 z-10 flex h-5 w-5 items-center justify-center rounded-md border transition-colors",
            selected
              ? "border-primary bg-primary text-primary-foreground"
              : "border-border bg-background/80 backdrop-blur hover:border-foreground",
          )}
        >
          {selected && <Check className="h-3 w-3" />}
        </button>
      )}

      {/* Book cover — spine + face */}
      <div className="relative aspect-[4/3] overflow-hidden">
        <div
          className="absolute inset-0 flex items-end p-5"
          style={{ background: gradient }}
        >
          {/* Subtle paper texture overlay */}
          <div
            aria-hidden
            className="absolute inset-0 opacity-30"
            style={{
              background:
                "radial-gradient(ellipse at top left, rgba(255,255,255,0.25), transparent 50%)",
            }}
          />
          <div
            aria-hidden
            className="absolute inset-y-0 left-0 w-px bg-black/20"
          />
          <div className="relative z-10 flex w-full items-end justify-between gap-3">
            <h3 className="line-clamp-3 font-heading text-[16px] font-semibold leading-tight tracking-tight text-white/95 drop-shadow-sm">
              {book.title}
            </h3>
            <BookOpen className="h-5 w-5 shrink-0 text-white/50" />
          </div>
        </div>

        {isProcessing && (
          <div className="absolute inset-0 flex items-center justify-center bg-background/60 backdrop-blur-sm">
            <Loader2 className="h-7 w-7 animate-spin text-primary" />
          </div>
        )}

        <div className="absolute top-3 right-3">
          <Badge variant={statusVariant}>{tStatus(statusKey)}</Badge>
        </div>
      </div>

      {/* Info strip */}
      <div className="flex items-center justify-between gap-3 p-4">
        <div className="min-w-0 flex-1">
          <p className="truncate font-mono text-[10px] uppercase tracking-[0.12em] text-muted-foreground">
            {book.author || tCard("unknown_author")}
          </p>
          {book.status === "ready" && book.total_knowledge_points > 0 ? (
            <p className="mt-1 text-[12.5px] text-foreground/90 tabular-nums">
              <span className="font-medium">
                {book.mastered_knowledge_points}
              </span>
              <span className="text-muted-foreground">
                {" / "}
                {book.total_knowledge_points} {tCard("concepts_suffix")}
              </span>
            </p>
          ) : (
            <p className="mt-1 text-[12.5px] text-muted-foreground">
              {isProcessing ? tCard("working") : tCard("no_concepts")}
            </p>
          )}
        </div>

        {book.status === "ready" && (
          <div className="relative flex shrink-0 items-center justify-center">
            <ProgressRing progress={book.progress} />
            <span
              className={cn(
                "absolute font-mono text-[10px] tabular-nums",
                book.progress > 0 ? "text-foreground" : "text-muted-foreground",
              )}
            >
              {Math.round(book.progress)}%
            </span>
          </div>
        )}
      </div>
    </motion.div>
  );

  if (selectable) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: index * 0.03, duration: 0.3 }}
        className="cursor-pointer"
        onClick={() => onToggleSelect(book.id)}
      >
        {cardContent}
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.03, duration: 0.3 }}
    >
      <Link href={`/book/${book.id}`}>{cardContent}</Link>
    </motion.div>
  );
}
