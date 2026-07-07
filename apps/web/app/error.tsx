"use client";

import { AlertTriangle } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

export default function Error({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <Card>
      <CardContent className="p-10 text-center">
        <AlertTriangle className="mx-auto h-10 w-10 text-destructive" />
        <h2 className="mt-4 text-xl font-semibold">页面数据加载失败</h2>
        <p className="mt-2 text-sm text-muted-foreground">请确认 FastAPI 服务正在运行，然后重试。</p>
        <Button className="mt-5" onClick={reset}>
          重试
        </Button>
      </CardContent>
    </Card>
  );
}
