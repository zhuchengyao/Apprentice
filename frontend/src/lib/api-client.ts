import { defaultLocale, isLocale, LOCALE_COOKIE } from "@/i18n/config";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api";

class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
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
    throw new ApiError(res.status, await res.text());
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
    if (!res.ok) throw new ApiError(res.status, await res.text());
    return res.json();
  },
};
