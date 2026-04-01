export const ACCEPTED_FILE_TYPES = {
  "application/pdf": [".pdf"],
  "application/epub+zip": [".epub"],
  "text/plain": [".txt"],
};

export const BOOK_STATUS = {
  UPLOADING: "uploading",
  PARSING: "parsing",
  EXTRACTING: "extracting",
  READY: "ready",
  ERROR: "error",
} as const;

export type BookStatus = (typeof BOOK_STATUS)[keyof typeof BOOK_STATUS];

export const MASTERY_COLORS = {
  none: "hsl(var(--muted))",
  learning: "hsl(var(--chart-4))",
  mastered: "hsl(var(--chart-2))",
} as const;
