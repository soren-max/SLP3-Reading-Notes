"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BookOpen, FileText, GitBranch, Home, Library, NotebookPen, Sparkles } from "lucide-react";

import { cn } from "@/lib/utils";

const nav = [
  { href: "/", label: "Dashboard", icon: Home },
  { href: "/sources", label: "Sources", icon: Library },
  { href: "/chapters", label: "SLP3", icon: BookOpen },
  { href: "/roadmap", label: "Roadmap", icon: GitBranch },
  { href: "/notes", label: "Notes", icon: NotebookPen },
  { href: "/report", label: "Report", icon: FileText },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  return (
    <div className="min-h-dvh">
      <header className="sticky top-0 z-20 border-b bg-background/76 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl flex-col gap-3 px-4 py-4 sm:px-6 lg:flex-row lg:items-center lg:justify-between">
          <Link href="/" className="flex items-center gap-3 no-underline">
            <div className="flex h-11 w-11 items-center justify-center rounded-lg bg-gradient-to-br from-indigo-600 to-cyan-500 text-white shadow-lg shadow-indigo-500/20">
              <Sparkles className="h-5 w-5" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">AI Research Notes Workspace</p>
              <h1 className="text-base font-semibold tracking-normal">NLP · LLM · RAG · Knowledge Graph Reasoning</h1>
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
                    "flex min-h-11 items-center gap-2 rounded-md px-3 text-sm font-medium text-muted-foreground no-underline transition-all duration-200 hover:-translate-y-0.5 hover:bg-muted hover:text-foreground focus-ring",
                    active && "bg-secondary text-foreground shadow-sm"
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
