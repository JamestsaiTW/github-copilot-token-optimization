# 2.7 工具與 MCP Server 成本：隱性的 Token 稅

[English](08-mcp-tool-costs.md) | [繁體中文（台灣）](08-mcp-tool-costs.zh-TW.md)

[← 返回指南](index.zh-TW.md)

---

## 在最佳化前，先量測真正載入了什麼

很多 context 浪費都藏在你平常不看的地方。先確認你真正的 context window 裡有什麼，再調整 MCP 或 instructions。

**Copilot CLI：** 可以在 session 中執行 `/context` 看拆解。

```text
Context Usage  claude-opus-4.6 · 104k/200k tokens (52%)
System/Tools:  62.5k (31%)
Messages:      41.8k (21%)
Free Space:    55.3k (28%)
Buffer:        40.4k (20%)
```

**關鍵差別：always-loaded vs on-demand**

| 元件 | 載入時機 | 會進 context window？ |
|------|----------|-----------------------|
| MCP tool definitions | 每則訊息 | ✅ |
| Agent instructions / `copilot-instructions.md` | 每則訊息 | ✅ |
| System prompt | 每則訊息 | ✅ |
| Copilot CLI skills | 被要求時才載入 | ❌ |
| Conversation history | 每輪累積 | ✅ |

這也是為什麼 skills 放很多內容在磁碟上，不代表會增加 `System/Tools` 基線；真正推高基線的是 MCP schema 與 always-on instructions。

## 2.7.1 每個 Tool 都要 Token

啟用 MCP server 或 tool 後，其**完整定義**都會被載入 agent 的 context：名稱、描述、參數 JSON schema，全都算。

| 元件 | 約略 Tokens |
|------|-------------|
| Tool 名稱 + 描述 | 20-50 |
| 簡單參數 schema | 30-80 |
| 複雜參數 schema | 100-300 |
| **每個 Tool 合計** | **100-500** |

## 2.7.2 乘法問題

真正貴的是它會被重複載入：

```text
Tools loaded = servers × tools_per_server × tokens_per_tool

Example:
10 MCP servers × 5 tools × 200 tokens = 10,000 tokens

Agent mode 走 15 steps：
10,000 × 15 = 150,000 tokens
```

也就是說，還沒做任何真正工作，就先花了 15 萬個 token 讓 agent 知道有哪些工具可用。

## 2.7.3 Tool Call 本身也有成本

除了 schema，工具呼叫本身也會產生成本：

| 階段 | 成本 |
|------|------|
| Function name + params | 每次 20-200 output tokens |
| Result parsing | 每次 50-2,000+ input tokens |
| Agent 判斷要用哪個工具 | 每步 50-200 tokens |

## 2.7.4 MCP Server 稽核的前後差異

**啟用一切的重度設定** 與 **只保留必要工具的設定**，差異可能是每次 agent 任務數十萬 token。

核心結論：

- 不用的 MCP server 真的要關
- schema 成本是每步都重付，不是只付一次

## 2.7.5 每個 Workspace 各自配置 MCP

不要把所有 MCP server 都全域開著。  
做法是：

- **全域設定** 只放真正到處都要用的
- **workspace 設定** 才放專案特定的

規則很簡單：**這次任務用不到，就先關掉。**

## 2.7.6 實用建議

1. **稽核你的 MCP servers**，停掉不用的
2. **依任務啟用**，例如做 DB migration 才打開 Postgres MCP
3. **優先用內建工具**，避免和外掛 MCP 重複
4. **注意總 tool 數量**
5. **在 custom instructions 補一句**，例如：`Minimize tool calls. Read files only when necessary.`
6. **偶爾才用的能力，優先做成 skill，不是 MCP**
7. **Copilot CLI 長工具鏈可考慮 CodeAct**
8. **用 RTK 壓縮工具輸出**

## 2.7.7 從源頭壓縮工具輸出：RTK

MCP schema 是「工作開始前」的成本。另一個大頭是 shell 命令的輸出：它們會在下一步原封不動回灌成 agent 的輸入 token。

[RTK (Rust Token Killer)](https://github.com/rtk-ai/rtk) 是 CLI proxy，會攔截指令、過濾噪音，再把壓縮後的結果傳回 agent。

**它做了什麼：**

1. Agent 發出 Bash tool call
2. RTK 攔截並改寫為 `rtk <command>`
3. RTK 執行真正命令
4. 依命令類型過濾雜訊
5. Agent 拿到語意相同但更短的結果

**常見減幅：**

| 指令 | 原始輸出 | RTK 後 | 減幅 |
|------|----------|--------|------|
| `ls` / `tree` | 約 2,000 | 約 400 | -80% |
| `git status` | 約 3,000 | 約 600 | -80% |
| `git diff` | 約 10,000 | 約 2,500 | -75% |
| `cargo test` / `npm test` | 約 25,000 | 約 2,500 | -90% |
| `grep` / `rg` | 約 16,000 | 約 3,200 | -80% |

**對 VS Code Copilot 的重點：**

- 需以 repo 為單位啟用：`rtk init --copilot`
- 這不是全域一次裝好就全部生效
- 只影響 agent 的 Bash tool calls，不影響內建 `Read`、`Grep`、`Glob`

## 2.7.8 案例：把大型 Plugin 範圍化

大型 plugin 常常是一整個 `System/Tools` 成本大戶。  
以 Azure MCP 為例，若預設載入 200+ tools，單一 plugin 就可能吃掉數萬 tokens。

做法通常有兩種：

- **完全停用**：這個 session 根本不用 Azure
- **namespace 範圍化**：只保留真的有在用的 Azure services

一般原則很清楚：

- 當 `System/Tools` 偏高時，先檢查大型 plugins
- 一個大 plugin 的成本，常常比其他所有工具加總還高

---

**下一章：** [Comparisons & Data →](09-comparisons-data.zh-TW.md)
