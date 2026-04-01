"use client";

import { motion } from "framer-motion";
import { Upload, FileSearch, Brain, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";
import type { BookStatus } from "@/lib/constants";

const steps = [
  { key: "uploading", label: "Uploading", icon: Upload },
  { key: "parsing", label: "Parsing content", icon: FileSearch },
  { key: "extracting", label: "Extracting knowledge", icon: Brain },
  { key: "ready", label: "Ready to learn", icon: CheckCircle2 },
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
  const currentStep = statusToStep[status] ?? 0;

  return (
    <div className="mx-auto w-full max-w-md">
      <div className="flex items-center justify-between">
        {steps.map((step, index) => {
          const Icon = step.icon;
          const isActive = index === currentStep;
          const isComplete = index < currentStep;

          return (
            <div key={step.key} className="flex flex-col items-center gap-2">
              <motion.div
                className={cn(
                  "flex h-12 w-12 items-center justify-center rounded-full transition-colors duration-500",
                  isComplete && "bg-foreground text-background",
                  isActive && "bg-foreground/10",
                  !isComplete && !isActive && "bg-muted",
                )}
                animate={
                  isActive
                    ? {
                        boxShadow: [
                          "0 0 0 0 rgba(0,0,0,0)",
                          "0 0 0 8px rgba(0,0,0,0.05)",
                          "0 0 0 0 rgba(0,0,0,0)",
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
                <Icon
                  className={cn(
                    "h-5 w-5",
                    isComplete && "text-background",
                    isActive && "text-foreground",
                    !isComplete && !isActive && "text-muted-foreground",
                  )}
                />
              </motion.div>
              <span
                className={cn(
                  "text-xs font-medium transition-colors",
                  isActive
                    ? "text-foreground"
                    : isComplete
                      ? "text-foreground"
                      : "text-muted-foreground",
                )}
              >
                {step.label}
              </span>
            </div>
          );
        })}
      </div>

      {/* Progress line */}
      <div className="relative mt-[-2.75rem] mb-8 mx-6 h-0.5 bg-muted -z-10">
        <motion.div
          className="absolute left-0 top-0 h-full bg-foreground"
          initial={{ width: "0%" }}
          animate={{ width: `${(currentStep / (steps.length - 1)) * 100}%` }}
          transition={{ duration: 0.8, ease: "easeInOut" }}
        />
      </div>
    </div>
  );
}
