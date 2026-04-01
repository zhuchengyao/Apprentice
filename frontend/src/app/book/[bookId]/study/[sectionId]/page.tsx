import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { StudySessionClient } from "@/components/study/study-session-client";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

async function createSession(bookId: string, sectionId: string) {
  const res = await fetch(`${BACKEND_URL}/api/study/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ book_id: bookId, section_id: sectionId }),
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Failed to create session: ${res.status}`);
  }
  return res.json();
}

export default async function StudySessionPage({
  params,
}: {
  params: Promise<{ bookId: string; sectionId: string }>;
}) {
  const { bookId, sectionId } = await params;
  const session = await createSession(bookId, sectionId);

  return (
    <div className="mx-auto max-w-3xl px-6 py-8">
      <Link href={`/book/${bookId}`}>
        <Button variant="ghost" size="sm" className="gap-1.5 mb-4">
          <ArrowLeft className="h-4 w-4" />
          Back to book
        </Button>
      </Link>

      <StudySessionClient initialSession={session} />
    </div>
  );
}
