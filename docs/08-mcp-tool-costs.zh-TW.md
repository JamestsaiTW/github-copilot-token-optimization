```markdown
# 2.7 工具與 MCP Server 成本：隱性的 Token 稅

[English](08-mcp-tool-costs.md) | [繁體中文（台灣）](08-mcp-tool-costs.zh-TW.md)

[← 返回指南](index.md)

---

## 在最佳化前，先量測真正載入了什麼

很多 context 浪費都藏在你平常不看的地方。先確認你真正的 context window 裡有什麼，再調整 MCP 或 instructions。

**Copilot CLI：** 可以在 session 中執行 `/context` 看拆解。

```text
Context Usage  claude-opus-4.6 · 104k/200k tokens (52%)
System/Tools:  62.5k (31%)   ← always-loaded: MCPs + instructions + system prompt
Messages:      41.8k (21%)   ← conversation history
Free Space:    55.3k (28%)
Buffer:        40.4k (20%)
```

**VS Code Copilot：** 沒有對應指令，但你可以估算 `System/Tools` 基線，方法是計算啟用的 MCP server 數 × 工具數 × 約 200 tokens 平均（見 §2.7.2）。

**關鍵差別 — always-loaded 與 on-demand：**

| 元件 | 載入時機 | 會進 context window？ |
|------|:--------:|:---------------------:|
| MCP tool definitions | 每則訊息 | ✅ 是 |
| Agent instructions / `copilot-instructions.md` | 每則訊息 | ✅ 是 |
| System prompt | 每則訊息 | ✅ 是（無法控制） |
| Copilot CLI skills (`.copilot/skills/`) | 只有請求時 | ❌ 只在磁碟上 |
| Conversation history | 每輪累積 | ✅ 是 |

即使 `.copilot/skills/` 裡有數百 KB 的內容，也不會增加 `System/Tools` 基線。優化 skills 只會加快個別 agent 啟動速度，不會增加 context 容量。真正影響 `System/Tools` 數字的是 MCP 外掛與指令檔。

> Microsoft/GitHub 內容貢獻者 Dina Berry 實測一套 Copilot CLI 生產環境，發現單一 Azure 外掛每則訊息載入約 27K tokens — 只有執行 `/context` 才看得出來。[完整報告 →](https://dfberry.github.io/2026-05-06-tuning-up-copilot-context)

---

## 2.7.1 每個 Tool 都要 Token

當你在 VS Code 啟用 MCP server 或工具時，其**完整定義**（函式名稱、描述、參數 JSON schema）會被載入 agent 的 context。每一步都會載入。

這不是免費的。每個工具定義大約需要：

| 元件 | 約略 Tokens |
|------|:-----------:|
| 工具名稱 + 描述 | 20-50 |
| 參數 schema（簡單） | 30-80 |
| 參數 schema（複雜） | 100-300 |
| **每個工具合計** | **100-500** |

## 2.7.2 乘法問題

真正貴的是它會被重複載入：

<div class="guide-visual" role="img" aria-label="工具定義成本會隨 server、tool 與 agent 步數相乘">
  <p class="guide-visual__title">工具成本會一直重載</p>
  <div class="guide-visual__grid guide-visual__grid--2">
    <section class="guide-visual__card">
      <h4>公式</h4>
      <p class="guide-visual__math">Tools loaded = servers x tools_per_server x tokens_per_tool</p>
      <p class="guide-visual__note">整包工具定義會在每個 agent step 再載一次。</p>
    </section>
    <section class="guide-visual__card">
      <h4>重度設定範例</h4>
      <p class="guide-visual__math">10 MCP servers x 5 tools x 200 tokens = 10,000 tokens</p>
      <div class="guide-visual__flow">
        <p class="guide-visual__math">10,000 tokens x 15 steps</p>
      </div>
      <p class="guide-visual__metric">150,000 tokens</p>
    </section>
  </div>
</div>

也就是說，還沒做任何真正工作，就先花了 15 萬個 token 讓 agent 知道有哪些工具可用。

## 2.7.3 Tool Call 本身也有成本

除了定義，工具呼叫本身也會產生成本：

| 階段 | 成本 |
|------|------|
| 函式名稱 + 參數（輸出 tokens） | 每次 20-200 |
| 結果解析（輸入 tokens，下一步） | 每次 50-2,000+ |
| Agent 判斷要用哪個工具 | 每步 50-200 |

單次 `read_file` 呼叫可能花 50 tokens 呼叫，但回傳 2,000 tokens 的檔案內容，agent 接著在下一步處理這些內容。

## 2.7.4 MCP Server 稽核的前後差異

**啟用一切的重度設定（15 MCP servers）：**

| Server | 工具數 | 約 Tokens/步 |
|--------|:------:|:------------:|
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
| **總計** | **187** | **約 17,700** |

15 步 agent：**265,500 tokens** 只用在工具定義。

**只保留必要工具的設定（3 MCP servers）：**

| Server | 工具數 | 約 Tokens/步 |
|--------|:------:|:------------:|
| GitHub | 40 | 4,000 |
| Context7 | 2 | 200 |
| Filesystem | 8 | 800 |
| **總計** | **50** | **約 5,000** |

15 步 agent：**75,000 tokens** 用於工具定義。

**節省：每個 agent 任務省下 190,500 tokens。** 工具定義成本降低 72%。

## 2.7.5 每個 Workspace 各自設定 MCP

不要把所有 MCP server 都全域開著。  
做法是：

- **全域設定**（`settings.json` 使用者設定）只放真正到處都要用的

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

- **workspace 設定**（`.vscode/mcp.json`）只放專案特定的

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

**規則很簡單：** 這次任務用不到，就先關掉。你隨時可以再啟用。每個閒置的 MCP server 都會在每個 agent 步驟消耗 tokens。

## 2.7.6 實用建議

1. **稽核你的 MCP servers** — 檢查啟用的伺服器，停掉不用的
2. **依任務啟用** — 例如做資料庫遷移時啟用 Postgres MCP，完成後停用
3. **優先用內建工具** — VS Code 內建工具（檔案讀寫、終端機、搜尋）已被 agent 載入，額外加 MCP 檔案系統伺服器是重複的
4. **注意工具數量** — 啟用超過 100 個工具，單是定義就會增加數千 tokens
5. **自訂指令檔幫助** — 在 custom instructions 補一句：「Minimize tool calls. Read files only when necessary.」以降低呼叫頻率
6. **偶爾才用的功能，優先做成 skill，不是 MCP** — MCP 工具定義每步都載入，skill 只載入標題與描述，完整內容按需載入。若功能使用頻率低於一半，skill 更省 tokens。詳見 [實用設定 §4.2](10-practical-setup.md#mcps-vs-skills-eager-vs-lazy-context-loading)
7. **Copilot CLI 長工具鏈可考慮 CodeAct** — 外部外掛 [`copilot-codeact-plugin`](https://github.com/jsturtevant/copilot-codeact-plugin) 可將多個小工具跳轉合併成一次沙箱執行。雖不會縮小單一伺服器的 schema，但可減少 CLI 密集任務中工具目錄重播頻率
8. **用 RTK 壓縮工具輸出**

## 2.7.7 從源頭壓縮工具輸出：RTK

MCP schema 是「工作開始前」的成本。另一個大頭是 shell 命令的輸出：它們會在下一步原封不動回灌成 agent 的輸入 token。

[RTK (Rust Token Killer)](https://github.com/rtk-ai/rtk) 是 CLI proxy，會攔截指令、過濾噪音，再把壓縮後的結果傳回 agent。

**它做了什麼：**

1. Agent 發出 Bash 工具呼叫（如 `git status`、`cargo test`）
2. RTK 攔截並改寫為 `rtk git status` / `rtk cargo test`
3. RTK 執行真正命令並擷取完整輸出
4. 依命令類型過濾雜訊（移除噪音、只保留失敗測試、去重複日誌、整理檔案列表）
5. Agent 拿到語意相同但更短的結果

**估計減幅**（RTK 自身在中型 TypeScript/Rust 專案的基準測試，實際節省視專案輸出量而異）：

| 指令 | 原始輸出 | RTK 後 | 減幅 |
|------|:--------:|:------:|:----:|
| `ls` / `tree` | 約 2,000 tokens | 約 400 tokens | -80% |
| `git status` | 約 3,000 tokens | 約 600 tokens | -80% |
| `git diff` | 約 10,000 tokens | 約 2,500 tokens | -75% |
| `cargo test` / `npm test` | 約 25,000 tokens | 約 2,500 tokens | -90% |
| `grep` / `rg` | 約 16,000 tokens | 約 3,200 tokens | -80% |
| `git log -n 10` | 約 2,500 tokens | 約 500 tokens | -80% |

這些減幅在實務中確實有效。輸出量大的指令（失敗測試、大型 diff）節省最多；輸出量小的指令節省較少。

**安裝：**

```bash
# macOS
brew install rtk

# Linux / macOS
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
```

**VS Code Copilot 的 per-repo 設定：**

RTK 為 VS Code Copilot 安裝一個 PreToolUse hook，範圍限定在當前 repo。請在每個要啟用 RTK 的 repo 執行一次：

```bash
cd your-repo
rtk init --copilot
# 重新啟動 VS Code
```

這是 per-repo 設定，沒有單一全域安裝可涵蓋所有 VS Code 工作區。啟用後，hook 透明運作：終端機指令不變，只有 agent 的 Bash 工具呼叫被攔截。

**其他 AI 工具（可全域安裝）：**

```bash
rtk init -g                   # Claude Code (全域)
rtk init -g --gemini          # Gemini CLI (全域)
rtk init -g --agent cursor    # Cursor (專案層級)
rtk init --agent cline        # Cline / Roo Code (專案層級)
```

**範圍：** hook 攔截 agent 發出的 **Bash 工具呼叫**。VS Code Copilot 內建工具（`Read`、`Grep`、`Glob`）不經由 Bash，不受影響。若要使用 RTK 過濾，請改用 shell 等效指令（`cat`、`rg`、`find`）。

**搭配 MCP 減量：** schema 稽核（§2.7.4–2.7.6）降低每步重載成本，RTK 則壓縮每次工具呼叫的回傳結果。兩者針對不同 token 預算，效果互補。

## 2.7.8 案例：把大型 Plugin 範圍化 — Azure MCP

單一大型 plugin 可能主導你的 `System/Tools` 預算。Microsoft/GitHub 內容貢獻者 Dina Berry 實測 Copilot CLI，發現 Azure MCP plugin 預設每則訊息載入約 27K tokens，超過其他所有 MCP server 總和。

原因：Azure MCP Server (v3.0.0-beta.6) 暴露 259 個工具，分布在 56 個命名空間。預設 `namespace` 模式會依服務分組，但若你只用幾個 Azure 服務，大部分 schema 是每則訊息的噪音。

**方案 A — 完全停用**（若本次 session 不用 Azure）：

```json
// ~/.copilot/settings.json
"azure@azure-skills": false
```

效果：立刻釋放約 27K tokens。

**方案 B — 命名空間範圍化（推薦）：**

Azure MCP 團隊提供 `--namespace` 過濾參數。只保留你實際使用的服務：

```bash
# MCP server 設定參數中：
--namespace appservice --namespace cosmos --namespace keyvault --namespace storage
```

這樣只載入約 24 個工具（4 個命名空間），而非全部 56 個。你需要的功能保留，其他不載入。

**常見開發者堆疊：**

| 角色 | 保留命名空間 |
|------|--------------|
| Web 應用 | `appservice`、`cosmos`、`keyvault`、`storage`、`functions` |
| 資料/分析 | `cosmos`、`sql`、`kusto`、`eventhubs`、`storage` |
| DevOps/基礎建設 | `compute`、`aks`、`azureterraform`、`deploy`、`monitor` |
| AI/機器學習 | `foundryextensions`、`search`、`speech`、`applicationinsights` |

**Azure MCP server 模式**（控制工具如何暴露）：

| 模式 | 暴露工具數 | Context 成本 |
|------|:----------:|:------------:|
| `namespace`（預設） | 每個服務命名空間一個工具 | 中等 |
| `consolidated` | 依使用者意圖分組 | 較低 |
| `single` | 一個路由工具涵蓋全部 | 最低 |
| `all` | 每個操作獨立工具（259 個） | 非常高 |

**VS Code：** 可視化範圍化 Azure MCP — 聊天面板旁齒輪圖示 → 在伺服器、命名空間或單一工具層級選擇啟用/停用，無需編輯設定檔。

**Dina Berry 實測結果：**

```text
啟用前（預設設定）：System/Tools 62.5k (31%) — Free Space 28%
範圍化後（Azure scoped）：System/Tools 35.2k (18%) — Free Space 45%
再加上精簡指令檔：System/Tools 25.5k (13%) — Free Space 67%
```

總結：當 `System/Tools` 偏高時，優先稽核大型外掛。單一大型外掛的成本，常超過其他所有工具加總。完整報告：[dfberry.github.io](https://dfberry.github.io/2026-05-06-tuning-up-copilot-context)。

---

**下一章：** [Comparisons & Data →](09-comparisons-data.zh-TW.md)
```
