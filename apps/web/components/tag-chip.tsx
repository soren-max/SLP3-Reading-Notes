import { cn } from "@/lib/utils";

export function TagChip({ label, active = false, onClick }: { label: string; active?: boolean; onClick?: () => void }) {
  const Comp = onClick ? "button" : "span";
  return (
    <Comp
      onClick={onClick}
      className={cn(
        "inline-flex min-h-8 items-center rounded-full border px-3 text-xs font-medium transition-all duration-200",
        "border-border bg-secondary/70 text-secondary-foreground",
        onClick && "cursor-pointer hover:border-primary hover:bg-secondary focus-ring",
        active && "border-primary bg-primary text-primary-foreground dark:text-primary-foreground"
      )}
    >
      {label}
    </Comp>
  );
}
