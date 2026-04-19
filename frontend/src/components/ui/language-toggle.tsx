"use client";

import { useTransition } from "react";
import { useLocale, useTranslations } from "next-intl";
import { setLocale } from "@/i18n/actions";
import { locales, type Locale } from "@/i18n/config";
import { cn } from "@/lib/utils";

const labels: Record<Locale, string> = {
  en: "EN",
  zh: "中",
};

export function LanguageToggle({ className }: { className?: string }) {
  const current = useLocale() as Locale;
  const t = useTranslations("nav");
  const [pending, startTransition] = useTransition();

  return (
    <div
      role="radiogroup"
      aria-label={t("language_label")}
      className={cn(
        "inline-flex items-center gap-0.5 rounded-full bg-subtle p-0.5 ring-1 ring-border/60",
        className,
      )}
    >
      {locales.map((locale) => {
        const active = current === locale;
        return (
          <button
            key={locale}
            role="radio"
            aria-checked={active}
            disabled={pending}
            onClick={() =>
              startTransition(() => {
                void setLocale(locale);
              })
            }
            className={cn(
              "flex h-6 min-w-6 items-center justify-center rounded-full px-2 font-mono text-[10px] uppercase tracking-[0.08em] transition-colors",
              active
                ? "bg-background text-foreground shadow-sm ring-1 ring-border/70"
                : "text-muted-foreground hover:text-foreground",
              pending && "opacity-60",
            )}
          >
            {labels[locale]}
          </button>
        );
      })}
    </div>
  );
}
