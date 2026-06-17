# Squad Decisions

## Active Decisions

### 2026-04-14: Token Optimization Guide — Structure & Taxonomy
**Author:** Leela | **Status:** Active

- Taxonomy: 5 categories (A-E), 16 subcategories of token optimization techniques
  - A: Prompt Compression (caveman-speak, structured format, abbreviations, code-centric)
  - B: Natural Language Choice (CJK, wenyan, other languages)
  - C: Context Management (instruction compression, memory compression, file exclusion, file organization)
  - D: Output Control (format directives, terse response, scope limiting)
  - E: Workflow Optimization (commits, PR reviews, documentation)
- Experiment framework: 10 tasks, 6 metrics, 3 runs per combination, temperature=0, median

### 2026-04-14: Wenyan — Include as Demo Only, Not Recommended
**Author:** Hermes (informed by Farnsworth data) | **Status:** Active

- Wenyan modes kept in guide for completeness but clearly labeled "demo only"
- Data proves CJK costs MORE tokens (1.7-2.4x English) due to multi-byte encoding + English-dominant tokenizer
- Readers who've heard CJK myth need to see it debunked with numbers

### 2026-04-14: Quick Start Section at Top
**Author:** Hermes | **Status:** Active

- "5 Things to Do Right Now" before table of contents
- 1100-line doc needs fast path; most readers want immediate action

### 2026-04-14: Self-Reference Repo's Own copilot-instructions.md
**Author:** Hermes | **Status:** Active

- Guide uses this repo's `.github/copilot-instructions.md` as concrete example
- Proves guide practices what it preaches

### 2026-04-14: Full Technique Matrix + Big Winners Summary
**Author:** Hermes | **Status:** Active

- All 28 techniques from Farnsworth included in matrix
- "Big Winners" callout beneath for scanners who skip 28-row table

### 2026-04-14: Guide Tone — Practical, Not Academic
**Author:** Hermes | **Status:** Active

- Direct, second-person, imperative, concrete numbers
- Every claim backed by Farnsworth's data

### 2026-04-14: English Most Token-Efficient Language
**Author:** Farnsworth | **Status:** Active

- English = baseline. Latin-alphabet languages 1.5-2x. CJK 1.7-2.4x. Cyrillic 2.5-3x.
- Non-English prompts cost MORE tokens. Transliteration helps (~50% cut for non-Latin).

### 2026-04-14: CJK Tokens-Per-Character Correction
**Author:** Bender | **Status:** Active

- Guide originally said "2-3 tokens/char" for CJK. Data shows ~1-1.4 tokens/char. The "2-3" figure is UTF-8 bytes, not tokens.
- Fixed in §2.2.2, §5.1 Cheat Sheet. Conclusion unchanged: English still cheaper per semantic unit.
- Source #14 "Baloney, T." fixed to "Shaw, A. (tonybaloney)."
- Lesson: preserve source hedging when load-bearing. Farnsworth's "potentially more" became "2-3 tokens each" → factual error.

### 2026-04-14: Multiplicative Savings Stacking
**Author:** Bender | **Status:** Suggestion

- Savings stack multiplicatively not additively: 50% + 30% ≠ 80%, it's 65%.
- Guide says "can cut 60%+" which is defensible but stacking mechanics unexplained. Should fix.

### 2026-04-14: New Sections Appended After §2.5
**Author:** Hermes | **Status:** Active

- §2.6 (AGENTS.md) and §2.7 (MCP costs) placed after §2.5, not inserted mid-sequence.
- Avoids renumbering existing sections and breaking external links.

### 2026-04-14: AGENTS.md Section — Opinionated "Less Is More"
**Author:** Hermes | **Status:** Active

- ETH Zurich AGENTBENCH study: LLM-generated context files hurt performance in 5/8 settings, cost 20-23% more tokens.
- One study (Feb 2026). Lulla et al. counterpoint included for balance.
- Framed with specific data points, not absolutes. Flagged for update if contradicted.

### 2026-04-14: MCP Token Cost Estimates
**Author:** Hermes (from Farnsworth research) | **Status:** Active

- ~100-500 tokens per tool definition, ~200 average. Empirical observation, not peer-reviewed.
- GitHub MCP server with 40+ tools is real data point. Costs vary by tool complexity and tokenizer.

### 2026-04-14: Quick Start & Big Winners Expansion (5→7)
**Author:** Hermes | **Status:** Active

- Added items 6 (Audit MCP servers) and 7 (Prune AGENTS.md) to Quick Start and Big Winners.
- Both are high-impact, low-effort. Existing 5 items unchanged.

### 2026-04-14: MCP Tool Definitions Resent Every Turn
**Author:** Farnsworth | **Status:** Active

- Tool schemas sent with EVERY API call. Not cached between turns. Model is stateless.
- 10 servers = ~20,000 tokens overhead/turn. 5-step agent task = 100K+ just in tool overhead.
- Only enable/disable entire MCP servers, not individual tools (GitHub Issue #7328).
- Workspace-scoped `.vscode/mcp.json` preferred over global config to reduce per-project overhead.

### 2026-04-22: README Plugin Section — Messaging Strategy for Misconception Fix
**Author:** Leela | **Status:** Active

- Problem: "Install as a Copilot CLI Plugin" section causes readers to think plugin does runtime LLM compression. Phrases "bakes techniques into every session" and "without thinking about it" imply active processing.
- Root cause: Section frames mechanism (auto-loading skills) but not nature (static markdown behavioral instructions). Two-column table creates guide-vs-plugin binary implying plugin is the automated version of the guide.
- Strategy: (1) Rename section to foreground "habits/rules," not "plugin/install"; (2) Lead with what skills ARE (pre-authored markdown rules); (3) Reframe table from "guide vs. plugin" to "learn → codify"; (4) Add "not runtime compression" blockquote immediately after header; (5) Three-layer terminology: habits (headline) → rules (explanation) → skills (technical term); (6) Kill phrases "bakes techniques," "without thinking about it."

### 2026-04-22: README Plugin Section Rewrite — Clarified Static Behavioral Rules
**Author:** Hermes | **Status:** Active

- Implemented Leela's messaging strategy in README plugin section.
- Renamed: "Install as a Copilot CLI Plugin" → "Install the Plugin — Behavioral Rules, Not a Compression Engine"
- Added explicit "What this is NOT" blockquote to preempt runtime-compression misconception.
- Explained mechanism: static markdown files, description-match triggering, zero overhead when idle.
- Added "What it does" column to component table for clarity.
- Updated "Two ways to use this repo" table: replaced "bakes techniques into every session" with "Pre-authored behavioral rules that make Copilot terse by default."
- All install commands and code blocks preserved unchanged.

### 2026-04-22: Remove Plugin/Install Documentation from README
**Author:** Hermes | **Status:** Active | **Requested by:** Marco Olivo

- Removed "Two ways to use this repo" section and entire "Install the Plugin" section from README.md (~85 lines total)
- Plugin files (`plugin.json`, `skills/`, `agents/`) remain in repo unchanged
- README now flows: intro blockquote → Quick Start → Guide Contents. Single path, no bifurcation.
- No transition text added — flow is clean without it
- Previous decision "README Plugin Section — Messaging Strategy for Misconception Fix" (2026-04-22) is superseded: the section it rewrote no longer exists in README

### 2026-04-27: README Quick Start — Replace `Savings` Column with Scoped Impact Framing
**Author:** Leela | **Status:** Active

- Do not keep one mixed `Savings` field in README Quick Start. It currently blends incompatible units: output-token percentages, prompt-slice percentages, always-on context cuts, task-scale token ranges, and billing discounts.
- Quick Start should stay action-priority oriented, not act like a benchmark table with cross-row comparability it cannot defend.
- Preferred replacement structure:
  - `Primary Impact`: output volume | always-on context | agent overhead | model cost multiplier | prompt quality / minor input
  - `Confidence`: strong measured | measured but context-dependent | directional only
  - Optional `Typical Effect` note only when units are homogeneous and tightly scoped
- Presentation must stay mechanism-aware:
  - Output control: scoped `% of output tokens`
  - Context trimming: scoped `% of always-on context`
  - Ask vs Agent / MCP audit: `tokens per task`
  - Auto model selection: billing discount or cost multiplier, not token savings
  - Prompt precision: quality-first, token-second; no headline savings number

### 2026-04-27: README Quick Start — Savings Claims Must Not Imply Comparable Total Savings
**Author:** Bender | **Status:** Active

- Reviewer verdict on current table: reject the `Savings` column as methodologically unsafe.
- Core constraint: total cost effect depends on input/output/cached mix, task mode, context size, and model routing. Row-to-row values in one shared column falsely imply comparable total savings.
- If any scoped numeric field remains, it must be clearly labeled as non-additive, non-comparable across technique classes, and not equal to total bill reduction.
- Acceptable fallback structures:
  - `Primary Effect` plus `Scope`
  - Directionality/confidence language instead of headline percentages

### 2026-04-27: README Quick Start Table Re-Review — Scoped Table Approved
**Author:** Bender | **Status:** Active

- Reviewer approved the revised Quick Start table after `Savings` was replaced with `Primary Effect` plus `Scope`.
- Approval basis: the table now frames effects by mechanism instead of implying one comparable savings metric across rows.
- Remaining caveat: note under the table is sufficient, but stronger if it explicitly says rows are not directly comparable and some rows affect billing rather than raw token count.

### 2026-04-28: CodeAct Mention — Optional Advanced CLI-Only Tactic

**Author:** Hermes | **Status:** Active | **Requested by:** Marco Olivo

- Include external `jsturtevant/copilot-codeact-plugin` only as an optional advanced tactic in repo recommendations.
- Scope the mention to Copilot CLI. Do not present it as baseline repo advice or a default setup.
- Mechanism framing: fewer replayed turns when multi-step tool chains collapse into one sandboxed execution; upside can grow in MCP-heavy sessions because tool catalogs replay fewer times.
- Claims stay bounded to mechanism plus the plugin README's benchmark tasks. No universal repo-endorsed savings numbers.
- Keep mentions short. Do not turn the repo docs into a plugin install guide.

### 2026-04-28: Repo Structure — Keep Docs-First Spine, Schedule Boundary Cleanup

**Author:** Leela | **Status:** Active

- Keep the current docs-first architecture. Do not do a substantial restructure now.
- Schedule a light reorganization pass focused on discoverability and boundary clarity before the repo accumulates more packaging or governance surfaces.
- Preserve the current core split: `docs/` as guide source of truth, `skills/` and `agents/` as reusable Copilot/package surfaces, and `mkdocs.yml` as minimal publish config.
- Cleanup priorities: one explicit repo architecture map, clearer distinction between shipped assets and internal operating surfaces, more legible docs numbering, and one canonical asset location.

### 2026-04-28: Repo Structure — Boundary Clarification Is Quality Work, Not Cosmetic

**Author:** Bender | **Status:** Active

- Treat repository-structure clarification as a quality and maintainability issue, not an aesthetic cleanup task.
- Current root mixes three materially different surfaces: public guide/MkDocs site, plugin or package artifacts, and internal squad/Copilot operating machinery.
- Taxonomy and packaging story must be made canonical across docs, local `skills/` names, lockfile references, and contributor guidance.
- Highest-value fixes are explicit ownership boundaries, one contributor-facing repo map, and one canonical packaging story. Renaming or moving files without that clarity is cosmetic.

### 2026-04-28: Repo Surface Cleanup — Remove Shipped Skills, Keep Agent + Docs Canonical

**Author:** Hermes | **Status:** Active | **Requested by:** Marco Olivo

- Remove the repo-shipped top-level `skills/` surface.
- Keep `agents/` as the only remaining packaged Copilot artifact.
- Keep `docs/assets/` as the canonical site asset location and delete the duplicate root asset copy.
- Renumber late Part 4 guide files from `13/14` to `11/12` so chapter filenames are contiguous again.
- Cleanup stays semantic, not just structural: docs and plugin metadata must stop advertising shipped installable skills.
- Validation target stays bounded: live `rg` and filesystem checks must pass; strict MkDocs build remains desirable but may be blocked if `mkdocs` is unavailable.

### 2026-06-17: Token Recommendations Placement

**Author:** Hermes | **Status:** Active | **Requested by:** Marco Olivo

- Placed RTK Windows caution in MCP/tool-cost sections, VS Code extension/profile and custom-agent guidance in MCP/practical setup, model-switch cache risk in model-pricing anti-patterns, and Copilot CLI AIC value-framing in habit-building maintenance.
- Each recommendation now sits beside the mechanism it affects, avoiding a new page and keeping README changes limited to high-impact quick-start nudges.

## Governance

- All meaningful changes require team consensus
- Document architectural decisions here
- Keep history focused on work, decisions focused on direction
