import type { Metadata } from "next";
import "./globals.css";

import { AppShell } from "@/components/app-shell";

export const metadata: Metadata = {
  title: "SLP3 KG-LLM Reading Notes",
  description: "Interactive reading notes for Speech and Language Processing with KG-RAG and LLM reasoning focus.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="zh-CN">
      <body>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
