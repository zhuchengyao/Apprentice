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
  /** Render inline — strip block-level wrappers so the output can live inside
   *  an <h3>, <p>, <span>, etc. Useful for titles or short labels that may
   *  still contain math or other markdown. */
  inline?: boolean;
}

export function Markdown({ children, inline = false }: MarkdownProps) {
  const normalized = normalizeLatex(children);
  if (inline) {
    return (
      <ReactMarkdown
        remarkPlugins={remarkPlugins}
        rehypePlugins={rehypePlugins}
        components={{
          // Paragraphs would introduce block elements inside inline parents
          // (invalid HTML: <h3><p>…</p></h3>). Unwrap to the raw children.
          p: ({ children }) => <>{children}</>,
        }}
      >
        {normalized}
      </ReactMarkdown>
    );
  }
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
