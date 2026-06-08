# Token Optimization Guide for GitHub Copilot

[English](README.md) | [繁體中文（台灣）](README.zh-TW.md)

> [!IMPORTANT]
> **This is not official GitHub or Microsoft guidance.** This guide is a community resource born from real-world field experience — patterns observed, techniques tested, and lessons learned by practitioners adopting AI for development purposes. It reflects industry backspark: practical knowledge gathered from the ground up, not top-down product documentation. Use it to inform about optimization strategies, and adapt what works for the context of your customer. Official guidance lives at [docs.github.com/copilot](https://docs.github.com/copilot).

> A practical, data-driven guide to reducing token consumption while maintaining code quality.
> Covers Chat, Inline, and Coding Agent workflows.

---

## Quick Start — 12 Things to Do Right Now

> **June 1, 2026 — Usage-Based Billing (UBB) is live.** GitHub Copilot now bills real tokens (input + output + cached) drawn from pooled AI credits ($30/seat Business, $70/seat Enterprise) instead of request counters. Every technique in this guide translates directly into credit savings — and cache-friendly habits matter more than ever. See [Enterprise Governance](docs/12-enterprise-governance.md) for customer guardrails and [Model Selection & Pricing](docs/11-models-and-pricing.md) for model-cost guidance.

> **Output tokens cost much more than input tokens.** That's the most important pricing fact in this guide. Anthropic's public pricing makes the asymmetry concrete ($1/$5 Haiku, $3/$15 Sonnet, $5/$25 Opus per MTok input/output). Copilot's exact per-model UBB pricing table is not public yet, but UBB still makes verbose output disproportionately expensive. Most input tokens come from file context, history, and tool schemas — not from what you type. Your typed prompt is a tiny fraction of total input. Start with output control, then tackle structural input wins.

Don't have time to read the full guide? Do these today and cut your token usage:

| # | Action | Primary Effect | Time to Set Up |
|---|--------|----------------|----------------|
| 1 | **Request code-only responses** — add `Code only, no explanation.` to `copilot-instructions.md`. Highest per-token ROI: output costs 5× more than input, and this cuts 40-70% of output on every code task, permanently | Shrinks response length | 0 minutes |
| 2 | **Constrain output format by default** — add `Bullets over paragraphs. No explanations unless asked.` to `copilot-instructions.md` | Keeps answers terse | 0 minutes |
| 3 | **Shrink your always-on context** — compress `copilot-instructions.md` AND prune `AGENTS.md` to landmines only. Every token in either file is billed on every interaction (and every agent step). Strip filler, delete anything the agent discovers by reading code, delete LLM-generated `/init` boilerplate | Reduces always-on input/context | 15 minutes |
| 4 | **Default to Auto model selection** — use Auto as the baseline because it chooses from the supported Auto pool and gives a paid-plan discount. Pin higher-cost models manually when a task clearly justifies them. See [Model Selection & Pricing](docs/11-models-and-pricing.md) | Lowers billed rate on eligible usage | 0 minutes |
| 5 | **Use Ask Mode for simple questions** — reserve Agent Mode for multi-step tasks | Avoids agent overhead | 0 minutes (just choose the right mode) |
| 6 | **Scope context with `applyTo:` paths** — split one large instructions file into small scoped ones that load only when relevant | Reduces always-on input/context | 15 minutes |
| 7 | **Be precise in your prompts** — "Add null check to `getUser()`" not "Can you please look at this and maybe add some error handling?" Note: your typed prompt is a small fraction of total input; precision matters more for quality than for raw token savings | Improves task targeting | 0 minutes |
| 8 | **Retune prompts to the target model** — provider prompting guides change by model/version. Paste the official guide URL into Copilot and ask it to adapt `.github/copilot-instructions.md`, agent profiles, or app prompts for the model you actually use | Reduces rework | 10 minutes per model change |
| 9 | **Audit your MCP servers** — disable servers you're not using; each costs ~100-500 tokens per agent step | Removes tool/schema overhead | 5 minutes |
| 10 | **Convert rich files to Markdown before AI work** — `.docx`, `.pdf`, `.pptx`, `.xlsx`, HTML, images, audio, video, and ZIPs carry format tax. [Marc Bara's writeup](https://medium.com/@marc.bara.iniesta/your-docx-is-wasting-33-of-your-ai-budget-86a3d229d042) shows the cost; use [Microsoft MarkItDown](https://github.com/microsoft/markitdown) before chat, agent, or RAG ingestion | Reduces noisy input context | 5 minutes |
| 11 | **Run `/chronicle improve` weekly** (**Copilot CLI only**, experimental) — this slash command works in interactive Copilot CLI sessions, not as a general Copilot Chat feature. It finds recurring confusion in your CLI session history and generates custom-instruction fixes so the same misread intent stops costing tokens forever | Cuts recurring rework | 2 minutes per run |
| 12 | **Try CodeAct for long tool chains** (**Copilot CLI only**, optional external plugin) — [`copilot-codeact-plugin`](https://github.com/jsturtevant/copilot-codeact-plugin) collapses multi-step tool chains into one sandboxed execution, which can reduce repeated replay of system prompt, prior messages, and tool definitions | Reduces tool-loop replay | 10-15 minutes |

**Looking at this from an enterprise or customer-governance angle instead of an individual setup angle?** Start with [Enterprise Governance](docs/12-enterprise-governance.md). That chapter covers AI-credit budgets, per-user tightening, model-access policy, org instructions, and separate-organization tradeoffs.

*Figures above are scoped to the mechanism named in each row, are not additive, and do not equal total bill reduction.*

Output control (#1, #2) pays off immediately and compounds — set it once, save on every call. Structural input control (#3, #6) compounds across every interaction. Model routing (#4, #5) reduces cost at the billing tier. Model-specific prompt tuning (#8) cuts waste by improving first-pass quality. MCP audit (#9) eliminates thousands of hidden tokens per agent task. Markdown conversion (#10) removes DOCX/PDF/HTML layout noise before the model ever sees it.

---

## Guide Contents

### Part 1: Why Tokens Matter

Understand BPE tokenization, why tokens matter for cost/speed/limits, and how GitHub Copilot uses tokens behind the scenes.

→ **[Read Part 1](docs/01-why-tokens-matter.md)**

---

### Part 2: The Techniques

#### [2.1 Prompt Compression](docs/02-prompt-compression.md)

Caveman-speak, intensity levels (lite/full/ultra), structured formats, abbreviations, and code-centric prompting. 30-50% input token savings; combine with output control (2.4) for output savings.

#### [2.2 Language Comparison](docs/03-language-comparison.md)

Data-backed comparison: English is the most token-efficient language in these examples. CJK costs 1.7-2.4x more. Includes tokenization tables for 8 languages.

#### [2.3 Context Management](docs/04-context-management.md)

Compress system instructions, compress memory files, scope context with `applyTo`, close unused editor tabs, convert non-text files to Markdown before AI work, configure Content Exclusion (Business/Enterprise admins), start fresh conversations. Control what gets sent to the model.

#### [2.4 Output Control](docs/05-output-control.md)

"Code only, no explanation." Constrain response format. Set terse output as project default.

#### [2.5 Workflow Optimization](docs/06-workflow-optimization.md)

Terse commit messages, one-line PR reviews, Ask vs Agent mode selection, model-specific prompt tuning, and when NOT to compress.

#### [2.6 The Always-On Context Problem](docs/07-agents-md-problem.md)

Research on LLM-generated context files suggests they often hurt agent correctness while inflating token cost. The same lesson applies to both `AGENTS.md` and `.github/copilot-instructions.md` — they are distinct conventions (different filenames, different historical owners) that nonetheless function as always-on context for Copilot today. Apply the "landmines only" approach to whichever file(s) your repo uses. Treat context files like a bug tracker, not a wiki.

#### [2.7 MCP & Tool Costs](docs/08-mcp-tool-costs.md)

The hidden token tax: each MCP tool costs 100-500 tokens per agent step. 15 servers × 15 steps = 265K tokens of overhead. Audit guide included.

---

### Part 3: Comparisons & Data

Head-to-head prompt comparisons, language tokenization tables, the complete technique-by-technique matrix (40+ techniques), and quality impact assessment with the diminishing returns curve.

→ **[Read Part 3](docs/09-comparisons-data.md)**

---

### Part 4: Practical Setup

Step-by-step: configure Copilot, optimize the Coding Agent, configure agent mode, and build the habit. Includes VS Code settings, decision frameworks, and a 4-week adoption plan.

→ **[Read Part 4](docs/10-practical-setup.md)**

---

### Part 4.2: Model Selection & Pricing

Dedicated page on models, PRU-era multiplier history, current Auto guidance, plan availability, and where vendor input/output token pricing fits while Copilot's exact per-model UBB table remains unpublished. Includes links to the official GitHub Docs pages for Auto model selection, billing, and plan/model availability.

→ **[Read Part 4.2](docs/11-models-and-pricing.md)**

---

### Part 4.3: Enterprise Governance

Dedicated chapter for customer-facing admin guidance: usage-based billing guardrails, AI-credit budgets, per-user tightening, model-access policy, org-level instructions, and when separate organizations are worth the overhead.

→ **[Read Part 4.3](docs/12-enterprise-governance.md)**

---

Need the glossary, quick terms, tools, or core external links? Go to [Guide Home](docs/index.md).

---

## Highest-Impact Techniques

Ranked by cost impact. Output first — it costs 5× more per token than input.

1. **Output control** — "Code only, no explanation" + terse default in `copilot-instructions.md`. 40-70% output savings on code tasks, 30-60% across all interactions. One instruction, permanent.
2. **Shrink always-on context** (`copilot-instructions.md` + `AGENTS.md`) — compress filler, prune to landmines only, delete LLM-generated boilerplate. Compounds on every interaction and agent step; 20-23% agent-task reduction plus better correctness
3. **Ask Mode for simple questions** — 60-90% savings by avoiding Agent overhead
4. **Audit MCP servers** — disable unused servers, save 5K-190K tokens per agent task
5. **Auto model selection** — lower-cost default routing plus paid-plan discount on eligible usage, zero effort
6. **Convert rich files to Markdown first** — avoid paying for Word/PDF/HTML layout noise in chat, agent, and RAG workflows
7. **Retune prompts to the target model** — better first-pass output reduces repeated clarification turns
8. **Precise prompts** — 20-40% of user-prompt input tokens; more important for quality than raw savings

---

*This is a living document. As tokenizer technology evolves, model capabilities change, and new techniques emerge, this guide will be updated. Check the repository for the latest version.*
