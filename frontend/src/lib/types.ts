import type { BookStatus } from "./constants";

export interface Book {
  id: string;
  title: string;
  author: string;
  cover_url: string | null;
  file_type: string;
  total_pages: number;
  status: BookStatus;
  progress: number;
  total_knowledge_points: number;
  mastered_knowledge_points: number;
  created_at: string;
  updated_at: string;
}

export interface BookDetail extends Book {
  chapters: Chapter[];
}

export interface Chapter {
  id: string;
  book_id: string;
  title: string;
  order_index: number;
  start_page: number;
  end_page: number;
  processed: boolean;
  summary: string | null;
  sections: Section[];
  progress: number;
}

export interface Section {
  id: string;
  chapter_id: string;
  title: string;
  order_index: number;
  summary: string | null;
  knowledge_points: KnowledgePoint[];
  progress: number;
}

export interface KnowledgePoint {
  id: string;
  section_id: string;
  concept: string;
  explanation: string;
  difficulty: number;
  order_index: number;
  mastery_level: number;
}

export interface BookPage {
  page_number: number;
  html_content: string;
}

export interface BookPagesResponse {
  book_id: string;
  total_pages: number;
  pages: BookPage[];
}

export interface ChapterProgress {
  chapter_id: string;
  processed: boolean;
  pages_done: number;
  pages_total: number;
}

export interface ProgressOverview {
  total_books: number;
  total_kps: number;
  mastered_kps: number;
  current_streak: number;
  longest_streak: number;
  total_study_minutes: number;
  due_reviews: number;
}

// ── Billing types ──────────────────────────────────────────

export type SubscriptionStatus = "active" | "canceled" | "past_due";

export type TransactionType =
  | "signup_bonus"
  | "subscription_refill"
  | "topup_purchase"
  | "ai_usage"
  | "admin_adjustment";

export type UserRole = "user" | "admin";

export interface SubscriptionPlan {
  id: string;
  name: string;
  display_name: string;
  monthly_credits: number;
  price_usd: number;
  stripe_price_id: string | null;
  features: {
    max_books: number | null;
    allowed_models: string[] | null;
    priority_processing: boolean;
  };
}

export interface UserSubscription {
  id: string;
  status: SubscriptionStatus;
  cancel_at_period_end: boolean;
  current_period_start: string;
  current_period_end: string;
  plan: SubscriptionPlan | null;
}

export interface CreditTransaction {
  id: string;
  amount: number;
  balance_after: number;
  transaction_type: TransactionType;
  description: string | null;
  created_at: string;
}

export interface CreditPack {
  credits: number;
  price_usd: number;
  label: string;
}

export interface UsageDailyEntry {
  date: string;
  cost_usd: number;
  credits_used: number;
  calls: number;
}

export interface UsageBreakdown {
  caller: string;
  calls: number;
  input_tokens: number;
  output_tokens: number;
  cost_usd: number;
  credits_used: number;
}
