import { create } from "zustand";
import { api } from "@/lib/api-client";

interface AuthUser {
  id: string;
  email: string;
  name: string;
  avatar_url: string | null;
  auth_provider: string;
  preferred_language: string;
}

interface AuthState {
  user: AuthUser | null;
  isLoading: boolean;
  hasFetched: boolean;
  fetchUser: () => Promise<void>;
  setUser: (user: AuthUser | null) => void;
  updatePreferredLanguage: (code: string) => Promise<void>;
  logout: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isLoading: false,
  hasFetched: false,

  fetchUser: async () => {
    if (get().hasFetched) return;
    set({ isLoading: true });
    try {
      const data = await api.get<{ user: AuthUser }>("/auth/me");
      set({ user: data.user, hasFetched: true });
    } catch {
      set({ user: null, hasFetched: true });
    } finally {
      set({ isLoading: false });
    }
  },

  setUser: (user) => set({ user, hasFetched: true }),

  updatePreferredLanguage: async (code) => {
    const data = await api.patch<{ user: AuthUser }>("/auth/me", {
      preferred_language: code,
    });
    set({ user: data.user });
  },

  logout: async () => {
    try {
      await api.post("/auth/logout");
    } catch {
      // best-effort: proceed with local logout even if server call fails
    }
    set({ user: null, hasFetched: false });
    window.location.href = "/login";
  },
}));
