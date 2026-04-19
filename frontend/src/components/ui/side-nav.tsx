"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTranslations } from "next-intl";
import {
  Clapperboard,
  Coins,
  CreditCard,
  LayoutDashboard,
  Library,
  LogOut,
  Menu,
  Plus,
  Settings,
  Sparkles,
  User,
  X,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/ui/theme-toggle";
import { LanguageToggle } from "@/components/ui/language-toggle";
import { useAuthStore } from "@/stores/auth-store";
import { useBillingStore } from "@/stores/billing-store";
import { UploadDialog } from "@/components/upload/upload-dialog";
import { api } from "@/lib/api-client";
import type { Book } from "@/lib/types";

function Avatar({
  url,
  name,
  size = 32,
}: {
  url: string | null;
  name: string;
  size?: number;
}) {
  const [failed, setFailed] = useState(false);
  const initials = name
    .split(" ")
    .map((p) => p[0])
    .filter(Boolean)
    .slice(0, 2)
    .join("")
    .toUpperCase();

  if (!url || failed) {
    return (
      <div
        className="flex shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-primary/25 to-primary/10 text-[11px] font-semibold text-primary ring-1 ring-primary/20"
        style={{ width: size, height: size }}
        aria-label={name}
      >
        {initials || <User className="h-3.5 w-3.5" />}
      </div>
    );
  }
  return (
    /* eslint-disable-next-line @next/next/no-img-element */
    <img
      src={url}
      alt={name}
      style={{ width: size, height: size }}
      className="shrink-0 rounded-full object-cover ring-1 ring-border"
      onError={() => setFailed(true)}
    />
  );
}

const primaryNavConfig = [
  { href: "/library", key: "library", icon: Library },
  { href: "/dashboard", key: "progress", icon: LayoutDashboard },
  { href: "/billing", key: "billing", icon: CreditCard },
] as const;

export function SideNav() {
  const pathname = usePathname();
  const t = useTranslations("nav");
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const balance = useBillingStore((s) => s.balance);
  const fetchBalance = useBillingStore((s) => s.fetchBalance);

  const [uploadOpen, setUploadOpen] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [books, setBooks] = useState<Book[]>([]);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (user) fetchBalance();
  }, [user, fetchBalance]);

  const refreshBooks = useCallback(() => {
    if (!user) return;
    api
      .get<{ books: Book[] }>("/books")
      .then((d) => setBooks(d.books))
      .catch(() => {});
  }, [user]);

  useEffect(() => {
    refreshBooks();
  }, [refreshBooks]);

  useEffect(() => {
    function onClick(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuOpen(false);
      }
    }
    if (menuOpen) document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, [menuOpen]);

  useEffect(() => {
    setMobileOpen(false);
    setMenuOpen(false);
  }, [pathname]);

  const recent = books
    .slice()
    .sort(
      (a, b) =>
        new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime(),
    )
    .slice(0, 8);

  const nav = (
    <div className="flex h-full flex-col">
      {/* Brand */}
      <div className="flex items-center gap-2.5 px-5 pt-5 pb-5">
        <Link
          href="/library"
          className="flex items-center gap-2.5 transition-opacity hover:opacity-90"
        >
          <div className="relative flex h-8 w-8 items-center justify-center rounded-lg bg-foreground text-background">
            <Sparkles className="h-3.5 w-3.5" />
            <span className="absolute -top-0.5 -right-0.5 h-2 w-2 rounded-full bg-primary ring-2 ring-sidebar" />
          </div>
          <span className="font-heading text-[17px] font-semibold tracking-tight">
            Apprentice
          </span>
        </Link>
        <button
          onClick={() => setMobileOpen(false)}
          className="ml-auto rounded-md p-1.5 text-muted-foreground hover:bg-sidebar-accent hover:text-foreground md:hidden"
          aria-label={t("close_menu")}
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      {/* New book CTA */}
      <div className="px-3 pb-4">
        <Button
          variant="primary"
          onClick={() => setUploadOpen(true)}
          className="w-full justify-start gap-2 rounded-xl"
          size="lg"
        >
          <Plus className="h-4 w-4" />
          <span className="font-medium">{t("new_book")}</span>
        </Button>
      </div>

      {/* Primary nav */}
      <nav className="px-2">
        {primaryNavConfig.map(({ href, key, icon: Icon }) => {
          const active =
            pathname === href || pathname.startsWith(href + "/");
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "group relative mb-0.5 flex items-center gap-3 rounded-lg px-3 py-2 text-[13.5px] transition-all",
                active
                  ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium"
                  : "text-muted-foreground hover:bg-sidebar-accent/50 hover:text-foreground",
              )}
            >
              {active && (
                <span className="absolute left-0 top-1/2 h-5 w-0.5 -translate-y-1/2 rounded-r-full bg-primary" />
              )}
              <Icon className="h-4 w-4 shrink-0" />
              <span className="truncate">{t(key)}</span>
              {href === "/billing" && balance !== null && (
                <span className="ml-auto flex items-center gap-1 font-mono text-[10px] tabular-nums text-muted-foreground">
                  <Coins className="h-3 w-3 text-primary/80" />
                  {balance.toLocaleString()}
                </span>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Recent */}
      <div className="mt-6 flex min-h-0 flex-1 flex-col px-2">
        <div className="flex items-center justify-between px-3 pb-2">
          <span className="eyebrow">{t("recent")}</span>
          <Link
            href="/library"
            className="text-[11px] text-muted-foreground/70 transition-colors hover:text-foreground"
          >
            {t("all")} →
          </Link>
        </div>
        <div className="flex-1 space-y-0.5 overflow-y-auto pr-1">
          {recent.length === 0 ? (
            <p className="px-3 py-2 text-[12px] leading-relaxed text-muted-foreground/60">
              {t("recent_empty")}
            </p>
          ) : (
            recent.map((b) => {
              const active = pathname.startsWith(`/book/${b.id}`);
              return (
                <Link
                  key={b.id}
                  href={`/book/${b.id}`}
                  className={cn(
                    "flex items-center gap-2.5 truncate rounded-lg px-3 py-1.5 text-[12.5px] transition-colors",
                    active
                      ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium"
                      : "text-muted-foreground hover:bg-sidebar-accent/50 hover:text-foreground",
                  )}
                  title={b.title}
                >
                  <span
                    className={cn(
                      "h-1.5 w-1.5 shrink-0 rounded-full",
                      active ? "bg-primary" : "bg-muted-foreground/30",
                    )}
                  />
                  <span className="truncate">{b.title}</span>
                </Link>
              );
            })
          )}
        </div>
      </div>

      {/* Theme + language */}
      <div className="flex items-center justify-between gap-2 px-4 pb-3 pt-4">
        <ThemeToggle />
        <LanguageToggle />
      </div>

      {/* Account footer */}
      {user && (
        <div className="border-t border-sidebar-border/70 p-2">
          <div ref={menuRef} className="relative">
            <button
              onClick={() => setMenuOpen((v) => !v)}
              className="flex w-full items-center gap-3 rounded-lg p-2 text-left transition-colors hover:bg-sidebar-accent/60"
            >
              <Avatar url={user.avatar_url} name={user.name} />
              <div className="min-w-0 flex-1">
                <div className="truncate text-[13px] font-medium text-foreground">
                  {user.name}
                </div>
                <div className="truncate font-mono text-[10px] text-muted-foreground">
                  {user.email}
                </div>
              </div>
            </button>
            {menuOpen && (
              <div className="absolute bottom-full left-0 right-0 z-50 mb-2 rounded-xl border border-border/70 bg-popover p-1 shadow-editorial-lg">
                <MenuItem href="/settings" icon={Settings}>
                  {t("settings")}
                </MenuItem>
                <MenuItem href="/manim-lab" icon={Clapperboard}>
                  {t("manim_lab")}
                </MenuItem>
                <div className="my-1 h-px bg-border/60" />
                <button
                  onClick={logout}
                  className="flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-[13px] text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
                >
                  <LogOut className="h-3.5 w-3.5" />
                  {t("log_out")}
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );

  return (
    <>
      {/* Mobile top bar */}
      <header className="sticky top-0 z-30 flex items-center gap-2 border-b border-sidebar-border bg-sidebar/90 px-3 py-2 backdrop-blur md:hidden">
        <button
          onClick={() => setMobileOpen(true)}
          className="rounded-md p-1.5 text-muted-foreground hover:bg-sidebar-accent hover:text-foreground"
          aria-label={t("open_menu")}
        >
          <Menu className="h-5 w-5" />
        </button>
        <Link href="/library" className="flex items-center gap-2">
          <div className="flex h-6 w-6 items-center justify-center rounded-md bg-foreground text-background">
            <Sparkles className="h-3 w-3" />
          </div>
          <span className="font-heading text-sm font-semibold">
            Apprentice
          </span>
        </Link>
      </header>

      {/* Desktop sidebar */}
      <aside className="sticky top-0 hidden h-screen w-[264px] shrink-0 flex-col border-r border-sidebar-border/80 bg-sidebar md:flex">
        {nav}
      </aside>

      {/* Mobile drawer */}
      {mobileOpen && (
        <>
          <div
            className="fixed inset-0 z-40 bg-foreground/25 backdrop-blur-sm md:hidden"
            onClick={() => setMobileOpen(false)}
          />
          <aside className="fixed inset-y-0 left-0 z-50 flex w-[280px] flex-col border-r border-sidebar-border bg-sidebar md:hidden">
            {nav}
          </aside>
        </>
      )}

      <UploadDialog
        open={uploadOpen}
        onClose={() => {
          setUploadOpen(false);
          refreshBooks();
        }}
      />
    </>
  );
}

function MenuItem({
  href,
  icon: Icon,
  children,
}: {
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  children: React.ReactNode;
}) {
  return (
    <Link
      href={href}
      className="flex items-center gap-2.5 rounded-lg px-3 py-2 text-[13px] text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
    >
      <Icon className="h-3.5 w-3.5" />
      {children}
    </Link>
  );
}
