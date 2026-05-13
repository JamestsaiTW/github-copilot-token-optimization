# 2.6 The Always-On Context Problem — Why Less Is More

[← Back to Guide](index.md)

---

> **Distinct conventions, shared cost profile.** `AGENTS.md` (cross-tool convention), `.github/copilot-instructions.md` (Copilot-native), and `CLAUDE.md` (Claude Code convention) are **different files with different historical owners and different scopes** — they are not interchangeable, and a repo can legitimately use more than one. What they share is the cost dynamic this section is about: each functions as **always-on context**, loaded into every interaction by the tool that reads it. The research below was performed on `AGENTS.md`, but the underlying mechanism (redundant context dilutes attention and inflates token cost) applies to any always-on instruction file. Apply the pruning guidance below to whichever file(s) your repo uses, and the compression guidance in [Part 2.3](04-context-management.md) likewise.

## 2.6.1 The Research: Context Files Often Hurt

A persistent assumption in AI-assisted development: more context = better results. Write a detailed `AGENTS.md`, `copilot-instructions.md`, or `CLAUDE.md` — or run `/init` to generate one — and the agent performs better.

**The ETH Zurich study (Gloaguen et al., AGENTBENCH, Feb 2026) tested this at scale: 138 tasks across 12 repositories, 4 different coding agents.** The results:

| Finding | Data |
|---------|------|
| LLM-generated context files hurt performance | Declined in 5/8 experimental settings |
| Average correctness change | **−2%** on AGENTBENCH |
| Cost increase with LLM-generated context | **20-23%** more tokens burned |
| GPT-5.2 reasoning overhead | **22%** more reasoning tokens with context file |

That's not "neutral." LLM-generated context files actively make agents worse while costing more.

## 2.6.2 Human-Written Files: Marginal at Best

Human-written context files performed slightly better — but not consistently:

| Model | Effect of Human-Written Context File |
|-------|--------------------------------------|
| Average across models | ~4% improvement (inconsistent) |
| Claude Code | **Worse** with human-written context |
| File discovery rates | Identical with or without context files |

The last point is important: agents find the same files regardless. The context file doesn't help them navigate — they already know how to `ls` and `grep`.

## 2.6.3 Why More Context Hurts

Four mechanisms explain the findings:

**1. Redundancy tax.** LLM-generated context files contain information the agent discovers by reading code. The agent reads your `package.json`, your imports, your directory structure — and then reads the context file that says the same things. Double the tokens, zero new information.

**2. Attention tax.** LLMs have U-shaped attention: they attend strongly to the beginning and end of context, but the middle gets lost (Liu et al., "Lost in the Middle," 2023). A 200-line `AGENTS.md` means the guidelines in lines 50-150 get ignored. Your most important rules are the ones most likely to be skipped.

**3. Anchoring trap.** Agents follow context file instructions too faithfully — even outdated ones. If your `AGENTS.md` mentions a specific tool, agents use it **1.6x more** than they otherwise would, even when another tool is better for the task.

**4. Signal-to-noise ratio.** Every token of context competes for the model's attention. Low-value context (routine facts like "this project uses TypeScript" when `tsconfig.json` exists) dilutes the high-value context (project-specific cautions like "don't refactor the auth module — it has a pending security audit").

## 2.6.4 The Counterpoint: Efficiency vs. Correctness

Lulla et al. (Jan 2026) found human-written `AGENTS.md` **reduced runtime 29%** and **output tokens 17%**. That sounds great — until you read the methodology.

They measured **efficiency**, not **correctness**. Context files help agents navigate faster. They don't help agents arrive at the right answer.

The distinction matters: a faster wrong answer is still wrong. And the 17% token reduction from faster navigation is offset by the 20-23% cost increase from processing the context file itself.

## 2.6.5 What to Actually Put in Context Files

Addy Osmani's filter (Google, 2026):

> **"Can the agent discover this on its own by reading your code? If yes, delete it."**

What survives this filter:

| Keep | Delete |
|------|--------|
| "Use `uv` instead of `pip`" | "This is a Python project" |
| "Run tests with `--no-cache`" | "Tests are in the `tests/` directory" |
| "Don't refactor the auth module" | "We use JWT for authentication" |
| "Deploy requires VPN connection" | "Main branch is protected" |
| "DB migrations must run in order" | "We use PostgreSQL" |

**The pattern:** Keep only **landmines** — things that look normal but cause mistakes. Delete everything discoverable.

## 2.6.6 The Ideal: Treat It Like a Bug Tracker

```text
Start with almost empty file.
Agent trips on something → add one line.
Root cause gets fixed → delete that line.
```

Your context file should grow and shrink like a bug tracker, not accumulate like a wiki. If it's only getting longer, you're doing it wrong.

## 2.6.7 This Repo's Approach: 6 Lines, ~50 Tokens

This project's `.github/copilot-instructions.md`:

```text
Terse like caveman. Technical substance exact. Only fluff die.
Drop: articles, filler (just/really/basically), pleasantries, hedging.
Fragments OK. Short synonyms. Code unchanged.
Pattern: [thing] [action] [reason]. [next step].
ACTIVE EVERY RESPONSE. No revert after many turns. No filler drift.
Code/commits/PRs: normal. Off: "stop caveman" / "normal mode".
```

**6 lines. ~50 tokens.** Loaded every interaction.

Compare with typical `/init` output: **200+ lines, ~1,500 tokens.** That's 1,450 tokens of waste on every single interaction — and per the research, it likely makes the agent perform *worse*.

**The math over a session:**

| Context File Style | Tokens per Load | 50 Interactions | Agent (20 steps) |
|-------------------|:--------------:|:---------------:|:----------------:|
| `/init` generated (200 lines) | ~1,500 | 75,000 | 30,000 |
| Typical hand-written (50 lines) | ~400 | 20,000 | 8,000 |
| Caveman-compressed (6 lines) | ~50 | 2,500 | 1,000 |
| **Savings (caveman vs /init)** | **1,450** | **72,500** | **29,000** |

---

**Next:** [MCP & Tool Costs →](08-mcp-tool-costs.md)
