# Farnsworth — History

## Core Context

- Project: caveman — living doc comparing GitHub Copilot token usage across techniques
- User: Marco Olivo
- Role: Run experiments, measure tokens, gather data
- Known techniques to test: caveman-speak, English vs other languages

## Learnings

### 2026-04-14: Token Optimization Research Complete

Comprehensive research delivered to `.squad/decisions/inbox/farnsworth-research-findings.md`.

Key findings:
- **English is most token-efficient language.** Non-English costs 1.5-3x more tokens. CJK (Chinese/Japanese/Korean) = 1.7-2.4x English. Cyrillic/Hebrew = 2.5-3x+. Myth busted: writing prompts in Chinese does NOT save tokens.
- **Caveman-speak = highest ROI technique.** 40-75% savings, zero cost to implement. Removing articles/filler/hedging directly eliminates tokens.
- **Compound instruction compression is massive.** copilot-instructions.md loaded on EVERY interaction — compressing it saves tokens × every prompt.
- **Output control (code-only, diffs, format constraints) = 40-90% output savings.** Easy wins.
- **Agent Mode vs Ask Mode matters.** Agent = 3-10 internal calls per action. Ask = 1 call. Use Ask for simple questions.
- **8 categories cataloged, 28 techniques total.** Matrix with savings estimates, quality impact, and Copilot applicability (Chat/Inline/Coding Agent).
- **Wenyan (文言文) modes are creative but token-negative.** Fewer characters but more tokens due to multi-byte encoding + English-dominant tokenizer training.

Sources: 17 references from web research, academic papers, GitHub community, official docs.

### 2026-04-14: Cross-Agent Update

- Hermes incorporated all research data into TOKEN-OPTIMIZATION-GUIDE.md (1107 lines). Language comparison tables and technique matrix translated well to guide format.
- Hermes decision: kept wenyan as "demo only" — aligns with research finding. Good.
- Bender reviewing guide (in progress) — may surface data accuracy questions.

### 2026-04-14: MCP & Agent Mode Token Research

Delivered `.squad/decisions/inbox/farnsworth-mcp-agent-research.md`.

Key findings:
- **MCP tool definitions = 100–500 tokens each**, sent EVERY turn. Not cached. 10 servers = ~20,000 tokens overhead per turn.
- **Agent mode multiplier is massive.** 5-step task × 20K tool defs = 100K+ tokens just in tool overhead. Reducing to 2 servers saves ~54% per task.
- **copilot-instructions.md at 100 tokens vs 700 tokens** saves 25,000 tokens over 50 interactions (×5 agent steps each).
- **VS Code deferred tool loading** pattern reduces baseline — not all tools loaded eagerly. Custom agents with explicit `tools:` lists = massive savings.
- **Workspace-scoped MCP config** (`.vscode/mcp.json`) is key — project-specific servers, not global bloat.
- **Path-specific instructions** (`.github/instructions/`) load only for matching files — zero cost otherwise.
- **Current limitation:** Can't filter individual tools within an MCP server. Only enable/disable entire servers (GitHub Issue #7328).
- **12 actionable recommendations** produced for guide integration, ranging from quick wins to advanced techniques.

Sources: 8 references from MindStudio research, GitHub Blog, VS Code docs, GitHub community.

### 2026-04-14: Cross-Agent Update (Guide Expansion)

- Hermes integrated MCP research into §2.7 and §4.5. Token cost estimates and server audit table used directly.
- Hermes also wrote §2.6 (AGENTS.md) from task brief — cross-reference needed against delivered research.
- Bender reviewing expanded guide concurrently. May surface accuracy questions on MCP estimates.

### 2026-04-28: Repo Structure Analysis

- Repo has a strong primary spine for newcomers at the documentation layer: `README.md` -> `docs/index.md` -> numbered MkDocs chapters in `docs/`, with `mkdocs.yml` matching that sequence cleanly.
- Top-level packaging intent is less obvious than the docs intent. Public-facing `skills/`, `agents/`, `plugin.json`, and `skills-lock.json` suggest installable Copilot assets, but hidden `.github/skills`, `.github/agents`, and `.copilot/skills` create parallel surfaces a new contributor would not distinguish quickly.
- Concrete drift found in docs: `docs/10-practical-setup.md` and `docs/04-context-management.md` still describe `.agents/skills/<name>/SKILL.md`, while this repo's exposed install surface uses top-level `skills/` and `agents/` plus `plugin.json`.
- Contributor setup is thin. Docs build path exists (`requirements-docs.txt`, `.github/workflows/deploy-pages.yml`), but local bootstrap is not obvious from repo root; running `python3 -m mkdocs build --strict` failed locally because `mkdocs` was not installed.
- Orphan/duplication signal: `assets/caveman-octocat.png` and `docs/assets/caveman-octocat.png` duplicate the same apparent artifact across two roots without clear ownership.

### 2026-04-28: Cross-Agent Update — Repo Structure Analysis Batch Logged

- Scribe recorded a parallel repo-structure analysis batch with Leela and Bender.
- Farnsworth owned the factual inventory lens: concrete repo surfaces, layout splits, and evidence-first structure mapping.
- Leela covered reader-facing structure; Bender covered structure-risk review.
- Scribe later merged Leela's docs-first boundary-cleanup decision and Bender's boundary-risk review into `decisions.md`.
- Farnsworth's concrete findings supported both directions: root-level audience mixing, docs/package taxonomy drift, and duplicated asset ownership all showed up in the repo scan.

### 2026-04-28: Cross-Agent Update — CodeAct Mention Uses MCP Replay Logic

- Hermes added a bounded recommendation for external plugin `jsturtevant/copilot-codeact-plugin` as an optional advanced Copilot CLI tactic.
- Rationale matches MCP research: collapsing multi-step tool chains into one execution can reduce how often system/context/tool definitions replay.
- Framing stayed disciplined: no universal savings number, no repo-owned benchmark claim, and stronger upside only as a context-dependent possibility in MCP-heavy sessions.
