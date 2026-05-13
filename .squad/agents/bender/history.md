# Bender — History

## Core Context

- Project: caveman — living doc comparing GitHub Copilot token usage across techniques
- User: Marco Olivo
- Role: Validate methodology, review doc quality, challenge assumptions

## Learnings

### 2026-04-14: Cross-Agent Update — Review Assignment

- TOKEN-OPTIMIZATION-GUIDE.md (1107 lines) ready for review. Written by Hermes using Leela's outline + Farnsworth's data.
- Key areas to validate: savings percentages (projected, not measured), CJK myth-busting claims, technique completeness
- Guide references repo's own copilot-instructions.md as example — verify accuracy

### 2026-04-14: TOKEN-OPTIMIZATION-GUIDE.md Review — Complete

- **Verdict: APPROVE** with 3 editorial fixes applied directly.
- CJK tokens-per-character overstated: guide said "2-3 tokens/char" but own data shows ~1-1.4. The "2-3" is UTF-8 bytes, not tokens. Fixed.
- Source #14 "Baloney, T." was mangled blog handle, not real name (Anthony Shaw). Fixed.
- Cheat sheet CJK entry matched the wrong figure. Fixed.
- Savings percentages stack multiplicatively, not additively — guide doesn't explain this. Flagged as "should fix" suggestion.
- Farnsworth's careful hedging ("potentially more tokens") was simplified into absolutes ("2-3 tokens each") → factual error. Lesson: preserve source hedging when load-bearing.
- Guide is solid: well-structured, internally consistent (after fixes), practically useful, covers Leela's full outline, matches SKILL.md exactly.

### 2026-04-14: TOKEN-OPTIMIZATION-GUIDE.md Expansion Review — Complete

- **Verdict: APPROVE** with 2 fixes applied directly.
- §2.6 (AGENTS.md Problem): ETH Zurich findings accurately represented. Added missing study scope (138 tasks, 12 repos, 4 agents) for completeness. Sulat article coverage thorough — landmine metaphor, Osmani filter, Lulla counterpoint, all four hurt-mechanisms (redundancy/attention/anchoring/signal-noise) properly explained.
- §2.7 (MCP Server Costs): Token estimates (100-500/tool) match Farnsworth source data. Before/after audit table internally consistent with 18K measurement. Practical config guidance actionable.
- §4.5 (Agent Mode Config): Mode comparison, internal loop explanation, decision framework all well-structured. Settings references plausible.
- Technique matrix I1 "20-23% total" was misleading for pruning (only accurate for LLM-generated file removal). Fixed to "Variable (file size)". I2 kept at 20-23% (accurate).
- Quick Start items #6 and #7 appropriately concise, sources properly added (#18-#22).
- All new sections match existing style/format conventions.
- Review logged: `.squad/decisions/inbox/bender-review-expansion.md`

### 2026-04-14: Cross-Agent Update (Guide Expansion)

- Hermes expanded guide 1107→1486 lines. 3 new sections: §2.6 AGENTS.md, §2.7 MCP costs, §4.5 Agent mode config.
- Reviewing concurrently. Key areas: MCP token estimates (empirical, not peer-reviewed), AGENTS.md ETH Zurich study claims, new technique matrix rows.
- Previous review lesson applies: check if Farnsworth hedging preserved or simplified into absolutes.

### 2026-04-27: README Quick Start Savings Column Review

- **Verdict: REJECT current column as written.** Column mixes incompatible units: output-only reductions, input-only reductions, total task/session savings, absolute token ranges, and billing discounts.
- Rows 1 and 2 are defensible only when labeled as output-token reductions. Rows 5 and 8 are defensible only as task-shape dependent directional savings, not headline percentages comparable to other rows.
- Rows 3, 4, 6, and 7 are especially risky in a single shared column because readers can overread them as total request savings even though they apply to instruction tokens, model-price multipliers, scoped context, or the user-prompt slice only.
- Core methodology problem: output tokens cost more per token, but total bill impact still depends on the input/output mix of the specific interaction. A 50% output reduction does not mean 50% total savings if output was a small share of tokens; likewise small input cuts can matter a lot in agent mode where context dominates.
- Recommended fix: replace the single `Savings` column with either `Primary Effect` plus `Scope`, or keep a savings field only as clearly-scoped directionality/confidence language (for example: `High confidence: cuts output tokens on code tasks`, `Variable: depends on context size and mode`).
- If percentages remain, every row needs explicit unit/scope labeling and a note that figures are not additive, not comparable across buckets, and not equal to total bill reduction.

### 2026-04-27: Cross-Agent Update — Leela Proposed Replacement Shape

- Leela solved the structural side of the same review problem: keep Quick Start action-ranked, but replace the mixed `Savings` field with mechanism-aware framing.
- Her proposed structure (`Primary Impact`, `Confidence`, optional scoped `Typical Effect`) is consistent with Bender's methodological guardrails and gives implementation direction without pretending to benchmark one common unit.

### 2026-04-27: README Quick Start Table Re-Review — Approved

- **Verdict: APPROVE.** `Primary Effect` plus `Scope` fixes the original comparability problem well enough for README use because the table no longer pretends every row is one shared savings metric.
- Rows 1, 2, 3, 5, 6, 8, and 9 are now scoped to a mechanism or workflow shape instead of implying total bill reduction. Row 7 is appropriately hedged as quality-first.
- Row 4 is the only billing-vs-token exception, but it is methodologically safe because it explicitly says `not a token reduction` and labels the effect as billing multiplier / paid-plan discount.
- The note under the table is sufficient for approval, but it would be even stronger if it added `not directly comparable across rows` or `some rows affect billing rather than raw token count`.

### 2026-04-27: Cross-Agent Update — Hermes Implemented Table Revision Cleanly

- Hermes implemented the README Quick Start table rewrite in the approved shape: `Primary Effect` plus `Scope`, with mechanism-aware row language.
- Strict MkDocs build passed after the README change, so no docs-structure regressions surfaced during review closure.

### 2026-04-28: Repository Structure Review — Complete

- **Verdict: REJECT current structure as the long-term maintainability baseline.** Content is strong, but repository boundaries are not explicit enough for contributors to know what is product, what is packaging, and what is internal team machinery.
- Highest-risk boundary problem: the repo currently presents itself as a docs site, a Copilot plugin package, and a squad-operated internal workspace at the same root with no authoritative map of ownership or intended contributor path.
- Taxonomy drift is now real, not cosmetic. Docs teach external `.agents/skills/...` installation and reference `caveman-*` skill names, while the packaged repo surface exposes local `skills/` entries named `token-budget`, `context-management`, `output-control`, and `mcp-tool-budget`; `skills-lock.json` still tracks `caveman-*` artifacts from another source.
- README removal of plugin-install guidance reduced misconception risk for readers, but it also left `plugin.json`, `skills/`, `agents/`, and `.github/plugin/marketplace.json` underexplained at the root. A newcomer cannot tell whether these are shipped assets, experiments, mirrors, or leftovers.
- Hidden internal surfaces add onboarding drag: `.squad/`, `.copilot/`, and `.github/agents/` are substantial systems with different audiences and ownership models, but there is no single repo-map document telling contributors what to touch, ignore, or treat as generated/internal.
- Improvement priority is structural clarity first, not renaming polish. Highest-value moves are explicit boundary documentation, one canonical packaging story, and one canonical skill taxonomy.

### 2026-04-28: Cross-Agent Update — Repo Structure Analysis Batch Logged

- Scribe recorded a parallel repo-structure analysis batch with Leela and Farnsworth.
- Bender owned the validation/risk lens: challenge weak structure assumptions, duplication risk, and layout choices that could mislead future edits.
- Leela covered reader-facing structure; Farnsworth covered factual repo inventory.
- Scribe later merged Bender's review decision with Leela's docs-first recommendation into `decisions.md`.
- Farnsworth's inventory findings corroborated the review concerns: mixed audiences at root, taxonomy drift across install surfaces, and duplicated asset ownership are real maintenance risks.

### 2026-04-28: Skills Removal Cleanup Review — Pre-Implementation Guardrails

- Cleanup has real hidden-breakage risk if Hermes removes `skills/` without also removing the package/install metadata that still advertises a shipped plugin surface. `plugin.json` and `.github/plugin/marketplace.json` both still describe the repo as "Skills and an agent" and point at `skills/`.
- Public docs still contain live install-surface claims. Highest-risk examples: README Part 4 says "install caveman skills"; `docs/10-practical-setup.md` has a full "Installing Skills from Source" section with `.agents/skills/<name>/SKILL.md`; `docs/04-context-management.md` and `docs/09-comparisons-data.md` still use skills as active taxonomy/examples.
- Taxonomy cleanup must be semantic, not only file deletion. If skills disappear, tables and guidance that currently distinguish `applyTo` vs skill vs MCP need replacement language or row removal; otherwise the guide teaches a feature the repo no longer ships.
- Asset duplication cleanup is safe only if published-doc ownership stays with `docs/assets/`. Prior history shows MkDocs needed `docs/assets/caveman-octocat.png` to emit `/assets/caveman-octocat.png`; deleting the wrong copy can silently regress the homepage image.
- Acceptance checks for Hermes: strict MkDocs build passes after cleanup; grep shows no remaining public references to repo-local skills/plugin install surfaces in README/docs/plugin metadata; only one canonical `caveman-octocat.png` remains and published path still resolves from the docs build.

### 2026-04-28: Cross-Agent Update — Hermes Cleanup Passed Live Guardrails

- Hermes completed the semantic cleanup, not just file removal: plugin metadata now advertises the guide + agent surface, repo docs no longer teach repo-local skill installation, and late Part 4 numbering is contiguous again.
- Live filesystem and `rg` checks satisfied the main acceptance criteria: no top-level `skills/`, no `skills-lock.json`, and one canonical image copy under `docs/assets/`.
- Remaining gap is environmental, not yet a content failure: strict MkDocs build still cannot be executed here because `mkdocs` is not installed.
