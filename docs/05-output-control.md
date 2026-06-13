# 2.4 Output Control — Tell the Model What NOT to Say

[English](05-output-control.md) | [繁體中文（台灣）](05-output-control.zh-TW.md)

[← Back to Guide](index.md)

> **Why this section matters most for cost.** Output tokens cost **5× more per token** than input tokens across all Anthropic/Copilot UBB pricing tiers. Even though responses are typically smaller in volume than total input (which includes file context, history, and tool schemas), the pricing asymmetry makes output control the highest per-token ROI action in this guide. One line in `copilot-instructions.md` — "Code only, no explanation" — cuts output cost by 40–70% on every code task, permanently.

---

## 2.4.1 Request Code-Only Responses

LLMs love to explain. A simple code generation request can return 50 lines of code wrapped in 200 tokens of explanation you didn't ask for.

**Add to your prompt or `copilot-instructions.md`:**

```text
Code only, no explanation.
```

or in your prompt:

```text
Add input validation to processOrder(). Code only.
```

**Savings: 40-70% output tokens** for code generation tasks.

**Trade-off:** If you're learning or debugging, you want the explanation. Use "code only" when you know what you're doing and just need the implementation.

## 2.4.2 Constrain Response Format

Tell the model exactly what format to use:

| Instruction | Effect | Output Savings |
|-------------|--------|----------------|
| "Answer in one sentence" | Caps verbosity | ~60-80% |
| "3 bullet points max" | Hard limit on items | ~50-70% |
| "Reply as JSON" | Structured, no prose | ~30-60% |
| "Table format" | Compact for comparisons | ~40-60% |
| "Yes or no, then one line why" | Minimal response | ~70-90% |

## 2.4.3 System-Level Terse Output

Set terse output as a project default via `copilot-instructions.md`:

```text
Be concise. No explanations unless asked.
Code only for generation tasks.
Bullets over paragraphs.
```

This applies to every interaction automatically. You don't have to remember to type "code only" each time.

**Savings: 30-60% output tokens on every interaction.**

**When to override:** When you need explanations, just ask: "Explain why this approach is better than X." The model will expand when explicitly asked, even under terse instructions.

---

**Next:** [Workflow Optimization →](06-workflow-optimization.md)
