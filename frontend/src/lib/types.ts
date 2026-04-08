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

export interface StudySession {
  id: string;
  book_id: string;
  section_id: string;
  current_kp_index: number;
  state: "idle" | "explain" | "check" | "evaluate" | "deepen";
  knowledge_points: KnowledgePointDetail[];
}

export interface KnowledgePointDetail {
  id: string;
  concept: string;
  explanation: string;
  difficulty: number;
  mastered?: boolean;
  illustration?: string;
  question?: string;
  image_urls?: string[];
}

export type KPCardStatus =
  | "pending"
  | "illustrating"
  | "checking"
  | "answering"
  | "evaluating"
  | "deepening"
  | "completed";

export interface KPCardState {
  status: KPCardStatus;
  illustration: string;
  question: string;
  userAnswer: string;
  feedback: { quality: number; feedback: string } | null;
  deepenText: string;
  secondQuestion: string;
  secondAnswer: string;
  secondFeedback: { quality: number; feedback: string } | null;
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
