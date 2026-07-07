import { ArrowRight } from "lucide-react";

const steps = ["LLM Foundation", "RAG", "Information Extraction", "Entity Linking", "KG Reasoning"];

export function ResearchThread() {
  return (
    <div className="rounded-lg border bg-card/80 p-4 backdrop-blur-xl">
      <div className="flex flex-col gap-3 lg:flex-row lg:items-center">
        {steps.map((step, index) => (
          <div key={step} className="flex flex-1 items-center gap-3">
            <div className="flex min-h-14 flex-1 items-center rounded-lg border bg-background/70 px-4 text-sm font-semibold shadow-sm">
              {step}
            </div>
            {index < steps.length - 1 && <ArrowRight className="hidden h-5 w-5 shrink-0 text-muted-foreground lg:block" />}
          </div>
        ))}
      </div>
    </div>
  );
}
