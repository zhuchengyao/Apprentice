"use client";

import { AnimatePresence } from "framer-motion";
import { BookCard } from "./book-card";
import type { Book } from "@/lib/types";

interface BookGridProps {
  books: Book[];
  selectedIds?: Set<string>;
  onToggleSelect?: (id: string) => void;
}

export function BookGrid({ books, selectedIds, onToggleSelect }: BookGridProps) {
  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
      <AnimatePresence>
        {books.map((book, index) => (
          <BookCard
            key={book.id}
            book={book}
            index={index}
            selected={selectedIds?.has(book.id) ?? false}
            onToggleSelect={onToggleSelect}
          />
        ))}
      </AnimatePresence>
    </div>
  );
}
