# Leela — History

## Core Context

- Project: caveman — living doc comparing GitHub Copilot token usage across techniques
- User: Marco Olivo
- Stack: Markdown documentation, GitHub Copilot experiments
- Techniques of interest: caveman-speak, English vs other languages, other token optimization techniques TBD

## Learnings

### 2026-04-14: Doc Structure & Experiment Framework Designed

- Produced detailed 5-part outline for token optimization guide (leela-doc-outline.md)
- Defined taxonomy: 5 categories (A-E), 16 subcategories of token optimization techniques
- Designed experiment framework: 10 tasks, 6 metrics, controlled methodology with 3 runs per combination
- Scope decisions: v1 covers caveman modes, wenyan, English vs Chinese, context management, workflow skills. Out: multi-language comparison (needs native speakers), model-specific tokenizer diffs, Copilot Inline completions
- Key principle: data-backed claims only — no percentage savings without worked examples
- Progressive complexity: reader gets value from section 2.1 alone, advanced techniques later
- Deliverables in `.squad/decisions/inbox/leela-doc-structure.md` and `leela-doc-outline.md`

### 2026-04-22: README "Install" Section Messaging Fix

- Problem: "Install as a Copilot CLI Plugin" section causes readers to think plugin does runtime LLM compression. Phrases "bakes techniques into every session" and "without thinking about it" imply active processing engine.
- Root cause: Section frames mechanism (auto-loading skills) but not nature (static markdown behavioral instructions). Two-column table creates guide-vs-plugin binary that implies plugin is the automated version of the guide.
- Strategy delivered to Hermes:
  1. Rename section — foreground "habits/rules," not "plugin/install"
  2. Lead with what skills ARE (pre-authored markdown rules), not what they do
  3. Reframe two-column table from "guide vs. plugin" to "learn → codify"
  4. Add "not runtime compression" callout immediately after header
  5. Three-layer terminology: "habits" (headline) → "rules" (explanation) → "skills" (technical term)
  6. Kill phrases: "bakes techniques," "without thinking about it"
- Decision: messaging strategy only — Hermes implements prose

### 2026-04-14: Cross-Agent Update

- Farnsworth confirmed taxonomy alignment, cataloged 28 techniques across 8 categories (expanded from Leela's 5)
- Hermes wrote guide at 1107 lines using outline. Added Quick Start section (not in original outline) — good call, validates progressive-complexity principle
- Key data from Farnsworth: English is most token-efficient, CJK myth busted, caveman-speak = highest ROI technique

### 2026-04-27: README Quick Start `Savings` Column Review

- Current `Savings` column in README Quick Start over-compresses unlike claims into one field: output-token percentages, context-token percentages, task-scale token counts, and billing discounts.
- Structural problem bigger than wording problem. Same column makes readers compare non-comparable units and infer certainty not supported by the methodology.
- Recommendation: remove one mixed `Savings` column from Quick Start. Replace with mechanism-aware framing such as `Primary Impact` plus `Confidence`, with scoped numeric notes only for techniques whose unit is stable.
- Technique-class split matters:
  - Output control and context trimming can carry scoped numeric effects.
  - Mode selection and MCP audit should be framed as workflow/task overhead.
  - Auto model selection is pricing-layer optimization, not the same class as token reduction.
  - Prompt precision should be framed as quality-first, token-second.
- Logged team decision in `.squad/decisions/inbox/leela-savings-column.md`.

### 2026-04-27: Cross-Agent Update — Bender Backed Methodology Risk

- Bender independently rejected the current Quick Start `Savings` column on methodology grounds.
- Shared conclusion: one field currently invites false comparability across output savings, context savings, task-token ranges, and billing discounts.
- Useful alignment for future README rewrite: replacement structure should foreground scoped impact and confidence, not one universal savings claim.

### 2026-04-27: Model Cost Language Must Move Off Multiplier-Centric Framing

- New directive: billing multipliers are going away; exact per-model prices are not public yet; Auto persists; keep the current documented 10% Auto discount for now.
- Repo decision: keep Auto-as-default guidance and UBB token-bucket framing, but stop teaching readers to reason with `0.33x` / `1x` / `3x` tables as the primary live model-cost surface.
- Rewrite rule: use durable language such as `model-specific rates`, `higher-cost models`, `supported Auto pool`, `plan/policy availability`, and `pin manually when task justifies it`.
- Historical exception: PRU / multiplier language stays only where the repo is explicitly explaining the retired system or the transition from PRUs to UBB.
- Strong caution for Hermes: do not invent placeholder price tables and do not use vendor API token prices as if they were Copilot per-model prices.

### 2026-04-28: Cross-Agent Update — Repo Structure Analysis Batch Logged

- Scribe recorded a parallel repo-structure analysis batch with Farnsworth and Bender.
- Leela owned the reader-facing structure lens: top-level entry points, doc flow, and information architecture fit.
- Farnsworth covered factual repo inventory; Bender covered structure-risk review.
- Scribe later merged Leela's repo-structure decision with Bender's review verdict into `decisions.md`.
- Farnsworth's inventory findings reinforced the same direction: keep the docs-first spine, then clean up boundary clarity, taxonomy drift, and asset ownership.

### 2026-04-28: Repo Structure Review

- Core structure is fundamentally sound for a docs-first project: `docs/` holds the guide, `skills/` holds reusable behavior packs, `agents/` holds the packaged agent surface, and `mkdocs.yml` keeps published navigation simple.
- Main structural risk: too many repo identities sit at top level without an explicit map. Public guide, plugin packaging, repo-local Copilot config, and internal `.squad/` governance coexist, but the boundary between distributable assets and internal operating files is mostly implicit.
- Discoverability gaps observed:
  - README currently explains guide content well but not repository architecture.
  - `plugin.json` and `skills-lock.json` are visible at root even though install/runtime narrative was removed from README, so purpose is now less obvious.
  - Hidden config trees (`.github/`, `.copilot/`, `.squad/`) add real structure but are not legible to a new contributor scanning root.
  - Numbered docs jump from `10` to `13` and can read like missing content instead of intentional reserved slots.
  - Asset placement duplicates across `assets/` and `docs/assets/` for what appears to be the same image.
- Verdict formed for team use: light reorganization later, not substantial rethink. Keep docs-first spine; improve repo map, boundary labeling, naming consistency, and asset placement before adding more surfaces.
