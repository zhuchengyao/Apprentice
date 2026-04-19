import { create } from "zustand";
import { api } from "@/lib/api-client";
import type {
  SubscriptionPlan,
  UserSubscription,
  CreditTransaction,
} from "@/lib/types";

interface BillingState {
  balance: number | null;
  transactions: CreditTransaction[];
  subscription: UserSubscription | null;
  plans: SubscriptionPlan[];
  isLoading: boolean;
  hasFetched: boolean;
  fetchBalance: () => Promise<void>;
  fetchSubscription: () => Promise<void>;
  fetchPlans: () => Promise<void>;
  fetchAll: () => Promise<void>;
}

export const useBillingStore = create<BillingState>((set, get) => ({
  balance: null,
  transactions: [],
  subscription: null,
  plans: [],
  isLoading: false,
  hasFetched: false,

  fetchBalance: async () => {
    try {
      const data = await api.get<{
        balance: number;
        transactions: CreditTransaction[];
      }>("/billing/credits");
      set({ balance: data.balance, transactions: data.transactions });
    } catch {
      // ignore
    }
  },

  fetchSubscription: async () => {
    try {
      const data = await api.get<{ subscription: UserSubscription | null }>(
        "/billing/subscription",
      );
      set({ subscription: data.subscription });
    } catch {
      // ignore
    }
  },

  fetchPlans: async () => {
    try {
      const data = await api.get<{ plans: SubscriptionPlan[] }>(
        "/billing/plans",
      );
      set({ plans: data.plans });
    } catch {
      // ignore
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
