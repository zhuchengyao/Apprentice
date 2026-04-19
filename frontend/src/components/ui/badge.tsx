import { mergeProps } from "@base-ui/react/merge-props"
import { useRender } from "@base-ui/react/use-render"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const badgeVariants = cva(
  [
    "group/badge inline-flex h-5 w-fit shrink-0 items-center justify-center gap-1",
    "overflow-hidden rounded-full border border-transparent px-2 py-0.5",
    "text-[11px] font-medium whitespace-nowrap tracking-wide transition-all",
    "focus-visible:ring-2 focus-visible:ring-ring/50",
    "has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5",
    "aria-invalid:border-destructive aria-invalid:ring-destructive/30",
    "[&>svg]:pointer-events-none [&>svg]:size-3!",
  ].join(" "),
  {
    variants: {
      variant: {
        default: "bg-foreground text-background",
        primary:
          "bg-primary/12 text-primary border-primary/20 dark:bg-primary/20 dark:text-primary-foreground",
        secondary:
          "bg-secondary text-secondary-foreground [a]:hover:bg-secondary/80",
        soft:
          "bg-accent text-accent-foreground [a]:hover:bg-accent/80",
        success:
          "bg-success/12 text-success border-success/20 dark:bg-success/18",
        warning:
          "bg-warning/15 text-warning border-warning/25 dark:bg-warning/20",
        destructive:
          "bg-destructive/10 text-destructive border-destructive/20 dark:bg-destructive/20",
        outline:
          "border-border text-foreground/80 [a]:hover:bg-subtle",
        ghost:
          "text-muted-foreground hover:bg-subtle hover:text-foreground",
        mono:
          "bg-transparent text-muted-foreground border border-border/70 font-mono tracking-[0.08em] uppercase text-[10px]",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

function Badge({
  className,
  variant = "default",
  render,
  ...props
}: useRender.ComponentProps<"span"> & VariantProps<typeof badgeVariants>) {
  return useRender({
    defaultTagName: "span",
    props: mergeProps<"span">(
      {
        className: cn(badgeVariants({ variant }), className),
      },
      props
    ),
    render,
    state: {
      slot: "badge",
      variant,
    },
  })
}

export { Badge, badgeVariants }
