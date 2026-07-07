import { Card, CardContent } from "@/components/ui/card";

export default function Loading() {
  return (
    <div className="grid gap-4">
      <Card>
        <CardContent className="space-y-4 p-6">
          <div className="h-8 w-64 animate-pulse rounded-md bg-muted" />
          <div className="h-4 w-full max-w-2xl animate-pulse rounded-md bg-muted" />
          <div className="h-4 w-3/4 animate-pulse rounded-md bg-muted" />
        </CardContent>
      </Card>
      <div className="grid gap-4 md:grid-cols-3">
        {[1, 2, 3].map((item) => (
          <div key={item} className="h-36 animate-pulse rounded-lg border bg-card/70" />
        ))}
      </div>
    </div>
  );
}
