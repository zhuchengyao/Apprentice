import { create } from "zustand";
import { api, ApiError } from "@/lib/api-client";
import type {
  SubscriptionPlan,
  UserSubscription,
  CreditTransaction,
} from "@/lib/types";

export interface BillingErrors {
  balance: string | null;
  subscription: string | null;
  plans: string | null;
}

interface BillingState {
  balance: number | null;
  transactions: CreditTransaction[];
  subscription: UserSubscription | null;
  plans: SubscriptionPlan[];
  isLoading: boolean;
  hasFetched: boolean;
  errors: BillingErrors;
  fetchBalance: () => Promise<void>;
  fetchSubscription: () => Promise<void>;
  fetchPlans: () => Promise<void>;
  fetchAll: () => Promise<void>;
}

function describe(err: unknown): string {
  if (err instanceof ApiError) return `HTTP ${err.status}: ${err.message}`;
  if (err instanceof Error) return err.message;
  return String(err);
}

export const useBillingStore = create<BillingState>((set, get) => ({
  balance: null,
  transactions: [],
  subscription: null,
  plans: [],
  isLoading: false,
  hasFetched: false,
  errors: { balance: null, subscription: null, plans: null },

  fetchBalance: async () => {
    try {
      const data = await api.get<{
        balance: number;
        transactions: CreditTransaction[];
      }>("/billing/credits");
      set((s) => ({
        balance: data.balance,
        transactions: data.transactions,
        errors: { ...s.errors, balance: null },
      }));
    } catch (err) {
      const msg = describe(err);
      console.error("[billing] fetchBalance failed:", msg);
      set((s) => ({ errors: { ...s.errors, balance: msg } }));
    }
  },

  fetchSubscription: async () => {
    try {
      const data = await api.get<{ subscription: UserSubscription | null }>(
        "/billing/subscription",
      );
      set((s) => ({
        subscription: data.subscription,
        errors: { ...s.errors, subscription: null },
      }));
    } catch (err) {
      const msg = describe(err);
      console.error("[billing] fetchSubscription failed:", msg);
      set((s) => ({ errors: { ...s.errors, subscription: msg } }));
    }
  },

  fetchPlans: async () => {
    try {
      const data = await api.get<{ plans: SubscriptionPlan[] }>(
        "/billing/plans",
      );
      set((s) => ({
        plans: data.plans,
        errors: { ...s.errors, plans: null },
      }));
    } catch (err) {
      const msg = describe(err);
      console.error("[billing] fetchPlans failed:", msg);
      set((s) => ({ errors: { ...s.errors, plans: msg } }));
    }
  },

  fetchAll: async () => {
    if (get().isLoading) return;
    set({ isLoading: true });
    await Promise.all([
      get().fetchBalance(),
      get().fetchSubscription(),
      get().fetchPlans(),
    ]);
    set({ isLoading: false, hasFetched: true });
  },
}));
