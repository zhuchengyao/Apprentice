"use client";

import { useEffect, useState } from "react";
import { use } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { ArrowLeft, Loader2, GraduationCap, BookOpen, AlertCircle, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ChapterTree } from "@/components/book/chapter-tree";
import { BookStats } from "@/components/book/book-stats";
import { ProcessingAnimation } from "@/components/upload/processing-animation";
import { api } from "@/lib/api-client";
import type { BookDetail } from "@/lib/types";
import type { BookStatus } from "@/lib/constants";

export default function BookOverviewPage({
  params,
}: {
  params: Promise<{ bookId: string }>;
}) {
  const { bookId } = use(params);
  const router = useRouter();
  const [book, setBook] = useState<BookDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState(false);

  const handleDelete = async () => {
    if (!confirm("Delete this book? This cannot be undone.")) return;
    setDeleting(true);
    try {
      await api.delete(`/books/${bookId}`);
      router.push("/library");
    } catch {
      setDeleting(false);
      alert("Failed to delete book.");
    }
  };

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;

    async function fetchBook() {
      try {
        const data = await api.get<BookDetail>(`/books/${bookId}`);
        setBook(data);
        setLoading(false);

        // If still processing, poll for updates
        if (
          data.status === "uploading" ||
          data.status === "parsing" ||
          data.status === "extracting"
        ) {
          interval = setInterval(async () => {
            try {
              const updated = await api.get<BookDetail>(`/books/${bookId}`);
              setBook(updated);
              if (updated.status === "ready" || updated.status === "error") {
                if (interval) clearInterval(interval);
              }
            } catch {
              // ignore polling errors
            }
          }, 3000);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load book");
        setLoading(false);
      }
    }

    fetchBook();
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [bookId]);

  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (error || !book) {
    return (
      <div className="mx-auto max-w-7xl px-6 py-8">
        <Link href="/library">
          <Button variant="ghost" size="sm" className="mb-6 gap-1.5">
            <ArrowLeft className="h-4 w-4" />
            Back to library
          </Button>
        </Link>
        <div className="flex flex-col items-center justify-center py-24">
          <AlertCircle className="h-10 w-10 text-destructive" />
          <p className="mt-4 text-sm text-muted-foreground">{error || "Book not found"}</p>
        </div>
      </div>
    );
  }

  const isProcessing = ["uploading", "parsing", "extracting"].includes(book.status);

  // Find first section for "Start studying" button
  const firstSection = book.chapters?.[0]?.sections?.[0];

  return (
    <div className="mx-auto max-w-7xl px-6 py-8">
      <Link href="/library">
        <Button variant="ghost" size="sm" className="mb-6 gap-1.5">
          <ArrowLeft className="h-4 w-4" />
          Back to library
        </Button>
      </Link>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">{book.title}</h1>
            {book.author && book.author !== "Unknown" && (
              <p className="mt-1 text-sm text-muted-foreground">by {book.author}</p>
            )}
          </div>
          <div className="flex items-center gap-2">
            <Badge
              variant={book.status === "ready" ? "default" : book.status === "error" ? "destructive" : "secondary"}
            >
              {book.status}
            </Badge>
            <Button
              variant="ghost"
              size="icon"
              className="text-muted-foreground hover:text-destructive"
              onClick={handleDelete}
              disabled={deleting}
            >
              {deleting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Trash2 className="h-4 w-4" />}
            </Button>
          </div>
        </div>

        {/* Processing state */}
        {isProcessing && (
          <div className="mt-8">
            <ProcessingAnimation status={book.status as BookStatus} />
            <p className="mt-6 text-center text-sm text-muted-foreground">
              This may take a minute depending on the book size...
            </p>
          </div>
        )}

        {/* Error state */}
        {book.status === "error" && (
          <div className="mt-8 rounded-lg border border-destructive/20 bg-destructive/5 p-4">
            <p className="text-sm text-destructive">
              Processing failed. You can try re-uploading the book.
            </p>
          </div>
        )}

        {/* Ready state — show stats + chapter tree */}
        {book.status === "ready" && (
          <>
            {/* Stats */}
            <div className="mt-8">
              <BookStats book={book} />
            </div>

            {/* Start studying CTA */}
            <div className="mt-6 flex gap-3">
              <Link href={`/book/${bookId}/read`}>
                <Button size="lg" variant="outline" className="gap-2">
                  <BookOpen className="h-5 w-5" />
                  Read book
                </Button>
              </Link>
              {firstSection && (
                <Link href={`/book/${bookId}/study/${firstSection.id}`}>
                  <Button size="lg" className="gap-2">
                    <GraduationCap className="h-5 w-5" />
                    Start studying
                  </Button>
                </Link>
              )}
            </div>

            {/* Chapter tree */}
            <div className="mt-8">
              <h2 className="mb-4 text-lg font-semibold">Contents</h2>
              <div className="rounded-xl border bg-card p-2">
                <ChapterTree chapters={book.chapters} bookId={bookId} />
              </div>
            </div>
          </>
        )}
      </motion.div>
    </div>
  );
}
