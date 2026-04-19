"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { Search, Loader2, CheckCircle2, XCircle, Shield } from "lucide-react";
import { cn } from "@/lib/utils";

type UserRow = {
  id: string;
  email: string;
  name: string;
  role: string;
  is_active: boolean;
  auth_provider: string;
  created_at: string | null;
  balance: number;
  plan: { name: string; display_name: string } | null;
};

type ListResponse = {
  total: number;
  limit: number;
  offset: number;
  users: UserRow[];
};

const PAGE_SIZE = 50;

export default function AdminUsersPage() {
  const t = useTranslations("admin.users");
  const [query, setQuery] = useState("");
  const [debounced, setDebounced] = useState("");
  const [offset, setOffset] = useState(0);
  const [data, setData] = useState<ListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const handle = setTimeout(() => setDebounced(query), 250);
    return () => clearTimeout(handle);
  }, [query]);

  useEffect(() => {
    setOffset(0);
  }, [debounced]);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    const params = new URLSearchParams({
      limit: PAGE_SIZE.toString(),
      offset: offset.toString(),
    });
    if (debounced.trim()) params.set("q", debounced.trim());

    fetch(`/api/admin/users?${params.toString()}`)
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
  }, [debounced, offset]);

  const total = data?.total ?? 0;
  const maxOffset = Math.max(0, total - PAGE_SIZE);

  return (
    <div className="space-y-6 p-8">
      <header>
        <h1 className="font-display text-3xl font-semibold tracking-tight">
          {t("heading")}
        </h1>
        <p className="mt-1 text-[13.5px] text-muted-foreground">
          {t("count", { count: total })}
        </p>
      </header>

      <div className="flex items-center gap-3">
        <div className="relative max-w-sm flex-1">
          <Search className="absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={t("search_placeholder")}
            className="w-full rounded-full bg-card py-2 pr-3 pl-9 text-sm ring-1 ring-border/60 outline-none transition-colors focus:ring-2 focus:ring-primary/30"
          />
        </div>
      </div>

      <div className="overflow-hidden rounded-2xl bg-card ring-1 ring-border/60">
        {loading ? (
          <div className="flex justify-center py-16">
            <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
          </div>
        ) : error ? (
          <div className="p-8 text-sm text-destructive">{error}</div>
        ) : !data || data.users.length === 0 ? (
          <div className="p-12 text-center text-sm text-muted-foreground">
            {t("empty")}
          </div>
        ) : (
          <table className="w-full text-sm">
            <thead className="border-b border-border/60">
              <tr>
                {(
                  [
                    ["col_email", "left"],
                    ["col_name", "left"],
                    ["col_plan", "left"],
                    ["col_credits", "right"],
                    ["col_status", "center"],
                    ["col_joined", "left"],
                  ] as const
                ).map(([key, align]) => (
                  <th
                    key={key}
                    className={cn(
                      "px-4 py-3 font-mono text-[10px] font-normal uppercase tracking-[0.1em] text-muted-foreground",
                      align === "right" && "text-right",
                      align === "center" && "text-center",
                      align === "left" && "text-left",
                    )}
                  >
                    {t(key)}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.users.map((u) => (
                <tr
                  key={u.id}
                  className="border-b border-border/40 last:border-b-0 hover:bg-subtle/60"
                >
                  <td className="px-4 py-3">
                    <Link
                      href={`/admin/users/${u.id}`}
                      className="flex items-center gap-2 hover:underline"
                    >
                      {u.role === "admin" && (
                        <Shield className="h-3.5 w-3.5 text-primary" />
                      )}
                      {u.email}
                    </Link>
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">{u.name}</td>
                  <td className="px-4 py-3">
                    {u.plan ? (
                      <span className="rounded-full bg-subtle px-2.5 py-0.5 font-mono text-[10px] uppercase tracking-[0.08em] ring-1 ring-border/60">
                        {u.plan.display_name}
                      </span>
                    ) : (
                      <span className="text-xs text-muted-foreground/60">—</span>
                    )}
                  </td>
                  <td className="px-4 py-3 text-right tabular-nums">
                    {u.balance.toLocaleString()}
                  </td>
                  <td className="px-4 py-3 text-center">
                    {u.is_active ? (
                      <CheckCircle2 className="mx-auto h-4 w-4 text-success" />
                    ) : (
                      <XCircle className="mx-auto h-4 w-4 text-destructive" />
                    )}
                  </td>
                  <td className="px-4 py-3 text-xs text-muted-foreground">
                    {u.created_at
                      ? new Date(u.created_at).toLocaleDateString()
                      : "—"}
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
            {t("showing", {
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
              {t("prev")}
            </button>
            <button
              onClick={() => setOffset(Math.min(maxOffset, offset + PAGE_SIZE))}
              disabled={offset >= maxOffset}
              className="rounded-full bg-card px-3.5 py-1.5 ring-1 ring-border/60 transition-colors hover:ring-border disabled:opacity-40"
            >
              {t("next")}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
