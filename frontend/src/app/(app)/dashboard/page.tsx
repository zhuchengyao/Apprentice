"use client";

import { useEffect, useState } from "react";
import { useTranslations } from "next-intl";
import { StatCards } from "@/components/dashboard/stat-cards";
import { BookProgressList } from "@/components/dashboard/book-progress-list";
import { MasteryChart } from "@/components/dashboard/mastery-chart";
import { RecentConversations } from "@/components/dashboard/recent-conversations";
import { StreakCalendar } from "@/components/dashboard/streak-calendar";
import { api } from "@/lib/api-client";

interface DashboardData {
  books: {
    total: number;
    ready: number;
    list: Array<{
      id: string;
      title: string;
      status: string;
      total_pages: number;
      total_kps: number;
      mastered_kps: number;
      progress: number;
    }>;
  };
  knowledge_points: {
    total: number;
    mastered: number;
    progress: number;
    mastery_timeline: Array<{ date: string; points_mastered: number }>;
  };
  tutor: {
    total_conversations: number;
    total_messages: number;
    recent_conversations: Array<{
      id: string;
      book_title: string;
      chapter_title: string;
      message_count: number;
      updated_at: string | null;
    }>;
  };
  streaks: {
    current_streak: number;
    total_study_minutes: number;
    daily: Array<{
      date: string;
      minutes_studied: number;
      points_mastered: number;
    }>;
  };
}

export default function DashboardPage() {
  const t = useTranslations("dashboard");
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<DashboardData>("/progress/overview")
      .then(setData)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="mx-auto w-full max-w-6xl px-5 py-10 sm:px-8 sm:py-12">
      <div>
        <p className="eyebrow">{t("eyebrow")}</p>
        <h1 className="mt-3 font-display text-4xl font-semibold tracking-tight sm:text-5xl">
          {t("heading")}
        </h1>
        <p className="mt-3 max-w-xl text-[14.5px] leading-relaxed text-muted-foreground">
          {t("lede")}
        </p>
      </div>

      <div className="mt-10">
        {loading ? (
          <div className="space-y-5">
            <div className="grid grid-cols-2 gap-px overflow-hidden rounded-2xl bg-border/60 ring-1 ring-border/60 lg:grid-cols-4">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-28 bg-card">
                  <div className="shimmer h-full w-full" />
                </div>
              ))}
            </div>
            {[...Array(2)].map((_, i) => (
              <div
                key={i}
                className="h-56 overflow-hidden rounded-2xl ring-1 ring-border/60"
              >
                <div className="shimmer h-full w-full" />
              </div>
            ))}
          </div>
        ) : data ? (
          <div className="space-y-5">
            <StatCards
              totalBooks={data.books.total}
              totalKPs={data.knowledge_points.total}
              masteredKPs={data.knowledge_points.mastered}
              totalConversations={data.tutor.total_conversations}
              totalMessages={data.tutor.total_messages}
              currentStreak={data.streaks.current_streak}
            />

            <div className="grid gap-5 lg:grid-cols-2">
              <MasteryChart
                data={data.knowledge_points.mastery_timeline}
                totalMastered={data.knowledge_points.mastered}
                totalKPs={data.knowledge_points.total}
              />
              <StreakCalendar
                days={data.streaks.daily}
                currentStreak={data.streaks.current_streak}
                totalMinutes={data.streaks.total_study_minutes}
              />
            </div>

            <div className="grid gap-5 lg:grid-cols-2">
              <BookProgressList books={data.books.list} />
              <RecentConversations
                conversations={data.tutor.recent_conversations}
              />
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-24">
            <p className="text-sm text-muted-foreground">{t("load_failed")}</p>
          </div>
        )}
      </div>
    </div>
  );
}
