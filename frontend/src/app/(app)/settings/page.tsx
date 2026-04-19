"use client";

import { useEffect, useState } from "react";
import { useTranslations } from "next-intl";
import { Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { LanguageToggle } from "@/components/ui/language-toggle";
import { useAuthStore } from "@/stores/auth-store";
import {
  DEFAULT_LANGUAGE,
  SUPPORTED_LANGUAGES,
  type LanguageCode,
} from "@/lib/languages";
import { cn } from "@/lib/utils";

export default function SettingsPage() {
  const t = useTranslations("settings");
  const user = useAuthStore((s) => s.user);
  const updatePreferredLanguage = useAuthStore(
    (s) => s.updatePreferredLanguage,
  );

  const [language, setLanguage] = useState<LanguageCode>(DEFAULT_LANGUAGE);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<
    { kind: "success" | "error"; text: string } | null
  >(null);

  useEffect(() => {
    if (user?.preferred_language) {
      setLanguage(user.preferred_language as LanguageCode);
    }
  }, [user?.preferred_language]);

  const dirty = !!user && language !== user.preferred_language;

  async function handleSave() {
    setSaving(true);
    setMessage(null);
    try {
      await updatePreferredLanguage(language);
      setMessage({ kind: "success", text: t("teaching_language_updated") });
    } catch (err) {
      setMessage({
        kind: "error",
        text: err instanceof Error ? err.message : t("generic_error"),
      });
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="mx-auto w-full max-w-2xl px-5 py-10 sm:px-8 sm:py-12">
      <div>
        <p className="eyebrow">{t("eyebrow")}</p>
        <h1 className="mt-3 font-display text-4xl font-semibold tracking-tight sm:text-5xl">
          {t("heading")}
        </h1>
        <p className="mt-3 max-w-xl text-[14.5px] leading-relaxed text-muted-foreground">
          {t("lede")}
        </p>
      </div>

      <section className="mt-10 rounded-2xl bg-card p-6 ring-1 ring-border/60">
        <h2 className="font-display text-xl font-semibold tracking-tight">
          {t("interface_language")}
        </h2>
        <p className="mt-1.5 text-[13.5px] leading-relaxed text-muted-foreground">
          {t("interface_language_help")}
        </p>
        <div className="mt-4">
          <LanguageToggle />
        </div>
      </section>

      <section className="mt-5 rounded-2xl bg-card p-6 ring-1 ring-border/60">
        <h2 className="font-display text-xl font-semibold tracking-tight">
          {t("teaching_language")}
        </h2>
        <p className="mt-1.5 text-[13.5px] leading-relaxed text-muted-foreground">
          {t("teaching_language_help")}
        </p>

        <div className="mt-5 space-y-2">
          <label
            htmlFor="language"
            className="font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground"
          >
            {t("teaching_language")}
          </label>
          <select
            id="language"
            value={language}
            onChange={(e) => setLanguage(e.target.value as LanguageCode)}
            className="w-full max-w-sm rounded-xl bg-background px-3.5 py-2.5 text-sm ring-1 ring-border/60 outline-none transition-colors focus:ring-2 focus:ring-primary/30"
            disabled={!user}
          >
            {SUPPORTED_LANGUAGES.map((lang) => (
              <option key={lang.code} value={lang.code}>
                {lang.label}
              </option>
            ))}
          </select>
        </div>

        {message && (
          <p
            className={cn(
              "mt-4 rounded-xl px-3.5 py-2.5 text-[13px] leading-relaxed ring-1",
              message.kind === "success"
                ? "bg-primary/8 text-primary ring-primary/20"
                : "bg-destructive/8 text-destructive ring-destructive/20",
            )}
          >
            {message.text}
          </p>
        )}

        <div className="mt-6 flex justify-end">
          <Button
            variant="primary"
            onClick={handleSave}
            disabled={!dirty || saving}
            className="gap-2 rounded-full"
          >
            {saving && <Loader2 className="h-4 w-4 animate-spin" />}
            {saving ? t("saving") : t("save")}
          </Button>
        </div>
      </section>
    </div>
  );
}
