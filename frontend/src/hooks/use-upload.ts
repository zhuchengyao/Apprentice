"use client";

import { useState, useCallback } from "react";
import { api } from "@/lib/api-client";
import type { Book } from "@/lib/types";

interface UploadState {
  isUploading: boolean;
  progress: number;
  error: string | null;
  book: Book | null;
}

export function useUpload() {
  const [state, setState] = useState<UploadState>({
    isUploading: false,
    progress: 0,
    error: null,
    book: null,
  });

  const upload = useCallback(async (file: File) => {
    setState({ isUploading: true, progress: 0, error: null, book: null });

    try {
      setState((s) => ({ ...s, progress: 30 }));
      const book = await api.upload<Book>("/books/upload", file);
      setState({ isUploading: false, progress: 100, error: null, book });
      return book;
    } catch (err) {
      const message = err instanceof Error ? err.message : "Upload failed";
      setState({ isUploading: false, progress: 0, error: message, book: null });
      return null;
    }
  }, []);

  const reset = useCallback(() => {
    setState({ isUploading: false, progress: 0, error: null, book: null });
  }, []);

  return { ...state, upload, reset };
}
