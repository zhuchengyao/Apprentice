"use client";

import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import Link from "next/link";
import { useTranslations } from "next-intl";
import {
  LayoutDashboard,
  Users,
  ScrollText,
  LogOut,
  Loader2,
  Shield,
} from "lucide-react";
import { cn } from "@/lib/utils";

type AdminProfile = {
  id: string;
  email: string;
  name: string;
  role: string;
};

const NAV_ITEMS = [
  { href: "/admin", key: "dashboard", icon: LayoutDashboard, exact: true },
  { href: "/admin/users", key: "users", icon: Users, exact: false },
  { href: "/admin/audit", key: "audit", icon: ScrollText, exact: false },
] as const;

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const router = useRouter();
  const t = useTranslations("admin");
  const tNav = useTranslations("admin.nav");
  const isLogin = pathname === "/admin/login";

  const [admin, setAdmin] = useState<AdminProfile | null>(null);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    if (isLogin) {
      setChecking(false);
      return;
    }
    let cancelled = false;
    (async () => {
      try {
        const res = await fetch("/api/admin/auth/me");
        if (!res.ok) {
          if (!cancelled) router.replace("/admin/login");
          return;
        }
        const data = await res.json();
        if (!cancelled) {
          if (!data.admin) {
            router.replace("/admin/login");
          } else {
            setAdmin(data.admin);
          }
        }
      } catch {
        if (!cancelled) router.replace("/admin/login");
      } finally {
        if (!cancelled) setChecking(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [isLogin, pathname, router]);

  async function handleLogout() {
    await fetch("/api/auth/logout", { method: "POST" });
    router.replace("/admin/login");
  }

  if (isLogin) {
    return <>{children}</>;
  }

  if (checking || !admin) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-background text-foreground">
      <aside className="flex w-60 shrink-0 flex-col border-r border-border/60 bg-card">
        <div className="flex items-center gap-2.5 border-b border-border/60 px-5 py-4">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary/10 text-primary ring-1 ring-primary/20">
            <Shield className="h-4 w-4" />
          </div>
          <div>
            <div className="font-display text-sm font-semibold tracking-tight">
              {t("console")}
            </div>
            <div className="font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground">
              Apprentice
            </div>
          </div>
        </div>

        <nav className="flex-1 space-y-0.5 p-3">
          {NAV_ITEMS.map((item) => {
            const active = item.exact
              ? pathname === item.href
              : pathname.startsWith(item.href);
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-2.5 rounded-xl px-3 py-2 text-[13.5px] transition-colors",
                  active
                    ? "bg-primary/8 text-foreground ring-1 ring-primary/15"
                    : "text-muted-foreground hover:bg-subtle hover:text-foreground",
                )}
              >
                <Icon className="h-4 w-4" />
                {tNav(item.key)}
              </Link>
            );
          })}
        </nav>

        <div className="border-t border-border/60 p-3">
          <div className="mb-2 px-2">
            <div className="truncate text-[12.5px] font-medium">
              {admin.name}
            </div>
            <div className="truncate text-xs text-muted-foreground">
              {admin.email}
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="flex w-full items-center gap-2.5 rounded-xl px-3 py-2 text-[13.5px] text-muted-foreground transition-colors hover:bg-subtle hover:text-foreground"
          >
            <LogOut className="h-4 w-4" />
            {t("sign_out")}
          </button>
        </div>
      </aside>

      <main className="flex-1 overflow-y-auto">{children}</main>
    </div>
  );
}
