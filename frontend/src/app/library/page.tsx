"use client";

import { useEffect, useState, useCallback } from "react";
import { motion } from "framer-motion";
import { Plus, BookOpen, Trash2, X, Loader2 } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { BookGrid } from "@/components/library/book-grid";
import { api } from "@/lib/api-client";
import type { Book } from "@/lib/types";

export default function LibraryPage() {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectMode, setSelectMode] = useState(false);
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    async function fetchBooks() {
      try {
        const data = await api.get<{ books: Book[] }>("/books");
        setBooks(data.books);
      } catch {
        // API not available yet — show empty state
      } finally {
        setLoading(false);
      }
    }
    fetchBooks();

    // Poll for status updates if any books are processing
    const interval = setInterval(async () => {
      try {
        const data = await api.get<{ books: Book[] }>("/books");
        setBooks(data.books);
        const hasProcessing = data.books.some((b) =>
          ["uploading", "parsing", "extracting"].includes(b.status),
        );
        if (!hasProcessing) clearInterval(interval);
      } catch {
        // ignore polling errors
      }
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  const toggleSelect = useCallback((id: string) => {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }, []);

  const exitSelectMode = useCallback(() => {
    setSelectMode(false);
    setSelectedIds(new Set());
  }, []);

  const handleDeleteSelected = useCallback(async () => {
    if (selectedIds.size === 0) return;
    const count = selectedIds.size;
    if (!confirm(`Delete ${count} book${count > 1 ? "s" : ""}? This cannot be undone.`)) return;

    setDeleting(true);
    try {
      await Promise.all(
        Array.from(selectedIds).map((id) => api.delete(`/books/${id}`)),
      );
      setBooks((prev) => prev.filter((b) => !selectedIds.has(b.id)));
      exitSelectMode();
    } catch {
      alert("Some books failed to delete.");
    } finally {
      setDeleting(false);
    }
  }, [selectedIds, exitSelectMode]);

  return (
    <div className="mx-auto max-w-7xl px-6 py-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Library</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            {books.length > 0
              ? `${books.length} book${books.length === 1 ? "" : "s"}`
              : "Your books will appear here"}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {selectMode ? (
            <>
              <span className="text-sm text-muted-foreground">
                {selectedIds.size} selected
              </span>
              <Button
                size="sm"
                variant="destructive"
                className="gap-1.5"
                disabled={selectedIds.size === 0 || deleting}
                onClick={handleDeleteSelected}
              >
                {deleting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Trash2 className="h-4 w-4" />}
                Delete
              </Button>
              <Button size="sm" variant="ghost" onClick={exitSelectMode}>
                <X className="h-4 w-4" />
              </Button>
            </>
          ) : (
            <>
              {books.length > 0 && (
                <Button
                  size="sm"
                  variant="outline"
                  className="gap-1.5"
                  onClick={() => setSelectMode(true)}
                >
                  <Trash2 className="h-4 w-4" />
                  Select
                </Button>
              )}
              <Link href="/">
                <Button size="sm" className="gap-1.5">
                  <Plus className="h-4 w-4" />
                  Add book
                </Button>
              </Link>
            </>
          )}
        </div>
      </div>

      <div className="mt-8">
        {loading ? (
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="animate-pulse rounded-xl border bg-card">
                <div className="h-48 rounded-t-xl bg-muted" />
                <div className="p-4 space-y-2">
                  <div className="h-4 w-3/4 rounded bg-muted" />
                  <div className="h-3 w-1/2 rounded bg-muted" />
                </div>
              </div>
            ))}
          </div>
        ) : books.length > 0 ? (
          <BookGrid
            books={books}
            selectedIds={selectMode ? selectedIds : undefined}
            onToggleSelect={selectMode ? toggleSelect : undefined}
          />
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center justify-center py-24"
          >
            <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-muted">
              <BookOpen className="h-10 w-10 text-muted-foreground" />
            </div>
            <h3 className="mt-6 text-lg font-semibold">No books yet</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Upload your first book to start learning
            </p>
            <Link href="/" className="mt-6">
              <Button className="gap-1.5">
                <Plus className="h-4 w-4" />
                Upload a book
              </Button>
            </Link>
          </motion.div>
        )}
      </div>
    </div>
  );
}
