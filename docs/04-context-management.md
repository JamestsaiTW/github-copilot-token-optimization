# 2.3 Context Management — Control What Gets Sent

[← Back to Guide](index.md)

---

## 2.3.1 System Instruction Compression

Your `.github/copilot-instructions.md` file is injected into **every single Copilot interaction**. Every word in it costs tokens on every prompt.

> **Note — related but distinct conventions.** `.github/copilot-instructions.md` is GitHub Copilot's native repo-level instruction file. `AGENTS.md` is a broader cross-tool convention that Copilot also reads. They are **not the same file**, and they can legitimately coexist (e.g. `AGENTS.md` shared across multiple AI tools, `copilot-instructions.md` for Copilot-specific rules). What they have in common is that both function as **always-on context** — every token in either file is paid on every interaction. The compression and pruning techniques in this section apply equally to both. If your repo carries duplicated content across the two, that duplication *is* paid twice; deduplicate ruthlessly. See [Part 2.6](07-agents-md-problem.md) for the research on *what* to keep.

This makes it the highest-leverage file to optimize. A 500-word instruction file at ~700 tokens means 700 tokens burned on every interaction — before you even type your question.

**Before — natural English (~30 tokens):**

```text
You should write terse responses like a caveman. Make sure all technical substance
remains exact. Only remove unnecessary filler words. Drop articles and hedging.
Use fragments when appropriate. Keep code unchanged. Use short synonyms where possible.
```

**After — compressed (~12 tokens):**

```text
Terse like caveman. Technical substance exact. Only fluff die.
Drop: articles, filler (just/really/basically), pleasantries, hedging.
Fragments OK. Short synonyms. Code unchanged.
```

**Savings: 60%.** Multiply by every interaction in a session. Over 50 interactions, that's 900 tokens saved from this one file alone.

**Real-world example:** This repo's own `.github/copilot-instructions.md` is already compressed:

```text
Terse like caveman. Technical substance exact. Only fluff die.
Drop: articles, filler (just/really/basically), pleasantries, hedging.
Fragments OK. Short synonyms. Code unchanged.
Pattern: [thing] [action] [reason]. [next step].
ACTIVE EVERY RESPONSE. No revert after many turns. No filler drift.
Code/commits/PRs: normal. Off: "stop caveman" / "normal mode".
```

~50 tokens. Loaded on every interaction. That's what an optimized instruction file looks like.

## 2.3.2 Memory File Compression

Beyond `copilot-instructions.md` / `AGENTS.md` (which are the same file under two names, see note above), many projects accumulate other memory files that become context: `CLAUDE.md`, project notes, coding guidelines, `.cursorrules`. These are all loaded as context, and all burn tokens on every call. Consolidate duplicates before you start compressing.

**Before (~40 tokens):**

```text
You should always make sure to run the test suite before pushing any changes
to the main branch. This is important because it helps catch bugs early and
prevents broken builds from being deployed to production.
```

**After (~15 tokens):**

```text
Run tests before push to main. Catch bugs early, prevent broken prod deploys.
```

**Savings: 62%.** The technical meaning is identical.

**Compression rules:**

- Remove articles, filler, hedging, pleasantries
- Use short synonyms and fragments
- **Preserve ALL:** code blocks, inline code, URLs, file paths, technical terms
- Keep markdown structure (headings, lists, tables)

This repo no longer ships installable workflow packs. Compress memory files manually when they become always-on context, or keep occasional compression checklists outside the prompt and invoke them only when needed.

## 2.3.3 Strategic File Organization

Copilot automatically includes context from your workspace — open files, imported modules, nearby files. You can control what gets included.

**The official exclusion mechanism is Content Exclusion**, configured by repository / organization / enterprise admins via GitHub settings or the REST API. It's only available on **Copilot Business and Enterprise**, and it does **not** apply to Copilot CLI, the Copilot cloud agent, or Agent Mode in Copilot Chat in IDEs. Treat it as a privacy / policy control ("don't read this file"), not a per-developer token-saving knob. See [GitHub Docs — Excluding content from GitHub Copilot](https://docs.github.com/en/copilot/how-tos/configure-content-exclusion/exclude-content-from-copilot).

What actually reduces auto-included context (per-developer levers that work everywhere):

- **Close files you're not working on.** Open editor tabs are the #1 source of auto-included context. Closing a 1,000-line file you're not touching is the single fastest token win available in IDE Copilot.
- **Keep files focused and small.** If a 1,000-line file is open, Copilot may send large chunks of it as context. Break large files into focused modules.
- **Use `.gitignore` for build output, vendor dirs, and generated files.** Anything Git ignores is generally not pulled in as auto-context, and it keeps your repo clean as a side effect.
- **Use `applyTo:` scoped instruction files** (see § 2.3.4 below) so per-domain context only loads when relevant files are open — the most reliable way to shrink per-interaction context.
- **For Business/Enterprise customers:** ask your repo / org admin to configure **Content Exclusion** for genuinely sensitive paths (secrets, generated bundles, large data files). Primary purpose is policy, but it also keeps that content out of Chat / completions.

**Watch out for** — anything in this list, if open or referenced, will burn tokens:

- Large README files
- Generated files (build output, bundled CSS, minified JS)
- Vendor directories
- Data files (CSVs, JSON fixtures)
- Archived documentation
- Rich document formats (`.docx`, `.pdf`, `.pptx`, `.xlsx`, HTML exports, scanned images, audio/video transcripts)

Every file that enters context costs tokens. Be intentional about what's open and what's referenced with `#file`.

### Normalize non-text inputs to Markdown first

When the source is a Word file, PDF, PowerPoint, spreadsheet, image, audio file, or exported HTML, do not paste the rich format directly into an AI workflow if you can avoid it. Convert it to clean Markdown first, then send the Markdown.

Marc Bara calls this the **format tax** in [Your .docx Is Wasting 33% of Your AI Budget](https://medium.com/@marc.bara.iniesta/your-docx-is-wasting-33-of-your-ai-budget-86a3d229d042): Word, PDF, and HTML carry font data, XML, page-positioning metadata, layout artifacts, embedded objects, and tag soup that models must process but rarely need. The article cites a concrete example where a 10-page report extracted from PDF used roughly 12,400 tokens, while the same content as clean Markdown used about 8,350 tokens — a 33% reduction with the same information. HTML exports can be even worse because semantic content gets wrapped in long tags, classes, IDs, and layout scaffolding.

The rule: use Markdown as the **working format** for AI interaction, and treat Word/PDF/PowerPoint as delivery formats. Draft, review, summarize, chunk, and retrieve from Markdown. Generate `.docx` or `.pdf` at the end only when a client, regulator, or internal process needs that artifact.

[Microsoft MarkItDown](https://github.com/microsoft/markitdown) is the practical bridge. It is a Python tool for converting files and office documents to Markdown for LLM and text-analysis pipelines. It preserves useful structure such as headings, lists, tables, links, and extracted metadata, while avoiding high-fidelity visual layout noise. Current converters include PDF, Word, PowerPoint, Excel, images with EXIF/OCR support, audio with transcription support, HTML, CSV/JSON/XML, ZIP contents, YouTube URLs, EPUBs, and more.

Fast path:

```bash
pip install 'markitdown[all]'
markitdown report.docx -o report.md
markitdown deck.pptx -o deck.md
markitdown source.pdf > source.md
```

Use narrower extras when you control the workflow and want fewer dependencies:

```bash
pip install 'markitdown[pdf,docx,pptx,xlsx]'
```

Security note: MarkItDown reads files, streams, and URLs with the privileges of the current process. For untrusted inputs, validate paths and URLs first, and prefer the narrowest conversion API that fits the workflow.

## 2.3.4 Scope Context Intentionally — Conditional Over Always-On

Most context files are loaded on **every** interaction. That's a tax you pay even when the file isn't relevant — your React component questions don't need your database migration guidelines.

The fix: prefer **conditional context** over always-on context.

### Use `applyTo:` paths in custom instructions

Custom instruction files in `.github/instructions/*.instructions.md` accept an `applyTo` frontmatter field that scopes the file to matching paths. Copilot only loads it when the conversation involves files matching the glob.

```markdown
---
applyTo: "src/api/**/*.ts"
---
API conventions:
- Routes in src/api/routes/. Handlers thin, logic in services/.
- Validate with zod. Errors via Result<T,E>, never throw.
- All endpoints return { data, error } envelope.
```

Without `applyTo`, that's ~30 tokens loaded on every Copilot call across the whole repo. With it, the cost is paid only when you're actually editing API code.

**Pattern:** Split one big `copilot-instructions.md` into a small always-on core plus several scoped instruction files (`api.instructions.md`, `ui.instructions.md`, `tests.instructions.md`, `migrations.instructions.md`). Each carries its own `applyTo` glob. The total context surface stays large, but the per-interaction cost is small because only the relevant slice loads.

### Leverage on-demand guidance and MCP tool discovery

Workflow-specific guidance should follow the same rule as MCP tools: keep it off the always-on prompt and bring it in only when the task needs it. A PR-review checklist, release template, or debugging playbook does not belong in `copilot-instructions.md` if you only use it occasionally.

Treat small prompt files, slash-command snippets, or saved checklists as the home for *workflow-specific* guidance. They stay out of every-day context until you invoke them.

### The rule

- **Always-on:** the few rules that genuinely apply to every interaction (style, naming, "code only").
- **Conditional (`applyTo`):** anything path-specific (per-language, per-module, per-layer).
- **On-demand note / MCP:** anything workflow-specific that's invoked occasionally.

Most teams have it inverted — everything in always-on. Flipping the ratio cuts per-interaction context by 50-80% with zero loss of fidelity.

> **Large files on disk ≠ context cost.** A common mistake: spending time compressing files that never actually enter the context window. In Copilot CLI, skills stored in `.copilot/skills/` are on-demand — they load only when an agent explicitly requests one, and never touch the `System/Tools` baseline. Optimizing them improves per-spawn speed, not context headroom. The levers that move your context baseline are MCP tool definitions and always-on instruction files. See [MCP & Tool Costs §2.7](08-mcp-tool-costs.md) for how to measure what's actually loaded.

## 2.3.5 Caching — Store and Reuse Context Within Prompts

The cheapest token is the one the platform doesn't have to re-process. Modern Copilot interactions cache stable portions of context (system prompt, instruction files, recently-loaded files) so they don't pay the full input-token cost on every turn.

In long sessions, this is often the biggest single cost lever. When most of your input is cache-hit input, effective input cost can drop dramatically (commonly cited as up to ~90% discount on cached input, depending on provider/model/surface billing rules).

You can lean into this. Two practical patterns:

**1. Stable instructions at the top, volatile work at the bottom.** Cached context only works if the prefix of your conversation is stable. Don't reshuffle your `copilot-instructions.md` or rotate which files are open between every prompt — keep the stable layer stable, and let only the most recent message change.

**2. Reuse named context via slash commands and saved snippets.** When you frequently ask about the same domain, define it once and reference it. For example: keep a short customers-schema note or slash-command snippet, load it once for the session, then keep follow-up prompts anchored to that shared summary instead of re-pasting the schema every time.

Caching gains are real and dual-purpose: **it's faster** (cached prefixes skip re-encoding) **and cheaper** (most platforms bill cached input tokens at a fraction of the standard rate). Designing your context layout for cache stability is one of the lowest-effort wins available.

### Protect the cache: avoid cache-busting changes mid-thread

In expensive long-running chats, treat cache stability as a hard constraint. The most common cache-busters are:

- **Switching models mid-thread** (for example, moving from one Claude/GPT tier to another)
- **Enabling or disabling MCP servers mid-thread** (tool definitions sit near the top of context; changing them invalidates large prefixes)
- **Switching agent/profile mode mid-thread** (default agent ↔ custom agent, or one custom agent ↔ another)

Practical rule: keep this tuple fixed for the whole long thread:

```text
{ model, active MCP set, active agent/profile }
```

If you need to change any item in that tuple, start a fresh conversation with a compact handoff summary instead of changing it in place.

### Safe handoff pattern when a switch is required

1. Summarize current thread in 5-10 bullets (decisions, constraints, open tasks).
2. Start a new chat with the new model/agent/MCP setup.
3. Paste only the summary + required files, not the entire old transcript.

This preserves cache efficiency in the original thread and prevents dragging stale context into a new cost lane.

## 2.3.6 Start Fresh Conversations

Conversation history accumulates. After 20+ messages, you might have 50K+ tokens of history sent with every new message.

**When to start fresh:**

- Topic change — new question, new file, new concern
- After getting the answer you needed
- When responses start getting slow (context window filling up)
- When you notice quality dropping (model confused by old context)

**How to preserve continuity:** Summarize key decisions in your new prompt. "Continuing from auth refactor — we chose JWT over sessions. Now implement refresh tokens."

---

**Next:** [Output Control →](05-output-control.md)
