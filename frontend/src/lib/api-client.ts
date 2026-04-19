import { defaultLocale, isLocale, LOCALE_COOKIE } from "@/i18n/config";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api";

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

async function readErrorMessage(res: Response): Promise<string> {
  // FastAPI returns {"detail": "..."} for HTTPException; prefer that when
  // present so the UI doesn't surface raw JSON to the user. Falls back to
  // the raw body for non-JSON error pages (e.g. an upstream HTML 502).
  const text = await res.text();
  if (!text) return res.statusText || `HTTP ${res.status}`;
  try {
    const parsed = JSON.parse(text) as { detail?: unknown };
    if (typeof parsed.detail === "string") return parsed.detail;
    if (Array.isArray(parsed.detail) && parsed.detail.length > 0) {
      const first = parsed.detail[0] as { msg?: unknown };
      if (typeof first.msg === "string") return first.msg;
    }
  } catch {
    // non-JSON body — fall through
  }
  return text;
}

export function getLocaleFromCookie(): string {
  if (typeof document === "undefined") return defaultLocale;
  const match = document.cookie
    .split("; ")
    .find((row) => row.startsWith(`${LOCALE_COOKIE}=`));
  const value = match?.split("=")[1];
  return isLocale(value) ? value : defaultLocale;
}

function buildHeaders(extra?: HeadersInit): HeadersInit {
  return {
    "Content-Type": "application/json",
    "Accept-Language": getLocaleFromCookie(),
    ...extra,
  };
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: buildHeaders(options?.headers),
  });
  if (!res.ok) {
    if (res.status === 402) {
      // Dispatch global event for insufficient credits
      if (typeof window !== "undefined") {
        window.dispatchEvent(new CustomEvent("insufficient-credits"));
      }
    }
    throw new ApiError(res.status, await readErrorMessage(res));
  }
  return res.json();
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body?: unknown) =>
    request<T>(path, {
      method: "POST",
      body: body === undefined ? undefined : JSON.stringify(body),
    }),
  patch: <T>(path: string, body: unknown) =>
    request<T>(path, { method: "PATCH", body: JSON.stringify(body) }),
  delete: <T>(path: string) => request<T>(path, { method: "DELETE" }),
  upload: async <T>(path: string, file: File): Promise<T> => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetch(`${API_BASE}${path}`, {
      method: "POST",
      body: formData,
      headers: { "Accept-Language": getLocaleFromCookie() },
    });
    if (!res.ok) throw new ApiError(res.status, await readErrorMessage(res));
    return res.json();
  },
};
