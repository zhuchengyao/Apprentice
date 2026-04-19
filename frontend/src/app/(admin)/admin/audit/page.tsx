"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

type AuditEntry = {
  id: string;
  action: string;
  actor: { id: string; email: string | null };
  target: { id: string; email: string | null } | null;
  details: Record<string, unknown> | null;
  reason: string | null;
  created_at: string | null;
};

type AuditResponse = {
  total: number;
  limit: number;
  offset: number;
  logs: AuditEntry[];
};

const PAGE_SIZE = 100;

export default function AdminAuditPage() {
  const t = useTranslations("admin.audit");
  const tUsers = useTranslations("admin.users");
  const [data, setData] = useState<AuditResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    const params = new URLSearchParams({
      limit: PAGE_SIZE.toString(),
      offset: offset.toString(),
    });

    fetch(`/api/admin/audit?${params.toString()}`)
      .then(async (res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((d) => {
        if (!cancelled) setData(d);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [offset]);

  const total = data?.total ?? 0;
  const maxOffset = Math.max(0, total - PAGE_SIZE);

  return (
    <div className="space-y-6 p-8">
      <header>
        <h1 className="font-display text-3xl font-semibold tracking-tight">
          {t("heading")}
        </h1>
        <p className="mt-1 text-[13.5px] text-muted-foreground">{t("lede")}</p>
      </header>

      <div className="overflow-hidden rounded-2xl bg-card ring-1 ring-border/60">
        {loading ? (
          <div className="flex justify-center py-16">
            <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
          </div>
        ) : error ? (
          <div className="p-8 text-sm text-destructive">{error}</div>
        ) : !data || data.logs.length === 0 ? (
          <div className="p-12 text-center text-sm text-muted-foreground">
            {t("empty")}
          </div>
        ) : (
          <table className="w-full text-sm">
            <thead className="border-b border-border/60">
              <tr>
                {(
                  [
                    "col_when",
                    "col_actor",
                    "col_action",
                    "col_target",
                    "col_details",
                    "col_reason",
                  ] as const
                ).map((key) => (
                  <th
                    key={key}
                    className={cn(
                      "px-4 py-3 text-left font-mono text-[10px] font-normal uppercase tracking-[0.1em] text-muted-foreground",
                    )}
                  >
                    {t(key)}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.logs.map((e) => (
                <tr
                  key={e.id}
                  className="border-b border-border/40 last:border-b-0"
                >
                  <td className="px-4 py-3 text-xs whitespace-nowrap text-muted-foreground">
                    {e.created_at
                      ? new Date(e.created_at).toLocaleString()
                      : "—"}
                  </td>
                  <td className="px-4 py-3 text-xs text-muted-foreground">
                    {e.actor.email || e.actor.id.slice(0, 8)}
                  </td>
                  <td className="px-4 py-3">
                    <span className="rounded-full bg-subtle px-2.5 py-0.5 font-mono text-[10px] uppercase tracking-[0.08em] ring-1 ring-border/60">
                      {e.action}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-xs">
                    {e.target ? (
                      <Link
                        href={`/admin/users/${e.target.id}`}
                        className="hover:underline"
                      >
                        {e.target.email || e.target.id.slice(0, 8)}
                      </Link>
                    ) : (
                      <span className="text-muted-foreground/60">—</span>
                    )}
                  </td>
                  <td className="max-w-xs truncate px-4 py-3 font-mono text-xs text-muted-foreground">
                    {e.details ? JSON.stringify(e.details) : "—"}
                  </td>
                  <td className="max-w-xs truncate px-4 py-3 text-xs text-muted-foreground">
                    {e.reason || "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {total > PAGE_SIZE && (
        <div className="flex items-center justify-between text-sm text-muted-foreground">
          <span>
            {tUsers("showing", {
              from: offset + 1,
              to: Math.min(offset + PAGE_SIZE, total),
              total,
            })}
          </span>
          <div className="flex gap-2">
            <button
              onClick={() => setOffset(Math.max(0, offset - PAGE_SIZE))}
              disabled={offset === 0}
              className="rounded-full bg-card px-3.5 py-1.5 ring-1 ring-border/60 transition-colors hover:ring-border disabled:opacity-40"
            >
              {tUsers("prev")}
            </button>
            <button
              onClick={() => setOffset(Math.min(maxOffset, offset + PAGE_SIZE))}
              disabled={offset >= maxOffset}
              className="rounded-full bg-card px-3.5 py-1.5 ring-1 ring-border/60 transition-colors hover:ring-border disabled:opacity-40"
            >
              {tUsers("next")}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
