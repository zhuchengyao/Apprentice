"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTranslations } from "next-intl";
import {
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

function Avatar({ url, name }: { url: string | null; name: string }) {
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
        className="flex h-7 w-7 items-center justify-center rounded-full bg-gradient-to-br from-primary/25 to-primary/10 text-[10px] font-semibold text-primary ring-1 ring-primary/20"
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
      className="h-7 w-7 rounded-full object-cover ring-1 ring-border"
      onError={() => setFailed(true)}
    />
  );
}

const primaryNavConfig = [
  { href: "/library", key: "library", icon: Library },
  { href: "/dashboard", key: "progress", icon: LayoutDashboard },
] as const;

export function NavBar() {
  const pathname = usePathname();
  const t = useTranslations("nav");
  const user = useAuthStore((s) => s.user);
  const hasFetched = useAuthStore((s) => s.hasFetched);
  const logout = useAuthStore((s) => s.logout);
  const balance = useBillingStore((s) => s.balance);
  const fetchBalance = useBillingStore((s) => s.fetchBalance);

  const [uploadOpen, setUploadOpen] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (user) fetchBalance();
  }, [user, fetchBalance]);

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
    setMenuOpen(false);
    setMobileOpen(false);
  }, [pathname]);

  const homeHref = user ? "/library" : "/";

  return (
    <>
      <header className="sticky top-0 z-40 border-b border-border/60 bg-background/75 backdrop-blur-xl">
        <nav className="mx-auto flex h-14 max-w-6xl items-center gap-4 px-5 sm:px-6">
          <Link
            href={homeHref}
            className="flex items-center gap-2.5 transition-opacity hover:opacity-90"
          >
            <div className="relative flex h-7 w-7 items-center justify-center rounded-lg bg-foreground text-background">
              <Sparkles className="h-3.5 w-3.5" />
              <span className="absolute -top-0.5 -right-0.5 h-1.5 w-1.5 rounded-full bg-primary ring-2 ring-background" />
            </div>
            <span className="font-heading text-[17px] font-semibold tracking-tight">
              Apprentice
            </span>
          </Link>

          {user && (
            <div className="ml-3 hidden items-center gap-1 md:flex">
              {primaryNavConfig.map(({ href, key, icon: Icon }) => {
                const active =
                  pathname === href || pathname.startsWith(href + "/");
                return (
                  <Link
                    key={href}
                    href={href}
                    className={cn(
                      "flex items-center gap-2 rounded-lg px-3 py-1.5 text-[13px] font-medium transition-colors",
                      active
                        ? "bg-subtle text-foreground"
                        : "text-muted-foreground hover:bg-subtle/60 hover:text-foreground",
                    )}
                  >
                    <Icon className="h-3.5 w-3.5" />
                    {t(key)}
                  </Link>
                );
              })}
            </div>
          )}

          <div className="flex-1" />

          <LanguageToggle className="hidden sm:inline-flex" />
          <ThemeToggle className="hidden sm:inline-flex" />

          {hasFetched && !user && (
            <div className="flex items-center gap-1">
              <Link
                href="/login"
                className="rounded-lg px-3 py-1.5 text-[13px] text-muted-foreground transition-colors hover:bg-subtle hover:text-foreground"
              >
                {t("sign_in")}
              </Link>
              <Link href="/register">
                <Button size="sm" variant="primary" className="rounded-full">
                  {t("get_started")}
                </Button>
              </Link>
            </div>
          )}

          {user && (
            <>
              <Button
                size="sm"
                variant="primary"
                onClick={() => setUploadOpen(true)}
                className="hidden gap-1.5 rounded-full sm:inline-flex"
              >
                <Plus className="h-3.5 w-3.5" />
                {t("upload")}
              </Button>

              <Link
                href="/billing"
                className={cn(
                  "hidden items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-[12px] font-mono transition-colors sm:flex",
                  pathname.startsWith("/billing")
                    ? "bg-subtle text-foreground"
                    : "text-muted-foreground hover:bg-subtle hover:text-foreground",
                )}
                title={t("credits_title")}
              >
                <Coins className="h-3.5 w-3.5 text-primary/80" />
                <span className="tabular-nums">
                  {balance !== null ? balance.toLocaleString() : "—"}
                </span>
              </Link>

              <div ref={menuRef} className="relative">
                <button
                  onClick={() => setMenuOpen((v) => !v)}
                  aria-label={t("account_menu")}
                  className="flex items-center gap-2 rounded-full p-0.5 transition-colors hover:bg-subtle"
                >
                  <Avatar url={user.avatar_url} name={user.name} />
                </button>
                {menuOpen && (
                  <div className="absolute right-0 top-full z-50 mt-2 w-60 rounded-xl border border-border/70 bg-popover p-1 shadow-editorial-lg">
                    <div className="mb-1 border-b border-border/60 px-3 py-2.5">
                      <div className="truncate text-sm font-medium">
                        {user.name}
                      </div>
                      <div className="truncate font-mono text-[10px] text-muted-foreground">
                        {user.email}
                      </div>
                    </div>
                    <MenuLink href="/dashboard" icon={LayoutDashboard}>
                      {t("progress")}
                    </MenuLink>
                    <MenuLink href="/billing" icon={CreditCard}>
                      {t("billing")}
                    </MenuLink>
                    <MenuLink href="/settings" icon={Settings}>
                      {t("settings")}
                    </MenuLink>
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

              <button
                className="rounded-lg p-2 text-muted-foreground hover:bg-subtle hover:text-foreground md:hidden"
                onClick={() => setMobileOpen((v) => !v)}
                aria-label={t("open_menu")}
              >
                {mobileOpen ? (
                  <X className="h-5 w-5" />
                ) : (
                  <Menu className="h-5 w-5" />
                )}
              </button>
            </>
          )}
        </nav>

        {user && mobileOpen && (
          <div className="space-y-0.5 border-t border-border/60 bg-background px-3 py-3 md:hidden">
            {primaryNavConfig.map(({ href, key, icon: Icon }) => (
              <Link
                key={href}
                href={href}
                className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-muted-foreground hover:bg-subtle hover:text-foreground"
              >
                <Icon className="h-4 w-4" />
                {t(key)}
              </Link>
            ))}
            <button
              onClick={() => {
                setUploadOpen(true);
                setMobileOpen(false);
              }}
              className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-muted-foreground hover:bg-subtle hover:text-foreground"
            >
              <Plus className="h-4 w-4" />
              {t("upload")}
            </button>
            <Link
              href="/billing"
              className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-muted-foreground hover:bg-subtle hover:text-foreground"
            >
              <Coins className="h-4 w-4 text-primary/80" />
              {t("credits_title")} · {balance !== null ? balance.toLocaleString() : "—"}
            </Link>
          </div>
        )}
      </header>

      <UploadDialog open={uploadOpen} onClose={() => setUploadOpen(false)} />
    </>
  );
}

function MenuLink({
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
