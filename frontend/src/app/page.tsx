"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import { motion } from "framer-motion";
import {
  ArrowRight,
  BookOpen,
  Brain,
  GraduationCap,
  Sparkles,
  Quote,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/ui/theme-toggle";
import { LanguageToggle } from "@/components/ui/language-toggle";
import { useAuthStore } from "@/stores/auth-store";

const featureKeys = [
  { icon: BookOpen, id: "upload" },
  { icon: Brain, id: "extract" },
  { icon: GraduationCap, id: "teach" },
  { icon: Sparkles, id: "remember" },
] as const;

const principleKeys = [
  { index: "01", id: "one" },
  { index: "02", id: "two" },
  { index: "03", id: "three" },
] as const;

export default function LandingPage() {
  const router = useRouter();
  const user = useAuthStore((s) => s.user);
  const hasFetched = useAuthStore((s) => s.hasFetched);
  const fetchUser = useAuthStore((s) => s.fetchUser);
  const t = useTranslations("landing");

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  useEffect(() => {
    if (hasFetched && user) router.replace("/library");
  }, [hasFetched, user, router]);

  return (
    <div className="flex min-h-screen flex-col bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b border-border/60 bg-background/70 backdrop-blur-xl">
        <nav className="mx-auto flex h-14 max-w-6xl items-center justify-between px-5 sm:px-6">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="relative flex h-7 w-7 items-center justify-center rounded-lg bg-foreground text-background">
              <Sparkles className="h-3.5 w-3.5" />
              <span className="absolute -top-0.5 -right-0.5 h-1.5 w-1.5 rounded-full bg-primary ring-2 ring-background" />
            </div>
            <span className="font-heading text-[17px] font-semibold tracking-tight">
              Apprentice
            </span>
          </Link>
          <div className="flex items-center gap-2">
            <LanguageToggle className="hidden sm:inline-flex" />
            <ThemeToggle className="hidden sm:inline-flex" />
            <Link
              href="/login"
              className="rounded-lg px-3 py-1.5 text-[13px] text-muted-foreground transition-colors hover:bg-subtle hover:text-foreground"
            >
              {t("header.sign_in")}
            </Link>
            <Link href="/register">
              <Button size="sm" variant="primary" className="rounded-full">
                {t("header.get_started")}
              </Button>
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden px-5 pt-20 pb-28 sm:px-6 sm:pt-28">
        <div
          aria-hidden
          className="aurora pointer-events-none absolute inset-x-0 top-0 -z-10 h-[720px]"
        />
        <div
          aria-hidden
          className="grid-bg pointer-events-none absolute inset-0 -z-10 opacity-60 dark:opacity-30"
        />

        <div className="mx-auto max-w-3xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <span className="inline-flex items-center gap-1.5 rounded-full border border-border/70 bg-card/70 px-3 py-1 font-mono text-[10px] uppercase tracking-[0.14em] text-muted-foreground backdrop-blur">
              <Sparkles className="h-3 w-3 text-primary" />
              {t("hero.badge")}
            </span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.05 }}
            className="mt-7 font-display text-balance text-5xl font-semibold leading-[0.95] tracking-tight sm:text-7xl"
          >
            {t("hero.headline_line1")}
            <br />
            <span className="italic text-primary">{t("hero.headline_line2")}</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.15 }}
            className="mx-auto mt-7 max-w-xl text-pretty text-[17px] leading-relaxed text-muted-foreground sm:text-lg"
          >
            {t("hero.lede")}
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.25 }}
            className="mt-10 flex flex-wrap items-center justify-center gap-3"
          >
            <Link href="/register">
              <Button
                size="xl"
                variant="primary"
                className="gap-2 rounded-full px-6"
              >
                {t("hero.cta_primary")}
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link href="/login">
              <Button size="xl" variant="ghost" className="rounded-full">
                {t("hero.cta_secondary")}
              </Button>
            </Link>
          </motion.div>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.6 }}
            className="mt-5 font-mono text-[11px] uppercase tracking-[0.14em] text-muted-foreground/70"
          >
            {t("hero.cta_note")}
          </motion.p>
        </div>

        {/* Feature grid */}
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.35, duration: 0.6 }}
          className="mx-auto mt-24 grid w-full max-w-5xl grid-cols-1 gap-px overflow-hidden rounded-2xl bg-border/60 ring-1 ring-border/60 sm:grid-cols-2 lg:grid-cols-4"
        >
          {featureKeys.map((feature, i) => (
            <motion.div
              key={feature.id}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.45 + i * 0.06, duration: 0.4 }}
              className="group flex flex-col gap-3 bg-card p-6 transition-colors hover:bg-card/80"
            >
              <div className="flex items-center justify-between">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10 text-primary ring-1 ring-primary/15 transition-all group-hover:bg-primary/15">
                  <feature.icon className="h-4 w-4" />
                </div>
                <span className="font-mono text-[10px] tabular-nums text-muted-foreground/50">
                  0{i + 1}
                </span>
              </div>
              <h3 className="font-heading text-[15px] font-semibold leading-tight">
                {t(`features.${feature.id}_title`)}
              </h3>
              <p className="text-[13px] leading-relaxed text-muted-foreground">
                {t(`features.${feature.id}_body`)}
              </p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* Principles */}
      <section className="border-y border-border/50 bg-subtle/40 px-5 py-24 sm:px-6 sm:py-32">
        <div className="mx-auto max-w-5xl">
          <div className="max-w-2xl">
            <span className="eyebrow">{t("philosophy.eyebrow")}</span>
            <h2 className="mt-3 font-display text-balance text-4xl font-semibold tracking-tight sm:text-5xl">
              {t("philosophy.heading_line1")}
              <br />
              <span className="italic text-primary">{t("philosophy.heading_line2")}</span>
            </h2>
          </div>

          <div className="mt-16 grid gap-12 md:grid-cols-3">
            {principleKeys.map((p) => (
              <article key={p.index} className="relative">
                <div className="flex items-center gap-3">
                  <span className="font-mono text-[11px] tabular-nums text-primary">
                    {p.index}
                  </span>
                  <span className="h-px flex-1 bg-border" />
                </div>
                <h3 className="mt-5 font-heading text-xl font-semibold tracking-tight">
                  {t(`philosophy.${p.id}_title`)}
                </h3>
                <p className="mt-3 text-[14px] leading-relaxed text-muted-foreground">
                  {t(`philosophy.${p.id}_body`)}
                </p>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* Pull quote */}
      <section className="px-5 py-24 sm:px-6 sm:py-32">
        <figure className="mx-auto max-w-3xl text-center">
          <Quote className="mx-auto h-8 w-8 text-primary/40" />
          <blockquote className="mt-6 font-display text-balance text-3xl font-medium italic leading-tight tracking-tight text-foreground sm:text-4xl">
            {t("quote.body")}
          </blockquote>
          <figcaption className="mt-6 font-mono text-[11px] uppercase tracking-[0.14em] text-muted-foreground">
            {t("quote.attr")}
          </figcaption>
        </figure>
      </section>

      {/* CTA */}
      <section className="relative overflow-hidden border-t border-border/60 px-5 py-20 sm:px-6">
        <div
          aria-hidden
          className="aurora pointer-events-none absolute inset-0 -z-10 opacity-70"
        />
        <div className="mx-auto flex max-w-3xl flex-col items-center text-center">
          <h2 className="font-display text-4xl font-semibold tracking-tight sm:text-5xl">
            {t("final.heading_line1")}
            <br />
            <span className="italic text-primary">{t("final.heading_line2")}</span>
          </h2>
          <p className="mt-5 max-w-lg text-[15px] leading-relaxed text-muted-foreground">
            {t("final.body")}
          </p>
          <Link href="/register" className="mt-8">
            <Button variant="primary" size="xl" className="gap-2 rounded-full px-7">
              {t("final.cta")}
              <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/60 py-8">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-5 text-[12px] text-muted-foreground sm:flex-row sm:px-6">
          <div className="flex items-center gap-2">
            <div className="flex h-5 w-5 items-center justify-center rounded bg-foreground text-background">
              <Sparkles className="h-3 w-3" />
            </div>
            <span className="font-mono">
              {t("footer.copyright", { year: new Date().getFullYear() })}
            </span>
          </div>
          <div className="flex items-center gap-5">
            <Link href="/terms" className="hover:text-foreground">
              {t("footer.terms")}
            </Link>
            <Link href="/privacy" className="hover:text-foreground">
              {t("footer.privacy")}
            </Link>
            <Link href="/refund" className="hover:text-foreground">
              {t("footer.refunds")}
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
