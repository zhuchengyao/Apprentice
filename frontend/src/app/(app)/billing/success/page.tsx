"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function BillingSuccessPage() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/billing?success=credits");
  }, [router]);
  return null;
}
