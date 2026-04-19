"use client";

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { useLocale } from "next-intl";
import { cn } from "@/lib/utils";

function slugify(text: string): string {
  return text
    .toLowerCase()
    .trim()
    .replace(/[^\w\u4e00-\u9fa5\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/^-+|-+$/g, "");
}

interface TocItem {
  id: string;
  text: string;
}

export function LegalToc() {
  const pathname = usePathname();
  const lang = useLocale();
  const [items, setItems] = useState<TocItem[]>([]);
  const [active, setActive] = useState<string | null>(null);

  useEffect(() => {
    const raf = requestAnimationFrame(() => {
      const headings = document.querySelectorAll<HTMLHeadingElement>(
        "article h2",
      );
      const seen = new Set<string>();
      const next: TocItem[] = [];
      headings.forEach((h) => {
        const text = (h.textContent ?? "").trim();
        if (!text) return;
        let slug = slugify(text);
        if (!slug) slug = `section-${next.length + 1}`;
        let unique = slug;
        let i = 2;
        while (seen.has(unique)) {
          unique = `${slug}-${i++}`;
        }
        seen.add(unique);
        h.id = unique;
        next.push({ id: unique, text });
      });
      setItems(next);
    });
    return () => cancelAnimationFrame(raf);
  }, [pathname, lang]);

  useEffect(() => {
    if (items.length === 0) return;
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => a.target.getBoundingClientRect().top - b.target.getBoundingClientRect().top);
        if (visible.length > 0) {
          setActive(visible[0].target.id);
        }
      },
      { rootMargin: "-96px 0px -70% 0px" },
    );
    items.forEach(({ id }) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });
    return () => observer.disconnect();
  }, [items]);

  if (items.length === 0) return null;

  return (
    <nav aria-label="On this page" className="text-sm">
      <p className="mb-3 text-xs font-semibold uppercase tracking-[0.18em] text-muted-foreground">
        {lang === "zh" ? "目录" : "On this page"}
      </p>
      <ul className="border-l">
        {items.map(({ id, text }) => {
          const isActive = active === id;
          return (
            <li key={id}>
              <a
                href={`#${id}`}
                className={cn(
                  "block -ml-px border-l py-1.5 pl-4 transition-colors",
                  isActive
                    ? "border-foreground text-foreground font-medium"
                    : "border-transparent text-muted-foreground hover:border-border hover:text-foreground",
                )}
              >
                {text}
              </a>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
