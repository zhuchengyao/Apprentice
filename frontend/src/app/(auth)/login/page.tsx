"use client";

import { Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { Loader2, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input, Label } from "@/components/ui/input";

export default function LoginPage() {
  return (
    <Suspense fallback={null}>
      <LoginPageInner />
    </Suspense>
  );
}

function LoginPageInner() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const nextPath = searchParams.get("next");
  const t = useTranslations("auth");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || t("sign_in_failed"));
        return;
      }
      router.push(nextPath && nextPath.startsWith("/") ? nextPath : "/library");
    } catch {
      setError(t("generic_error"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthShell
      eyebrow={t("sign_in_eyebrow")}
      title={t("sign_in_title")}
      subtitle={t("sign_in_subtitle")}
    >
      <Button
        variant="outline"
        size="lg"
        className="w-full gap-2 rounded-lg"
        onClick={() => (window.location.href = "/api/auth/google")}
      >
        <GoogleIcon />
        {t("continue_with_google")}
      </Button>

      <Divider label={t("or_with_email")} />

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-1.5">
          <Label htmlFor="email">{t("email_label")}</Label>
          <Input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder={t("email_placeholder")}
          />
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="password">{t("password_label")}</Label>
          <Input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            placeholder={t("password_placeholder")}
          />
        </div>

        {error && (
          <p className="rounded-lg bg-destructive/10 px-3 py-2 text-[13px] text-destructive">
            {error}
          </p>
        )}

        <Button
          type="submit"
          variant="primary"
          size="lg"
          className="w-full rounded-lg"
          disabled={loading}
        >
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : t("sign_in_submit")}
        </Button>
      </form>

      <p className="text-center text-[13px] text-muted-foreground">
        {t("sign_in_no_account")}{" "}
        <Link
          href={
            nextPath && nextPath.startsWith("/")
              ? `/register?next=${encodeURIComponent(nextPath)}`
              : "/register"
          }
          className="font-medium text-foreground underline-offset-4 hover:underline"
        >
          {t("sign_in_create")}
        </Link>
      </p>
    </AuthShell>
  );
}

export function AuthShell({
  eyebrow,
  title,
  subtitle,
  children,
}: {
  eyebrow: string;
  title: string;
  subtitle: string;
  children: React.ReactNode;
}) {
  const t = useTranslations("auth");
  return (
    <div className="relative flex min-h-screen">
      {/* Left: editorial panel */}
      <div className="relative hidden w-1/2 overflow-hidden bg-foreground text-background lg:flex lg:flex-col lg:justify-between lg:p-12">
        <div className="aurora pointer-events-none absolute inset-0 opacity-80" />
        <Link
          href="/"
          className="relative z-10 flex items-center gap-2.5 text-background/90 transition-opacity hover:opacity-80"
        >
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-background/10 backdrop-blur">
            <Sparkles className="h-4 w-4" />
          </div>
          <span className="font-heading text-[17px] font-semibold tracking-tight">
            Apprentice
          </span>
        </Link>
        <div className="relative z-10 max-w-md">
          <p className="font-mono text-[10px] uppercase tracking-[0.14em] text-background/60">
            {t("editor_note_eyebrow")}
          </p>
          <p className="mt-4 font-display text-3xl font-medium leading-tight tracking-tight">
            {t("manifesto")}
          </p>
          <p className="mt-6 font-mono text-[10px] uppercase tracking-[0.14em] text-background/60">
            {t("manifesto_source")}
          </p>
        </div>
      </div>

      {/* Right: form */}
      <div className="flex w-full flex-col items-center justify-center px-5 py-10 sm:px-6 lg:w-1/2">
        <div className="w-full max-w-sm">
          <div className="mb-10">
            <Link
              href="/"
              className="inline-flex items-center gap-2 lg:hidden"
            >
              <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-foreground text-background">
                <Sparkles className="h-3.5 w-3.5" />
              </div>
              <span className="font-heading text-[16px] font-semibold tracking-tight">
                Apprentice
              </span>
            </Link>
            <p className="mt-10 eyebrow">{eyebrow}</p>
            <h1 className="mt-3 font-display text-4xl font-semibold tracking-tight">
              {title}
            </h1>
            <p className="mt-2 text-[14px] leading-relaxed text-muted-foreground">
              {subtitle}
            </p>
          </div>
          <div className="space-y-5">{children}</div>
        </div>
      </div>
    </div>
  );
}

function Divider({ label }: { label: string }) {
  return (
    <div className="relative">
      <div className="absolute inset-0 flex items-center">
        <div className="w-full border-t border-border/70" />
      </div>
      <div className="relative flex justify-center">
        <span className="bg-background px-3 font-mono text-[10px] uppercase tracking-[0.14em] text-muted-foreground">
          {label}
        </span>
      </div>
    </div>
  );
}

function GoogleIcon() {
  return (
    <svg className="h-4 w-4" viewBox="0 0 24 24">
      <path
        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"
        fill="#4285F4"
      />
      <path
        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
        fill="#34A853"
      />
      <path
        d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
        fill="#FBBC05"
      />
      <path
        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
        fill="#EA4335"
      />
    </svg>
  );
}
