"use client";

import { useTranslations } from "next-intl";
import { MessageSquare } from "lucide-react";

interface Conversation {
  id: string;
  book_title: string;
  chapter_title: string;
  message_count: number;
  updated_at: string | null;
}

interface RecentConversationsProps {
  conversations: Conversation[];
}

export function RecentConversations({
  conversations,
}: RecentConversationsProps) {
  const t = useTranslations("dashboard.conversations");

  const formatRelativeTime = (iso: string): string => {
    const date = new Date(iso);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    if (diffMins < 1) return t("just_now");
    if (diffMins < 60) return t("minutes_ago", { count: diffMins });
    const diffHrs = Math.floor(diffMins / 60);
    if (diffHrs < 24) return t("hours_ago", { count: diffHrs });
    const diffDays = Math.floor(diffHrs / 24);
    if (diffDays < 7) return t("days_ago", { count: diffDays });
    return date.toLocaleDateString();
  };

  return (
    <div className="rounded-2xl bg-card ring-1 ring-border/60">
      <div className="border-b border-border/60 px-5 py-4">
        <p className="eyebrow">{t("eyebrow")}</p>
        <h2 className="mt-1 font-heading text-base font-semibold tracking-tight">
          {t("heading")}
        </h2>
      </div>

      {conversations.length === 0 ? (
        <div className="flex flex-col items-center justify-center gap-3 p-10 text-center">
          <MessageSquare className="h-6 w-6 text-muted-foreground/50" />
          <p className="text-[13px] text-muted-foreground">{t("empty")}</p>
        </div>
      ) : (
        <ul className="divide-y divide-border/50">
          {conversations.map((c) => (
            <li
              key={c.id}
              className="flex items-start gap-3 px-5 py-3.5 transition-colors hover:bg-subtle/50"
            >
              <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary/10 ring-1 ring-primary/15">
                <MessageSquare className="h-3.5 w-3.5 text-primary" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="truncate font-heading text-[13.5px] font-medium">
                  {c.chapter_title}
                </p>
                <p className="mt-0.5 truncate font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground">
                  {c.book_title}
                </p>
              </div>
              <div className="shrink-0 text-right">
                <p className="font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground tabular-nums">
                  {t("messages_short", { count: c.message_count })}
                </p>
                {c.updated_at && (
                  <p className="mt-0.5 font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground/70">
                    {formatRelativeTime(c.updated_at)}
                  </p>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
