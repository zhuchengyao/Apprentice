"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { BookOpen, Loader2 } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { Book } from "@/lib/types";

interface BookCardProps {
  book: Book;
  index: number;
}

function ProgressRing({ progress, size = 40 }: { progress: number; size?: number }) {
  const strokeWidth = 3;
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
        className="text-muted"
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
        className="text-foreground transition-all duration-700"
      />
    </svg>
  );
}

const statusConfig: Record<string, { label: string; variant: "default" | "secondary" | "destructive" | "outline" }> = {
  uploading: { label: "Uploading", variant: "secondary" },
  parsing: { label: "Parsing", variant: "secondary" },
  extracting: { label: "Analyzing", variant: "secondary" },
  ready: { label: "Ready", variant: "default" },
  error: { label: "Error", variant: "destructive" },
};

export function BookCard({ book, index }: BookCardProps) {
  const statusInfo = statusConfig[book.status] || statusConfig.ready;
  const isProcessing = ["uploading", "parsing", "extracting"].includes(book.status);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05, duration: 0.3 }}
    >
      <Link href={`/book/${book.id}`}>
        <motion.div
          whileHover={{ y: -4, boxShadow: "0 12px 40px -12px rgba(0,0,0,0.15)" }}
          transition={{ type: "spring", stiffness: 400, damping: 25 }}
          className="group relative flex flex-col overflow-hidden rounded-xl border bg-card transition-colors hover:border-foreground/20"
        >
          {/* Cover area */}
          <div className="relative flex h-48 items-center justify-center bg-gradient-to-br from-muted/50 to-muted">
            <BookOpen className="h-12 w-12 text-muted-foreground/40" />
            {isProcessing && (
              <div className="absolute inset-0 flex items-center justify-center bg-background/60 backdrop-blur-sm">
                <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
              </div>
            )}
            <div className="absolute top-3 right-3">
              <Badge variant={statusInfo.variant} className="text-[10px] px-2 py-0.5">
                {statusInfo.label}
              </Badge>
            </div>
          </div>

          {/* Info area */}
          <div className="flex flex-1 items-start justify-between gap-3 p-4">
            <div className="min-w-0 flex-1">
              <h3 className="truncate text-sm font-semibold leading-tight group-hover:text-foreground">
                {book.title}
              </h3>
              <p className="mt-1 truncate text-xs text-muted-foreground">
                {book.author}
              </p>
              {book.status === "ready" && book.total_knowledge_points > 0 && (
                <p className="mt-2 text-xs text-muted-foreground">
                  {book.mastered_knowledge_points}/{book.total_knowledge_points} concepts
                </p>
              )}
            </div>

            {book.status === "ready" && (
              <div className="relative flex items-center justify-center">
                <ProgressRing progress={book.progress} />
                <span className={cn(
                  "absolute text-[10px] font-bold",
                  book.progress > 0 ? "text-foreground" : "text-muted-foreground"
                )}>
                  {Math.round(book.progress)}%
                </span>
              </div>
            )}
          </div>
        </motion.div>
      </Link>
    </motion.div>
  );
}
