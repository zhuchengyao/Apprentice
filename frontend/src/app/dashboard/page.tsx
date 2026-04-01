import Link from "next/link";
import { ArrowLeft, Construction } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function DashboardPage() {
  return (
    <div className="mx-auto max-w-7xl px-6 py-8">
      <Link href="/library">
        <Button variant="ghost" size="sm" className="gap-1.5 mb-6">
          <ArrowLeft className="h-4 w-4" />
          Back to library
        </Button>
      </Link>

      <div className="flex flex-col items-center justify-center py-24">
        <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-muted">
          <Construction className="h-10 w-10 text-muted-foreground" />
        </div>
        <h2 className="mt-6 text-xl font-semibold">Progress Dashboard</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Streaks, mastery charts, and review schedule coming in Phase 4
        </p>
      </div>
    </div>
  );
}
