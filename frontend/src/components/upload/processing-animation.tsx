"use client";

import { motion } from "framer-motion";
import { useTranslations } from "next-intl";
import { Upload, FileSearch, Brain, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";
import type { BookStatus } from "@/lib/constants";

const stepConfig = [
  { key: "uploading", icon: Upload },
  { key: "parsing", icon: FileSearch },
  { key: "extracting", icon: Brain },
  { key: "ready", icon: CheckCircle2 },
] as const;

const statusToStep: Record<string, number> = {
  uploading: 0,
  parsing: 1,
  extracting: 2,
  ready: 3,
};

interface ProcessingAnimationProps {
  status: BookStatus;
}

export function ProcessingAnimation({ status }: ProcessingAnimationProps) {
  const t = useTranslations("upload.stages");
  const currentStep = statusToStep[status] ?? 0;

  return (
    <div className="mx-auto w-full max-w-md">
      <div className="flex items-center justify-between">
        {stepConfig.map((step, index) => {
          const Icon = step.icon;
          const isActive = index === currentStep;
          const isComplete = index < currentStep;

          return (
            <div
              key={step.key}
              className="flex flex-col items-center gap-2.5"
            >
              <motion.div
                className={cn(
                  "flex h-11 w-11 items-center justify-center rounded-xl ring-1 transition-colors duration-500",
                  isComplete && "bg-primary text-primary-foreground ring-primary",
                  isActive && "bg-primary/10 text-primary ring-primary/25",
                  !isComplete && !isActive && "bg-subtle text-muted-foreground ring-border/60",
                )}
                animate={
                  isActive
                    ? {
                        boxShadow: [
                          "0 0 0 0 rgba(99,102,241,0)",
                          "0 0 0 8px rgba(99,102,241,0.08)",
                          "0 0 0 0 rgba(99,102,241,0)",
                        ],
                      }
                    : {}
                }
                transition={
                  isActive
                    ? { duration: 2, repeat: Infinity, ease: "easeInOut" }
                    : {}
                }
              >
                <Icon className="h-4 w-4" />
              </motion.div>
              <span
                className={cn(
                  "font-mono text-[10px] uppercase tracking-[0.08em] transition-colors",
                  isActive
                    ? "text-foreground"
                    : isComplete
                      ? "text-foreground"
                      : "text-muted-foreground",
                )}
              >
                {t(step.key)}
              </span>
            </div>
          );
        })}
      </div>

      <div className="relative mt-[-2.75rem] mb-8 mx-6 h-px bg-border/60 -z-10">
        <motion.div
          className="absolute left-0 top-0 h-full bg-primary"
          initial={{ width: "0%" }}
          animate={{
            width: `${(currentStep / (stepConfig.length - 1)) * 100}%`,
          }}
          transition={{ duration: 0.8, ease: "easeInOut" }}
        />
      </div>
    </div>
  );
}
