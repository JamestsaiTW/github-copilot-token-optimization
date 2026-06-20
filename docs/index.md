# Token Optimization Guide

Practical guide to reducing GitHub Copilot token spend while keeping answers and code useful.

[Start with Part 1](01-why-tokens-matter.md){ .md-button .md-button--primary }
[Jump to Practical Setup](10-practical-setup.md){ .md-button }

## What This Covers

- Why token usage actually costs money under Usage-Based Billing
- Why output control usually beats prompt compression on raw ROI
- How to shrink always-on context, history, and tool overhead
- How model-specific prompt guides improve first-pass quality and reduce rework
- When Ask Mode, Edit Mode, and Agent Mode make financial sense
- How to set enterprise guardrails without relying on unsupported controls
- How to turn this repo into repeatable team habits

## Fastest Wins

1. Constrain output by default: `Code only, no explanation.` and `No explanations unless asked.`
2. Keep `.github/copilot-instructions.md` small and specific.
3. Protect cache in long sessions: keep `{model, active MCP set, active agent/profile}` stable; if you must switch, start a fresh chat with a short handoff summary.
4. Use Ask Mode for questions that do not need tools.
5. Retune prompts and instructions against the official guide for your target model.
6. Disable MCP servers you are not using.
7. Convert DOCX/PDF/Office/media inputs to Markdown before AI work; start with [MarkItDown](https://github.com/microsoft/markitdown).
8. Audit long-running agent sessions and repeated back-and-forth.
9. Install [RTK](https://github.com/rtk-ai/rtk) — CLI proxy that filters `git`, test runners, `grep`, and 100+ other shell commands before output reaches the agent. One install, 60-90% savings on tool-call results in agent and coding-agent sessions.

## Read by Topic

### Foundations

- [Why Tokens Matter](01-why-tokens-matter.md)
- [Comparisons & Data](09-comparisons-data.md)

### Techniques

- [Context Management](04-context-management.md)
- [Output Control](05-output-control.md)
- [Workflow Optimization](06-workflow-optimization.md)
- [MCP & Tool Costs](08-mcp-tool-costs.md)

### Implementation

- [Practical Setup](10-practical-setup.md)
- [Model Selection & Pricing](11-models-and-pricing.md)
- [Enterprise Governance](12-enterprise-governance.md)

## Quick Terms

- **UBB**: usage-based billing. Copilot Business and Enterprise spend is tracked through AI-credit usage rather than request counters.
- **AI credits**: the pooled billing unit used after the cutover.
- **Auto mode**: Copilot's default model selector. Good default lane when you do not need to pin a model.
- **Ask Mode**: single-shot interaction. Lowest-overhead choice for simple questions.
- **Agent Mode**: multi-step interaction. Higher leverage, higher cost.
- **Content Exclusion**: admin control for keeping selected repo content out of Copilot context.
- **Format tax**: extra tokens from rich file metadata and layout noise in DOCX, PDF, HTML, slides, spreadsheets, images, and audio/video extraction. Convert to Markdown first.

## Useful Links

- [Official GitHub Copilot docs](https://docs.github.com/copilot)
- [Usage-based billing for organizations and enterprises](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-organizations-and-enterprises)
- [OpenAI Tokenizer](https://platform.openai.com/tokenizer)
- [Awesome GitHub Copilot Customizations](https://github.com/github/awesome-copilot-customizations)
- [LLMLingua](https://github.com/microsoft/LLMLingua)
- [Caveman project](https://github.com/JuliusBrussee/caveman)
- [RTK — Rust Token Killer](https://github.com/rtk-ai/rtk)
- [Microsoft MarkItDown](https://github.com/microsoft/markitdown) — convert PDF, Office files, images, audio, HTML, ZIP contents, YouTube URLs, EPUBs, and more to Markdown for LLM workflows
- [Marc Bara: "Your .docx Is Wasting 33% of Your AI Budget"](https://medium.com/@marc.bara.iniesta/your-docx-is-wasting-33-of-your-ai-budget-86a3d229d042)
- [Dina Berry: "How I Cut Token Usage from 52% to 13%"](https://dfberry.github.io/2026-05-06-tuning-up-copilot-context) — real measured numbers from a Copilot CLI production setup (Microsoft/GitHub content contributor)

## Notes

- `/chronicle` (full, all subcommands) is **Copilot CLI**. `/chronicle:tips` is also available in **VS Code**.
- Usage-Based Billing is labeled **UBB** in this repo.
