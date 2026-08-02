# AI Research Notes Workspace — Design System

This project is inspired by a warm, human, editorial product style. It does not use Claude, Anthropic, or any third-party brand name, mark, logo, proprietary asset, or proprietary font. The product remains **AI Research Notes Workspace**, with its own research and internship content system.

## Direction

Create a calm, content-first workspace: warm off-white canvas, deep ink text, restrained terracotta emphasis, and dark technical surfaces for code- and system-oriented information. Prefer readable long-form rhythm over dashboard spectacle. Avoid blue-purple gradients, glassmorphism, glowing effects, excessive shadows, and decorative animation.

## Tokens

- Canvas `#f7f3ec`; primary surface `#fffdf8`; subtle surface `#f0ebe3`; card surface `#eee7dc`.
- Ink `#1f1e1b`; muted text `#68645d`; border `#d9d2c7`.
- Accent `#bd6048`; accent hover `#a8503b`; soft accent `#f1d7ce`.
- Technical surface `#202633`; technical text `#f4f1ea`.
- Success `#39735a`; warning `#a46a24`; danger `#a7463d`.
- Radius: 6px controls, 10px cards, 16px feature surfaces. Use shadows sparingly; borders and surface contrast create depth.

## Typography

- Body and UI: `"Noto Sans SC", "PingFang SC", "Microsoft YaHei", Inter, ui-sans-serif, system-ui, sans-serif`.
- Display headings: `Georgia, "Noto Serif SC", "Songti SC", serif`; regular weight, compact tracking.
- Code: `"JetBrains Mono", "SFMono-Regular", Consolas, monospace`.
- Keep body text at 16px with 1.55–1.7 line-height. Use serif display faces only for major page and section headings.

## Layout and components

- Use a centered content container (max 1200px) and a readable content measure (about 760px) for long text.
- Create clear section rhythm with 32–64px spacing. On mobile, keep 16–24px page padding and stack grids without horizontal scrolling.
- Navigation is a quiet warm surface with text labels and a single active-state indicator.
- Buttons use the terracotta accent only for the primary action. Secondary controls use a border and the primary surface.
- Use dark panels only where technical context benefits from contrast: flows, code, and status summaries.
- Cards should not all look alike: use flat editorial sections for lists, subtle bordered surfaces for forms, and a limited number of dark technical panels.
- Keep focus rings visible, preserve semantic headings, and respect reduced motion.

## Reference

Adapted from the visual principles in the locally installed VoltAgent awesome-design-md Claude analysis at `/home/hoot/.codex/vendor/awesome-design-md/design-md/claude/DESIGN.md`; proprietary branding and fonts are intentionally excluded.
