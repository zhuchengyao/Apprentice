"use client";

import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { SideNav } from "@/components/ui/side-nav";
import { useAuthStore } from "@/stores/auth-store";

function isImmersive(pathname: string): boolean {
  // Reader uses its own full-screen chrome.
  return /^\/book\/[^/]+\/read(\/|$)/.test(pathname);
}

export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const router = useRouter();
  const user = useAuthStore((s) => s.user);
  const hasFetched = useAuthStore((s) => s.hasFetched);
  const fetchUser = useAuthStore((s) => s.fetchUser);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  useEffect(() => {
    if (hasFetched && !user) {
      const next = encodeURIComponent(pathname);
      router.replace(`/login?next=${next}`);
    }
  }, [hasFetched, user, pathname, router]);

  if (isImmersive(pathname)) {
    return <main className="flex-1">{children}</main>;
  }

  return (
    <div className="flex min-h-screen w-full">
      {user && <SideNav />}
      <main className="flex min-h-screen flex-1 flex-col">{children}</main>
    </div>
  );
}
