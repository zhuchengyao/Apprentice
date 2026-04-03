"use client";

import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import remarkGfm from "remark-gfm";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const remarkPlugins: any[] = [remarkMath, remarkGfm];
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const rehypePlugins: any[] = [rehypeKatex];

/**
 * Convert LaTeX delimiters to remark-math compatible format:
 *   \(...\)  →  $...$       (inline math)
 *   \[...\]  →  $$...$$     (display math)
 */
function normalizeLatex(text: string): string {
  // Display math: \[...\] → $$...$$  (handle multiline)
  text = text.replace(/\\\[([\s\S]*?)\\\]/g, (_match, inner) => `$$${inner}$$`);
  // Inline math: \(...\) → $...$
  text = text.replace(/\\\(([\s\S]*?)\\\)/g, (_match, inner) => `$${inner}$`);
  return text;
}

interface MarkdownProps {
  children: string;
}

export function Markdown({ children }: MarkdownProps) {
  const normalized = normalizeLatex(children);
  return (
    <ReactMarkdown
      remarkPlugins={remarkPlugins}
      rehypePlugins={rehypePlugins}
      components={{
        img: ({ src, alt, ...props }) => (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={src}
            alt={alt || "Book figure"}
            className="rounded-lg border my-3 max-w-full h-auto"
            loading="lazy"
            {...props}
          />
        ),
      }}
    >
      {normalized}
    </ReactMarkdown>
  );
}
