"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BookOpen, FileText, GitBranch, Home, Library, NotebookPen, NotebookTabs, Briefcase, Workflow } from "lucide-react";

import { cn } from "@/lib/utils";

const nav = [
  { href: "/", label: "Dashboard", icon: Home },
  { href: "/sources", label: "Sources", icon: Library },
  { href: "/chapters", label: "SLP3", icon: BookOpen },
  { href: "/text-to-model", label: "文本接口", icon: Workflow },
  { href: "/roadmap", label: "Roadmap", icon: GitBranch },
  { href: "/notes", label: "Notes", icon: NotebookPen },
  { href: "/interns", label: "实习记录", icon: Briefcase },
  { href: "/report", label: "Report", icon: FileText },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  return (
    <div className="min-h-dvh">
      <header className="sticky top-0 z-20 border-b bg-background/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl flex-col gap-3 px-4 py-3 sm:px-6 lg:flex-row lg:items-center lg:justify-between">
          <Link href="/" className="flex items-center gap-3 no-underline">
            <div className="flex h-10 w-10 items-center justify-center rounded-md bg-foreground text-background">
              <NotebookTabs className="h-5 w-5" />
            </div>
            <div>
              <p className="text-xs font-medium uppercase tracking-[0.12em] text-muted-foreground">Personal Knowledge Workspace</p>
              <h1 className="display-type text-lg leading-tight">AI Research Notes</h1>
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
                    "flex min-h-11 items-center gap-2 rounded-md px-3 text-sm font-medium text-muted-foreground no-underline transition-colors duration-200 hover:bg-secondary hover:text-foreground focus-ring",
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
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:py-12">{children}</main>
    </div>
  );
}
