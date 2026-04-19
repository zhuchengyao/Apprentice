"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import { Shield, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function AdminLoginPage() {
  const router = useRouter();
  const t = useTranslations("admin.login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await fetch("/api/admin/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        setError(data.detail || t("failed"));
        return;
      }
      router.push("/admin");
    } catch {
      setError(t("generic_error"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center bg-background px-4">
      <div className="aurora absolute inset-0 opacity-40" aria-hidden="true" />
      <div className="relative w-full max-w-sm">
        <div className="rounded-3xl bg-card p-8 ring-1 ring-border/60 shadow-editorial-lg">
          <div className="flex flex-col items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/10 text-primary ring-1 ring-primary/20">
              <Shield className="h-5 w-5" />
            </div>
            <h1 className="font-display text-2xl font-semibold tracking-tight">
              {t("title")}
            </h1>
            <p className="text-center text-[13.5px] leading-relaxed text-muted-foreground">
              {t("lede")}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="mt-7 space-y-4">
            <div className="space-y-1.5">
              <label
                htmlFor="email"
                className="font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground"
              >
                {t("email")}
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full rounded-xl bg-background px-3.5 py-2.5 text-sm ring-1 ring-border/60 outline-none transition-colors focus:ring-2 focus:ring-primary/30"
                placeholder={t("email_placeholder")}
              />
            </div>

            <div className="space-y-1.5">
              <label
                htmlFor="password"
                className="font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground"
              >
                {t("password")}
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full rounded-xl bg-background px-3.5 py-2.5 text-sm ring-1 ring-border/60 outline-none transition-colors focus:ring-2 focus:ring-primary/30"
                placeholder={t("password_placeholder")}
              />
            </div>

            {error && (
              <p className="rounded-xl bg-destructive/8 px-3.5 py-2.5 text-[13px] text-destructive ring-1 ring-destructive/20">
                {error}
              </p>
            )}

            <Button
              type="submit"
              variant="primary"
              className="w-full gap-2 rounded-full"
              disabled={loading}
            >
              {loading && <Loader2 className="h-4 w-4 animate-spin" />}
              {t("submit")}
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
