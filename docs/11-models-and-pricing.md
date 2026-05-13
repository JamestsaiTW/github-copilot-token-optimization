# Model Selection & Pricing

[← Back to Guide](index.md)

---

This page exists because model advice in token-optimization discussions gets mixed together too easily. There are **three different pricing views** in play:

1. **GitHub Copilot public docs** — model availability by plan, Auto behavior, and whatever relative pricing signals GitHub has published
2. **This repo's UBB framing** — how to think about the June 1, 2026 usage-based billing shift for Business and Enterprise: AI-credit metering and budgets by enterprise, org, cost center, and user
3. **Vendor API pricing** — per-token pricing from providers like Anthropic, where input and output are billed differently

Do **not** treat these as identical units. Use each for the question it actually answers.

## The Official GitHub Docs You Want

- [About Copilot auto model selection](https://docs.github.com/en/copilot/concepts/auto-model-selection)
- [Requests in GitHub Copilot](https://docs.github.com/en/copilot/concepts/billing/copilot-requests)
- [Plans for GitHub Copilot](https://docs.github.com/en/copilot/get-started/plans)

Those three pages cover almost everything a practitioner needs today:

- which models exist
- which plans include them
- which models are free vs premium on paid plans
- which models are currently documented as cheaper or more expensive relative to others
- what Auto actually does

One timing point matters for the rest of this page: usage-based billing for Copilot Business and Copilot Enterprise starts on **June 1, 2026**. After that date, AI-credit usage is the main billing lens for Business and Enterprise governance. Any premium-request language below should be read as legacy transition context only.

## The Most Important Clarification About Auto

The repo already recommends **Auto** as the default, and that is still directionally right. But the official GitHub docs are more specific than the repo previously was.

### What Auto actually does

Per [About Copilot auto model selection](https://docs.github.com/en/copilot/concepts/auto-model-selection):

- Auto chooses from the **supported Auto pool**, subject to your plan and org policies
- Auto selection is based on **real-time system health and model performance**
- On paid plans, Auto in Copilot Chat gets a **10% discount**
- Auto stays in the supported default pool rather than escalating into every premium model

That last point matters.

> **Practical consequence:** Auto is not "pick any model, including the expensive ones, when needed." It is a low-friction default across the supported Auto set. If you want a higher-cost premium model, you should expect to **pin it manually**.

## What Question Each Pricing View Answers

| Pricing view | Unit | Best use | Source |
|---|---|---|---|
| GitHub public Copilot billing | Model multipliers and, after June 1, AI-credit usage | "What does GitHub currently expose about this model's cost inside Copilot?" | [Requests in GitHub Copilot](https://docs.github.com/en/copilot/concepts/billing/copilot-requests) |
| Repo UBB framing | AI credits and future usage-based budgets | "How should we think about spend once Business and Enterprise move onto usage-based billing on June 1, 2026?" | [Budgets for metered products](https://docs.github.com/en/billing/how-tos/budgets/setting-up-budgets-to-control-spending-on-metered-products) |
| Vendor API pricing | Input/output price per MTok | "How do raw tokens differ in value, especially input vs output?" | [Anthropic Pricing](https://platform.claude.com/docs/en/about-claude/pricing) |

## Where Input vs Output Pricing Fits

The official public GitHub Copilot docs do **not** publish a public table of Copilot input-token price vs output-token price by model. Anthropic's API pricing still gives a clear example of the asymmetry, and it remains useful for intuition. Just do not describe that as today's Copilot billing math.

| Model | Input / MTok | Output / MTok |
|---|---:|---:|
| Claude Haiku 4.5 | $1 | $5 |
| Claude Sonnet 4.6 | $3 | $15 |
| Claude Opus 4.6 | $5 | $25 |

Source: [Anthropic Pricing](https://platform.claude.com/docs/en/about-claude/pricing)

This is useful for intuition:

- output tokens are materially more expensive than input tokens
- verbose responses can dominate cost faster than people expect
- output control remains one of the highest-ROI habits in this repo

## Reasoning Effort Is a Separate Cost Lever

Model choice is not the only dial. On supported reasoning-capable models, **thinking effort** or **reasoning effort** changes how much work the model does before answering.

This is already covered in more detail in [Practical Setup](10-practical-setup.md#reasoning-effort-another-lever), but it belongs on this page too because it directly affects spend.

### What it changes

- how many tokens the model spends thinking before responding
- how much tool use and preamble it tends to generate
- latency, especially on harder tasks

### Practical guidance

| Situation | Recommended effort | Why |
|---|---|---|
| High-volume, simple chat or classification | `low` | Cheapest. Good when small quality loss is acceptable |
| Typical coding, refactors, tool-heavy work on supported reasoning models | `medium` | Best balance of cost and quality; Anthropic recommends this as the default for Sonnet 4.6 |
| Hard architecture, security review, novel decomposition | `high` or `max` | Spend more only when the task clearly justifies it |

### Important nuance

> **Use reasoning effort only on models that support it.** Non-reasoning models such as GPT-4.1 and GPT-4o do not expose this control.

So the full decision stack is:

1. choose the right model tier
2. if the model supports it, choose the lowest reasoning effort that still gets the job done

This is especially relevant when comparing a cheap reasoning-capable model at `medium` effort versus a high-cost premium model at `high` effort. In practice, effort tuning can be a cheaper substitute for jumping to a more expensive model.

## So What Should You Actually Do?

### Default stance

1. **Use Auto by default** for general day-to-day work
2. **Use included or lower-cost models** for trivial tasks when you know you do not need anything stronger
3. **Pin a premium model manually** when the task clearly justifies it
4. **Review org model policy before enablement** so premium access expands intentionally, not by drift

### Good default heuristics

| Task | Default choice | Why |
|---|---|---|
| Syntax lookup, quick explanation, tiny edit | Included model or Auto | Cheapest path, good enough quality |
| Typical implementation, bug fix, refactor | Auto or standard model | Best quality-cost tradeoff |
| Architecture, threat modeling, novel decomposition | Manually pin premium model | Auto will not automatically escalate into the premium lane |

### Anti-patterns

- Leaving an expensive premium model pinned for the whole session
- Assuming Auto will escalate to Opus when a task gets hard
- Using vendor API prices and Copilot pricing signals as if they were the same metric
- Recommending a model without checking whether the plan includes it
- Turning on every premium model for the whole org before checking who actually needs it

## Org Rollout Rule: Review Before Enablement

For teams, model choice is a governance problem as much as a prompt problem.

Use [Configuring access to AI models in Copilot](https://docs.github.com/en/copilot/using-github-copilot/ai-models/configuring-access-to-ai-models-in-copilot) to control which AI models are available. GitHub documents that organization owners and enterprise owners can enable or disable access to AI models for members.

Practical rule:

1. enable cheaper models first
2. review premium model need by workflow, team, and expected ROI
3. enable premium access narrowly
4. watch usage reports and AI-credit consumption before widening access

Use user-level AI credit budgets when you need a direct per-user cap. Remember that code completions and next edit suggestions are not billed in AI credits. More on that in [Enterprise Governance](12-enterprise-governance.md).

## Cross-References in This Repo

- [Practical Setup](10-practical-setup.md) — day-to-day setup and routing advice
- [Practical Setup § Reasoning Effort](10-practical-setup.md#reasoning-effort-another-lever) — the deeper treatment of effort levels
- [Workflow Optimization](06-workflow-optimization.md) — why Auto is still the best default
- [Enterprise Governance](12-enterprise-governance.md) — budgets, user-level caps, model policy, instruction scope
- [Home](index.md#quick-terms) — quick terms and supporting links

---

**Next:** [Enterprise Governance →](12-enterprise-governance.md)
