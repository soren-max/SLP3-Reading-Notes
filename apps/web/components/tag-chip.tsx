import { cn } from "@/lib/utils";

export function TagChip({ label, active = false, onClick }: { label: string; active?: boolean; onClick?: () => void }) {
  const Comp = onClick ? "button" : "span";
  return (
    <Comp
      onClick={onClick}
      className={cn(
        "inline-flex min-h-8 items-center rounded-full border px-3 text-xs font-medium transition-all duration-200",
        "border-indigo-200/70 bg-indigo-50/80 text-indigo-700 dark:border-indigo-400/25 dark:bg-indigo-400/10 dark:text-indigo-200",
        onClick && "cursor-pointer hover:-translate-y-0.5 hover:border-primary hover:bg-secondary focus-ring",
        active && "border-primary bg-primary text-primary-foreground dark:text-primary-foreground"
      )}
    >
      {label}
    </Comp>
  );
}
