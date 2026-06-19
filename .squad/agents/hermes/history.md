# Hermes — History

## Core Context

- Project: caveman — living doc comparing GitHub Copilot token usage across techniques
- User: Marco Olivo
- Role: Maintain the living document, write clear comparisons
- Doc format: Markdown, structured comparisons with data from experiments

## Learnings

### 2026-06-19: Governance Cohorts and FinOps Automation

- Updated `docs/12-enterprise-governance.md` with spend-cohort guidance: export historical Copilot billing/usage CSVs, upload to Copilot Billing Preview, then map power/high/baseline/low usage cohorts to budget defaults and review paths.
- Added `amgdy/copilot-finops-automation` as an admin-scale option for Copilot FinOps-as-code: reviewed YAML config, schema validation, dry runs, idempotent budget apply, cost-center membership sync, audit reports, and private-config caveat.
- Made a tiny `README.md` guide-summary update so Enterprise Governance mentions spend cohorts and FinOps-as-code automation.


### 2026-06-17: Placement for Tool, Profile, Model-Switch, and AIC Recommendations

- Added RTK Windows caveat beside existing RTK setup, not as a new technique. Readers need the warning where they copy commands.
- Extension/profile cleanup belongs with MCP/tool costs and practical agent setup because extension-injected tools behave like hidden context surface.
- Model mid-chat switching belongs in model-pricing anti-patterns with careful cache/history wording; avoid claiming fixed implementation internals.
- Copilot CLI AIC counter fits habit-building/monthly maintenance: value framing is a behavior loop, not a setup prerequisite.

### 2026-04-14: Wrote TOKEN-OPTIMIZATION-GUIDE.md (v1)

- 1107 lines. Followed Leela's outline (5 parts), filled with Farnsworth's data.
- CJK myth-busting section works well with side-by-side tables — numbers speak louder than arguments.
- Caveman intensity level examples (lite/full/ultra) need real prompts, not abstract descriptions. Show the same question at each level.
- The technique matrix from Farnsworth translates well to markdown tables. Added "Big Winners" callout beneath for scanners.
- Quick Start section at top is critical — most readers won't read 1100 lines. 5 actions, table format, estimated savings.
- Referenced repo's own `copilot-instructions.md` as real-world example — gives the guide credibility since it practices what it preaches.
- Decision: kept wenyan in guide for completeness but clearly labeled "demo only, not recommended for savings." Data backs this.
- ASCII art for context window diagram and savings-vs-quality curve adds visual breaks in a text-heavy doc.
- Sources section pulled directly from Farnsworth — 17 references, all with attribution.

### 2026-04-14: Cross-Agent Update

- Guide sent to Bender for review (in progress). Expect feedback on methodology claims and data accuracy.
- Leela's experiment framework not yet executed — guide contains projected savings ranges, not measured. Future work.

### 2026-04-14: Expanded TOKEN-OPTIMIZATION-GUIDE.md (v2) — Three New Major Sections

- Added §2.6 "The AGENTS.md Problem — Why Less Context Is More" — synthesized ETH Zurich AGENTBENCH study (Gloaguen et al.), Lulla et al. counterpoint, Osmani's filter, Liu et al. attention research. Key takeaway: LLM-generated context files hurt performance in 5/8 settings, cost 20-23% more tokens. Human-written barely help. Only "landmines" belong in context files.
- Added §2.7 "Tool & MCP Server Costs — The Hidden Token Tax" — quantified MCP tool definition costs (~100-500 tokens/tool), showed multiplication problem (15 servers = 265K tokens/task vs 3 servers = 75K), included before/after audit table and per-workspace MCP config guidance.
- Added §4.5 "Configuring Agent Mode for Efficiency" — documented agent internal loop (context reload per step), mode comparison (Ask/Edit/Agent cost profiles), step minimization techniques, VS Code settings (maxTurns), custom instruction directives.
- Updated: TOC, Quick Start (5→7 items), Technique Matrix (+12 new rows across 4 new categories), Big Winners (5→7), Glossary (+2 terms), Sources (+5 references).
- Farnsworth's MCP research file not yet in inbox — used task brief + own knowledge. Will cross-reference when available.
- The AGENTS.md section is the most opinionated part of the guide. The research backing is solid (peer-reviewed + replicated) but the "6 lines vs 200 lines" framing is this repo's own position. Flagged in decisions file.

### 2026-04-14: Cross-Agent Update (Guide Expansion)

- Farnsworth delivered MCP research to inbox. Data aligned with estimates used in §2.7.
- Bender reviewing expanded sections concurrently. Previous review found CJK tokens-per-char error — watch for similar precision issues in new MCP estimates.
- Bender suggestion: explain multiplicative savings stacking. Future edit candidate.

### 2026-04-22: Plugin Section Rewrite — Clarified Static vs Runtime

- Rewrote "Install as a Copilot CLI Plugin" → "Install the Plugin — Behavioral Rules, Not a Compression Engine"
- Root cause: readers assumed plugin runs an LLM to compress prompts at runtime ("what's the point of compressing LLM with an LLM?")
- Fix: added blockquote "What this is NOT" callout, explained skills are static markdown files with description-match triggering, added "What it does" column to component table, clarified zero overhead when idle
- Updated "Two ways to use this repo" table: changed install description from "bakes techniques into every session" to "Pre-authored behavioral rules that make Copilot terse by default", fixed anchor link
- Kept all install commands and details section unchanged
- Tone matched: direct, practical, no hedging

### 2026-04-22: Removed Plugin/Install Documentation from README

- Removed "Two ways to use this repo" section (bifurcation table + "You can do both" line)
- Removed entire "Install the Plugin — Behavioral Rules, Not a Compression Engine" section (~75 lines: install commands, component table, agent usage, collapsible details)
- Plugin files (`plugin.json`, skills/, agents/) remain in repo — only documentation removed
- No transition sentence needed: intro blockquote → `---` → Quick Start reads naturally
- Reason: Marco requested removal of plugin documentation from README

### 2026-04-27: README Quick Start Table — Scoped Effect Labels

- Replaced the Quick Start `Savings` column with `Primary Effect` and `Scope` to stop mixing incompatible units in one field.
- Reframed rows by mechanism: output rows keep explicit output-token ranges; context rows now talk about always-on input/context load; Auto model selection now describes billing discount rather than token reduction.
- Ask vs Agent and MCP audit now read as per-task/workflow effects, not universal savings; prompt precision stays quality-first with only a light token note.
- Added a one-line note below the table that figures are scoped, non-additive, and not equal to total bill reduction.

### 2026-04-27: Cross-Agent Update — Bender Approved Revised Quick Start Table

- Bender re-reviewed the revised README Quick Start table and approved the `Primary Effect` + `Scope` structure as methodologically safe for README use.
- Reviewer caveat: the note under the table is good enough now, but could be strengthened later with explicit wording that rows are not directly comparable and some rows affect billing rather than raw token count.
- Validation passed: strict MkDocs build stayed green after the README table update.

### 2026-04-27: Homepage Image Restored for GitHub Pages

- Homepage hero image was missing because the published MkDocs homepage had no live image reference and the PNG only existed in the repo root `assets/`, not the doc source tree.
- Cheap check that disconfirmed GitHub Pages publishing the asset: strict build output initially had no `caveman-octocat.png` file.
- Fix: copied the PNG into `docs/assets/`, restored a homepage image reference in `docs/index.md`, and added one small centering rule in `docs/stylesheets/extra.css`.
- Validation: strict MkDocs build passed and built site now includes `/assets/caveman-octocat.png`.

### 2026-04-28: Added CodeAct as Advanced CLI-Only Token Tactic

- Added a bounded recommendation for external plugin `copilot-codeact-plugin` in README Quick Start surface and supporting docs.
- Framing kept narrow: optional, advanced, Copilot CLI only, external to this repo.
- Main explanation lives in workflow optimization: fewer turns means less replay of system prompt, prior messages, and tool definitions; effect can compound when MCP servers are loaded.
- Claims limited to mechanism plus plugin README benchmark language. No repo-owned universal savings claim added.
- Practical setup mention kept short and explicitly non-install-guide.

### 2026-04-28: Cross-Agent Update — Validation Boundaries on CodeAct Mention

- `get_errors` stayed clean for `docs/06-workflow-optimization.md` and `docs/08-mcp-tool-costs.md` after the CodeAct update.
- `README.md` and `docs/10-practical-setup.md` still carry unrelated pre-existing markdown-style warnings; not caused by the CodeAct edit.
- Strict MkDocs validation could not run in this environment because `mkdocs` is not installed.
- Farnsworth's MCP replay-cost research remains the supporting rationale for why turn-collapsing tactics can matter more in MCP-heavy sessions.

### 2026-04-28: Removed Repo-Shipped Skills Surface, Fixed Taxonomy Drift

- Removed docs and metadata that presented this repo as shipping installable skills. Kept the guide's generic advice about on-demand workflow guidance, but detached it from repo packaging.
- Practical Setup section now says this repo no longer ships installable skills and reframes the advice around keeping occasional checklists or prompt snippets out of always-on context.
- Renumbered late guide chapter filenames from `13/14` to `11/12` so Part 4 is contiguous again. Updated README, MkDocs nav, and doc cross-links to match.
- Canonical asset location stays `docs/assets/`. Root `assets/` copy became redundant once the site source owned the file.
- Repo packaging metadata kept minimal: agent surface remains, obsolete skill lockfile does not.

### 2026-04-28: Cross-Agent Update — Cleanup Accepted Under Bender Guardrails

- Bender's pre-implementation review correctly identified the risky surfaces: stale plugin metadata, docs that still taught repo-local skills, and the published homepage asset path.
- Cleanup closed those risks on live files: install-surface claims were removed from README/docs/plugin metadata and only `docs/assets/caveman-octocat.png` remains.
- Validation boundary stayed narrow but real: filesystem and `rg` checks passed, while strict MkDocs build could not run because `mkdocs` is not installed in this environment.
