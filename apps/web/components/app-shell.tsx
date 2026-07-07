"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BookOpen, FileText, GitBranch, Home, NotebookPen } from "lucide-react";

import { cn } from "@/lib/utils";

const nav = [
  { href: "/", label: "Dashboard", icon: Home },
  { href: "/chapters", label: "Chapters", icon: BookOpen },
  { href: "/roadmap", label: "Roadmap", icon: GitBranch },
  { href: "/notes", label: "Notes", icon: NotebookPen },
  { href: "/report", label: "Report", icon: FileText },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  return (
    <div className="min-h-dvh">
      <header className="sticky top-0 z-20 border-b bg-background/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl flex-col gap-3 px-4 py-4 sm:px-6 lg:flex-row lg:items-center lg:justify-between">
          <Link href="/" className="flex items-center gap-3 no-underline">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <BookOpen className="h-5 w-5" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">SLP3 Reading Notes</p>
              <h1 className="text-base font-semibold tracking-normal">KG + LLM 推理学习系统</h1>
            </div>
          </Link>
          <nav className="flex gap-1 overflow-x-auto" aria-label="Primary navigation">
            {nav.map((item) => {
              const Icon = item.icon;
              const active = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "flex min-h-11 items-center gap-2 rounded-md px-3 text-sm font-medium text-muted-foreground no-underline transition-colors hover:bg-muted hover:text-foreground",
                    active && "bg-secondary text-foreground"
                  )}
                >
                  <Icon className="h-4 w-4" />
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:py-8">{children}</main>
    </div>
  );
}
