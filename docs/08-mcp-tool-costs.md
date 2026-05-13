# 2.7 Tool & MCP Server Costs — The Hidden Token Tax

[← Back to Guide](index.md)

---

## Before You Optimize: Measure What's Actually Loaded

Most context waste hides in things you never examine. Before tuning MCP servers or instruction files, check what's actually in your context window.

**Copilot CLI:** run `/context` mid-session to get a real breakdown:

```text
Context Usage  claude-opus-4.6 · 104k/200k tokens (52%)
System/Tools:  62.5k (31%)   ← always-loaded: MCPs + instructions + system prompt
Messages:      41.8k (21%)   ← conversation history
Free Space:    55.3k (28%)
Buffer:        40.4k (20%)
```

**VS Code Copilot:** no equivalent command, but you can estimate your `System/Tools` baseline by counting active MCP servers × tools × ~200 tokens average (see §2.7.2).

**The critical distinction — always-loaded vs. on-demand:**

| Component | Loads | In context window? |
|-----------|:-----:|:------------------:|
| MCP tool definitions | Every message | ✅ Yes |
| Agent instructions / `copilot-instructions.md` | Every message | ✅ Yes |
| System prompt | Every message | ✅ Yes (not controllable) |
| Copilot CLI skills (`.copilot/skills/`) | On request only | ❌ On disk only |
| Conversation history | Accumulates per turn | ✅ Yes |

Skills stored in `.copilot/skills/` — even hundreds of kilobytes on disk — contribute **zero** to the `System/Tools` baseline. Optimizing skills improves individual agent spawn speed, not context headroom. MCP plugins and instruction files are the levers that move the `System/Tools` number.

> Dina Berry (Microsoft/GitHub content contributor) measured a real Copilot CLI production setup and found a single Azure plugin loading ~27K tokens per message — invisible until she ran `/context`. [Full writeup →](https://dfberry.github.io/2026-05-06-tuning-up-copilot-context)

---

## 2.7.1 Every Tool Costs Tokens

When you enable an MCP server or tool in VS Code, its **entire definition** — function name, description, JSON schema for parameters — gets loaded into the agent's context. Every step. Every time.

This isn't free. Each tool definition costs approximately:

| Component | ~Tokens |
|-----------|:-------:|
| Tool name + description | 20-50 |
| Parameter schema (simple) | 30-80 |
| Parameter schema (complex) | 100-300 |
| **Total per tool** | **100-500** |

## 2.7.2 The Multiplication Problem

Here's where it gets expensive:

```text
Tools loaded = servers × tools_per_server × tokens_per_tool

Example (heavy setup):
  10 MCP servers × 5 tools each × 200 tokens avg = 10,000 tokens

Agent mode runs 5-25 steps per task.
Tool definitions reload EVERY step.

10,000 tokens × 15 steps = 150,000 tokens just for tool definitions.
```

That's 150K tokens doing nothing but telling the agent what tools exist. Before any actual work happens.

## 2.7.3 Tool Call Costs

Beyond definitions, every tool *call* costs tokens:

| Phase | Cost |
|-------|------|
| Function name + parameters (output tokens) | 20-200 per call |
| Result parsing (input tokens, next step) | 50-2,000+ per call |
| Agent reasoning about which tool to use | 50-200 per step |

A single `read_file` call might cost 50 tokens to invoke but return 2,000 tokens of file content. The agent then processes all of that on the next step.

## 2.7.4 Before and After: MCP Server Audit

**Before — "I enabled everything" (15 MCP servers):**

| Server | Tools | ~Tokens/step |
|--------|:-----:|:------------:|
| GitHub | 40 | 4,000 |
| Filesystem | 8 | 800 |
| Docker | 12 | 1,200 |
| Database (Postgres) | 10 | 1,000 |
| Database (Redis) | 8 | 800 |
| Slack | 15 | 1,500 |
| Jira | 12 | 1,200 |
| AWS | 20 | 2,000 |
| GCP | 18 | 1,800 |
| Kubernetes | 15 | 1,500 |
| Monitoring (Datadog) | 10 | 1,000 |
| Email | 8 | 800 |
| Calendar | 6 | 600 |
| Search (Brave) | 3 | 300 |
| Context7 | 2 | 200 |
| **Total** | **187** | **~17,700** |

At 15 agent steps: **265,500 tokens** just for tool schemas.

**After — "Only what I need for coding" (3 MCP servers):**

| Server | Tools | ~Tokens/step |
|--------|:-----:|:------------:|
| GitHub | 40 | 4,000 |
| Context7 | 2 | 200 |
| Filesystem | 8 | 800 |
| **Total** | **50** | **~5,000** |

At 15 agent steps: **75,000 tokens** for tool schemas.

**Savings: 190,500 tokens per agent task.** That's 72% less token overhead from tool definitions alone.

## 2.7.5 Configuring MCP Servers Per-Workspace

Don't enable every MCP server globally. Use workspace-level configuration:

**Global config** (`settings.json` User Settings) — only universally-needed servers:

```json
{
  "mcp": {
    "servers": {
      "github": {
        "command": "github-mcp-server",
        "args": ["stdio"]
      }
    }
  }
}
```

**Per-workspace config** (`.vscode/mcp.json`) — project-specific servers only:

```json
{
  "servers": {
    "postgres": {
      "command": "mcp-server-postgres",
      "args": ["postgresql://localhost/mydb"]
    }
  }
}
```

**The rule:** If you don't need it for the current task, disable it. You can always re-enable it later. Every idle MCP server costs tokens on every agent step.

## 2.7.6 Practical Guidance

1. **Audit your MCP servers** — run through your enabled servers. Do you actually use all of them? Disable the rest
2. **Task-based enabling** — working on DB migrations? Enable the Postgres MCP. Done? Disable it
3. **Prefer built-in tools** — VS Code's built-in tools (file read/write, terminal, search) are already loaded by the agent. Adding an MCP filesystem server on top is redundant
4. **Watch tool count** — if you have 100+ tools enabled, you're adding thousands of tokens per step on definitions alone
5. **Custom instructions help** — add "Minimize tool calls. Read files only when necessary." to reduce call frequency
6. **Use skills instead of MCPs for occasional capabilities** — MCP tool schemas load on every step whether used or not. Skills load only title and description upfront; the full content pulls on demand. If a capability is used in fewer than half your sessions, a skill is cheaper. See [Practical Setup §4.2](10-practical-setup.md#mcps-vs-skills-eager-vs-lazy-context-loading) for the full comparison
7. **Optional, Copilot CLI only: try CodeAct for long tool chains** — external plugin [`copilot-codeact-plugin`](https://github.com/jsturtevant/copilot-codeact-plugin) collapses many small tool hops into one sandboxed execution. That does not shrink any one server's schema, but it can reduce how often the full tool catalog gets replayed on CLI-heavy tasks
8. **Compress tool output at the source with RTK** — [RTK (Rust Token Killer)](https://github.com/rtk-ai/rtk) is a CLI proxy that filters the *results* of shell commands before they reach the agent. Confirmed to work well in VS Code Copilot (repo-by-repo setup). Reductions are real but vary by command and project output volume. See §2.7.7

## 2.7.7 Compress Tool Output at the Source: RTK

MCP schema overhead is the cost *before* any work. Separately, every shell command the agent runs produces output that becomes input tokens on the next step. A failing `cargo test` or `git diff` on a large PR can return 10,000–25,000 tokens of raw text — passing test lines, unchanged diff context, build noise — that the agent reads in full.

[**RTK (Rust Token Killer)**](https://github.com/rtk-ai/rtk) is a CLI proxy that sits between the shell and the agent. It runs the original command, captures the output, applies per-command filters (noise removal, keeping only failing tests, deduplicating log lines, grouping file listings), and returns the compressed result. The agent sees smaller output; its behavior is otherwise unchanged.

**How it works, step by step:**
1. Agent issues a Bash tool call (`git status`, `cargo test`, etc.)
2. RTK hook intercepts and rewrites to `rtk git status` / `rtk cargo test`
3. RTK runs the real command and captures full output
4. RTK applies command-specific filters
5. Agent receives filtered result — semantically equivalent, shorter

**Estimated output reductions** (RTK's own benchmarks on a medium TypeScript/Rust project — actual savings depend on your project's output volume):

| Command | Raw output | With RTK | Reduction |
|---------|:-----------:|:--------:|:---------:|
| `ls` / `tree` | ~2,000 tokens | ~400 | -80% |
| `git status` | ~3,000 tokens | ~600 | -80% |
| `git diff` | ~10,000 tokens | ~2,500 | -75% |
| `cargo test` / `npm test` | ~25,000 tokens | ~2,500 | -90% |
| `grep` / `rg` | ~16,000 tokens | ~3,200 | -80% |
| `git log -n 10` | ~2,500 tokens | ~500 | -80% |

These reductions are real in practice. Commands with verbose output (test failures, large diffs) see the biggest gains; commands with short output see smaller absolute numbers.

**Install:**

```bash
# macOS
brew install rtk

# Linux / macOS
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
```

**Setting up for VS Code Copilot — per-repo:**

For VS Code Copilot, RTK installs a PreToolUse hook scoped to the current repository. Run this once inside each repo where you want RTK active:

```bash
cd your-repo
rtk init --copilot
# Restart VS Code
```

This is a per-repo setup — there is no single global install that covers all VS Code workspaces. Once enabled in a repo, the hook is transparent: your terminal commands are unchanged; only the agent's Bash tool calls are intercepted.

**Other AI tools (global install available):**

```bash
rtk init -g                   # Claude Code (global)
rtk init -g --gemini          # Gemini CLI (global)
rtk init -g --agent cursor    # Cursor (project-level)
rtk init --agent cline        # Cline / Roo Code (project-level)
```

**Scope:** The hook intercepts **Bash tool calls** issued by the agent. VS Code Copilot's built-in tools (`Read`, `Grep`, `Glob`) do not go through Bash and are not affected. Use shell-equivalent commands (`cat`, `rg`, `find`) when you specifically want RTK filtering.

**Pairs with MCP reduction:** Schema audit (§2.7.4–2.7.6) cuts the definition cost that reloads every step. RTK cuts what each tool call *returns*. Both address different parts of the token budget and work together.

## 2.7.8 Case Study: Scoping a Large Plugin — Azure MCP

A single plugin can dominate your `System/Tools` budget. Dina Berry (Microsoft/GitHub content contributor) audited her Copilot CLI setup with `/context` and found the Azure MCP plugin loading **~27K tokens per message** by default — more than all her other MCP servers combined.

The cause: the Azure MCP Server (v3.0.0-beta.6) exposes 259 tools across 56 namespaces. In its default `namespace` mode it already groups by service, but if you're only using a few Azure services, most of those schemas are noise in every message.

**Option A — disable entirely** (if you don't need Azure in this session):

```json
// ~/.copilot/settings.json
"azure@azure-skills": false
```

Result: ~27K tokens freed from every message immediately.

**Option B — namespace scoping (recommended):**

The Azure MCP team built `--namespace` filtering for exactly this. Declare the services you actually use:

```bash
# In your MCP server config args:
--namespace appservice --namespace cosmos --namespace keyvault --namespace storage
```

This loads ~24 tools (4 namespaces) instead of all 56 namespaces. The functionality you need stays; the rest doesn't load.

**Common developer stacks:**

| Persona | Namespaces to keep |
|---------|-------------------|
| Web apps | `appservice`, `cosmos`, `keyvault`, `storage`, `functions` |
| Data/Analytics | `cosmos`, `sql`, `kusto`, `eventhubs`, `storage` |
| DevOps/Infra | `compute`, `aks`, `azureterraform`, `deploy`, `monitor` |
| AI/ML | `foundryextensions`, `search`, `speech`, `applicationinsights` |

**Azure MCP server modes** (controls how tools are exposed):

| Mode | Tools exposed | Context cost |
|------|:------------:|:------------:|
| `namespace` (default) | One tool per service namespace | Moderate |
| `consolidated` | Groups by user intent | Lower |
| `single` | One routing tool for everything | Lowest |
| `all` | Every operation as separate tool (259) | Very high |

**VS Code:** scope the Azure MCP visually — gear icon next to the chat panel → select/deselect at server, namespace, or individual tool level. No config files needed.

**Measured results** from Dina Berry's setup:

```text
Before (default config):   System/Tools 62.5k (31%) — Free Space 28%
After (Azure scoped):      System/Tools 35.2k (18%) — Free Space 45%
After (+ slim instructions): System/Tools 25.5k (13%) — Free Space 67%
```

The general lesson: when `System/Tools` is high, audit plugins before anything else. One large plugin routinely costs more than the rest of the setup combined. Full writeup: [dfberry.github.io](https://dfberry.github.io/2026-05-06-tuning-up-copilot-context).

---

**Next:** [Comparisons & Data →](09-comparisons-data.md)
