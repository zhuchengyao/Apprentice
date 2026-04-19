"use client"

import { Button as ButtonPrimitive } from "@base-ui/react/button"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  [
    "group/button relative inline-flex shrink-0 items-center justify-center gap-2",
    "rounded-lg border border-transparent bg-clip-padding font-medium whitespace-nowrap",
    "transition-[background,color,border-color,box-shadow,transform] duration-150 ease-out",
    "outline-none select-none",
    "focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background",
    "active:not-aria-[haspopup]:translate-y-px",
    "disabled:pointer-events-none disabled:opacity-50",
    "aria-invalid:border-destructive aria-invalid:ring-2 aria-invalid:ring-destructive/30",
    "[&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4",
  ].join(" "),
  {
    variants: {
      variant: {
        default: [
          "bg-foreground text-background shadow-sm",
          "hover:bg-foreground/90",
          "dark:bg-foreground dark:text-background",
        ].join(" "),
        primary: [
          "bg-primary text-primary-foreground shadow-sm shadow-primary/20",
          "hover:bg-primary/92 hover:shadow-primary/25",
          "dark:shadow-primary/15",
        ].join(" "),
        outline: [
          "border-border bg-background text-foreground",
          "hover:bg-subtle hover:border-foreground/20",
          "aria-expanded:bg-subtle",
        ].join(" "),
        secondary: [
          "bg-secondary text-secondary-foreground",
          "hover:bg-secondary/80",
          "aria-expanded:bg-secondary/80",
        ].join(" "),
        soft: [
          "bg-accent text-accent-foreground",
          "hover:bg-accent/70",
        ].join(" "),
        ghost: [
          "text-foreground/80",
          "hover:bg-subtle hover:text-foreground",
          "aria-expanded:bg-subtle aria-expanded:text-foreground",
        ].join(" "),
        destructive: [
          "bg-destructive/10 text-destructive",
          "hover:bg-destructive/15",
          "dark:bg-destructive/15 dark:hover:bg-destructive/25",
        ].join(" "),
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-3.5 text-sm has-data-[icon=inline-end]:pr-3 has-data-[icon=inline-start]:pl-3",
        xs:
          "h-6 gap-1 rounded-md px-2 text-[11px] [&_svg:not([class*='size-'])]:size-3",
        sm:
          "h-8 gap-1.5 rounded-md px-2.5 text-[13px] [&_svg:not([class*='size-'])]:size-3.5",
        lg:
          "h-10 gap-2 px-4 text-[15px] has-data-[icon=inline-end]:pr-3.5 has-data-[icon=inline-start]:pl-3.5",
        xl:
          "h-12 gap-2 rounded-xl px-5 text-base has-data-[icon=inline-end]:pr-4 has-data-[icon=inline-start]:pl-4",
        icon: "size-9",
        "icon-xs": "size-6 rounded-md [&_svg:not([class*='size-'])]:size-3",
        "icon-sm": "size-8 rounded-md",
        "icon-lg": "size-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

function Button({
  className,
  variant = "default",
  size = "default",
  ...props
}: ButtonPrimitive.Props & VariantProps<typeof buttonVariants>) {
  return (
    <ButtonPrimitive
      data-slot="button"
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}

export { Button, buttonVariants }
