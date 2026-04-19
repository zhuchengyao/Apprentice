import Link from "next/link";
import { Sparkles } from "lucide-react";
import { getTranslations } from "next-intl/server";
import { LegalToc } from "@/components/legal/legal-toc";
import { ThemeToggle } from "@/components/ui/theme-toggle";
import { LanguageToggle } from "@/components/ui/language-toggle";

export default async function LegalLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const t = await getTranslations("legal");
  return (
    <div className="flex min-h-screen flex-col bg-background">
      <header className="sticky top-0 z-40 border-b border-border/60 bg-background/75 backdrop-blur-xl">
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
          <div className="flex items-center gap-4 text-[13px] text-muted-foreground">
            <Link href="/terms" className="transition-colors hover:text-foreground">
              {t("terms_title")}
            </Link>
            <Link href="/privacy" className="transition-colors hover:text-foreground">
              {t("privacy_title")}
            </Link>
            <Link href="/refund" className="transition-colors hover:text-foreground">
              {t("refund_title")}
            </Link>
            <LanguageToggle className="ml-2 hidden sm:inline-flex" />
            <ThemeToggle className="hidden sm:inline-flex" />
          </div>
        </nav>
      </header>

      <main className="mx-auto w-full max-w-6xl flex-1 px-5 py-16 sm:px-6">
        <div className="grid grid-cols-1 gap-x-16 gap-y-10 lg:grid-cols-[minmax(0,1fr)_240px]">
          <article
            className="prose prose-neutral max-w-none dark:prose-invert
              prose-headings:font-heading prose-headings:tracking-tight prose-headings:font-semibold
              prose-h2:mt-14 prose-h2:scroll-mt-24 prose-h2:text-2xl
              prose-h3:mt-8 prose-h3:text-lg
              prose-p:leading-[1.75] prose-p:text-[0.95rem]
              prose-li:leading-[1.75] prose-li:text-[0.95rem] prose-li:marker:text-muted-foreground
              prose-ul:my-4
              prose-strong:text-foreground prose-strong:font-semibold
              prose-a:text-primary prose-a:font-medium prose-a:underline-offset-4 hover:prose-a:underline
              prose-code:text-foreground prose-code:bg-subtle prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:text-[0.9em] prose-code:font-mono
              prose-code:before:content-[''] prose-code:after:content-['']"
          >
            {children}
          </article>

          <aside className="hidden lg:block">
            <div className="sticky top-24">
              <LegalToc />
            </div>
          </aside>
        </div>
      </main>

      <footer className="border-t border-border/60 py-8">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-3 px-5 text-[12px] text-muted-foreground sm:flex-row sm:px-6">
          <span className="font-mono">
            © {new Date().getFullYear()} Apprentice, Inc.
          </span>
          <div className="flex items-center gap-5">
            <Link href="/terms" className="hover:text-foreground">{t("terms_title")}</Link>
            <Link href="/privacy" className="hover:text-foreground">{t("privacy_title")}</Link>
            <Link href="/refund" className="hover:text-foreground">{t("refund_title")}</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
