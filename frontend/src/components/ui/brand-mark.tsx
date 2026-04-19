interface BrandMarkProps {
  size?: number;
  withDot?: boolean;
  className?: string;
}

export function BrandMark({
  size = 28,
  withDot = true,
  className,
}: BrandMarkProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      className={className}
      aria-hidden
    >
      <rect width="32" height="32" rx="8" fill="var(--foreground)" />
      <g
        transform="translate(8 8)"
        stroke="var(--background)"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      >
        <path d="M8 0L9.5 6.5L16 8L9.5 9.5L8 16L6.5 9.5L0 8L6.5 6.5L8 0Z" />
      </g>
      {withDot && (
        <>
          <circle cx="25" cy="7" r="3" fill="var(--primary)" />
          <circle
            cx="25"
            cy="7"
            r="4.5"
            fill="none"
            stroke="var(--background)"
            strokeWidth="1.5"
          />
        </>
      )}
    </svg>
  );
}
