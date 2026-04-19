interface LegalHeroProps {
  eyebrow: string;
  title: string;
  effectiveDate: string;
  description?: string;
}

export function LegalHero({
  eyebrow,
  title,
  effectiveDate,
  description,
}: LegalHeroProps) {
  return (
    <header className="not-prose mb-14 border-b border-border/70 pb-12">
      <p className="eyebrow">{eyebrow}</p>
      <h1 className="mt-5 font-display text-5xl font-semibold tracking-tight sm:text-6xl">
        {title}
      </h1>
      {description && (
        <p className="mt-5 max-w-2xl text-[16px] leading-relaxed text-muted-foreground">
          {description}
        </p>
      )}
      <div className="mt-7 inline-flex items-center gap-2 rounded-full border border-border/70 bg-card/70 px-3 py-1 font-mono text-[10px] uppercase tracking-[0.14em] text-muted-foreground">
        <span className="relative flex h-2 w-2">
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-success/60 opacity-75" />
          <span className="relative inline-flex h-2 w-2 rounded-full bg-success" />
        </span>
        {effectiveDate}
      </div>
    </header>
  );
}
