# Part 4：實際設定

[English](10-practical-setup.md) | [繁體中文（台灣）](10-practical-setup.zh-TW.md)

[← 返回指南](index.zh-TW.md)

---

## 4.1 如何把 GitHub Copilot 設定得更省 Token

### Step 1：建立 `copilot-instructions.md`

在 repo 根目錄建立 `.github/copilot-instructions.md`。這個檔案會在每次 Copilot 互動都被載入。

```bash
mkdir -p .github
touch .github/copilot-instructions.md
```

**建議起手式：**

```markdown
Terse like caveman. Technical substance exact. Only fluff die.
Drop: articles, filler (just/really/basically), pleasantries, hedging.
Fragments OK. Short synonyms. Code unchanged.
Pattern: [thing] [action] [reason]. [next step].
ACTIVE EVERY RESPONSE. No revert after many turns. No filler drift.
Code/commits/PRs: normal. Off: "stop caveman" / "normal mode".
```

這種版本大約 50 tokens，遠小於自然英文版的 120+ tokens。

### Step 2：用壓縮風格加入專案規則

```markdown
Stack: Node.js 20, TypeScript 5.4, PostgreSQL 16, Redis.
Test: Vitest. Lint: ESLint flat config.
Style: functional core, imperative shell. No classes.
Naming: camelCase vars/fns, PascalCase types, UPPER_SNAKE constants.
Errors: Result<T,E> pattern, no thrown exceptions in business logic.
```

重點是：**保留規則，不保留廢話。**

### Step 3：選擇預設模式

| 任務類型 | 建議模式 | 原因 |
|----------|----------|------|
| 快問快答 | Ask | 單次 LLM 呼叫，無工具負擔 |
| 程式說明 | Ask | 通常不需要改檔 |
| Bug 診斷 | Ask（多數） | 你可直接提供上下文 |
| 單檔修改 | Edit | 目標明確，負擔較低 |
| 多檔案重構 | Agent | 需要跨檔案讀寫 |
| 新功能實作 | Agent | 多步驟建立 |
| Issue-to-PR 自動化 | Coding Agent | 完整自主流程 |

### Step 4：有策略地選模型

模型選擇應該反映任務真正需要的**努力等級**，不是習慣性地把最強模型整天釘住。

| 模型層級 | 相對成本 | 適用情境 |
|----------|----------|----------|
| 輕量模型 | 最低 | autocomplete、語法查詢、簡單問答 |
| 標準模型 | 中等 | 大多數日常開發 |
| 高努力模型 | 最高 | 架構、深度推理、安全審查 |
| **Auto** | 預設較低 | 當作日常基準最合理 |

**預設用 Auto。**  
只有在你知道任務特別簡單，或真的需要更深推理時，再手動切模型。

### Step 5：依任務混用模型

一個有效的成本策略是：**同一個工作流程，不同子任務用不同模型。**

| 任務 | 建議模型 | 為什麼 |
|------|----------|--------|
| "What does this function do?" | 便宜／內含模型 | 只要知識擷取 |
| Quick explanations | 輕量模型 | 夠用就好 |
| 實作功能、修 bug | 標準模型 | 品質／成本比最好 |
| 架構決策、安全審查 | 高努力模型 | 真的值得多花 |

核心原則：**不要把 premium 模型拿去做便宜模型也能正確完成的工作。**

### Step 6：依實際使用模型重調 Instructions

換模型時，不要假設舊 prompt stack 還是最佳做法。  
最佳流程：

```text
把官方 guide 網址貼進 Copilot。
指定目標模型與要調整的檔案。
請它在不改變行為的前提下，降低錯誤與返工。
```

### Step 7：把治理控制放在 Prompt 外

Prompt 檔只能影響行為，真正的計費控制在別處。  
若你在做組織或企業推動，請直接看 [Enterprise Governance](12-enterprise-governance.zh-TW.md)。

### Step 8：先把非純文字輸入轉成 Markdown 再交給 AI

如果工作流一開始就會碰到 `.docx`、`.pdf`、`.pptx`、`.xlsx`、HTML 匯出、圖片、音訊、影片或 ZIP 壓縮檔，請在內容進入 Copilot 或 RAG pipeline 之前先加一道轉換步驟。富格式檔案會夾帶版面與中繼資料，增加輸入 token，卻不會提升模型理解。

[Marc Bara 的格式稅文章](https://medium.com/@marc.bara.iniesta/your-docx-is-wasting-33-of-your-ai-budget-86a3d229d042) 已把原則講得很清楚：Markdown 才是 AI 的工作格式，Word／PDF 則是人類流程需要時的交付格式。文中引用的 10 頁 PDF 範例，轉成乾淨 Markdown 後，token 量大約從 12,400 降到 8,350，資訊不變，輸入卻少了約 33%。

[Microsoft MarkItDown](https://github.com/microsoft/markitdown) 是預設最值得先試的工具。它可以把 PDF、Word、PowerPoint、Excel、圖片、音訊、HTML、CSV／JSON／XML、ZIP 內容、YouTube URL、EPUB 等轉成適合 LLM 與文字分析工作流的 Markdown。

```bash
pip install 'markitdown[all]'

markitdown report.docx -o report.md
markitdown slides.pptx -o slides.md
markitdown spreadsheet.xlsx -o spreadsheet.md
markitdown source.pdf > source.md
```

如果是正式流程，且可控格式有限，盡量只安裝需要的 extras：

```bash
pip install 'markitdown[pdf,docx,pptx,xlsx]'
```

之後把 `.md` 檔送進模型，或拿 `.md` 做 chunk／index；等到最後交付階段，再重新產出 `.docx` 或 `.pdf`。若來源不受信任，先驗證路徑與 URL；MarkItDown 會以執行程序的權限進行 I/O。

## 4.2 把可重用指引留在 Always-On Context 之外

這個 repo 不再內建可安裝 workflow packs，但原則一樣：

- PR review checklist
- release／rollback templates
- debugging playbooks
- subsystem migration notes

只要不是大多數互動都需要的內容，就不要一直放在 always-on prompt 裡。

### MCP vs Skills：Eager vs Lazy

| 機制 | 每輪載入什麼 | 完整內容何時載入 |
|------|--------------|------------------|
| MCP | 完整 tool schema | 一直都在 |
| Skill | 標題 + 描述 | 只有被使用時 |

**規則：** 常用能力用 MCP；偶爾才用的能力更適合 skill。

## 4.3 GitHub Coding Agent 的注意事項

### 4.3.1 壓縮 `copilot-instructions.md`

Agent 也會讀這個檔案；它每一步都可能再次為這些 token 付費。

### 4.3.2 使用 `copilot-setup-steps.yml`

預先把依賴安裝與建置步驟寫死，避免 agent 反覆試錯。

```yaml
steps:
  - name: Install dependencies
    run: npm ci
  - name: Build
    run: npm run build
```

### 4.3.3 Issue 描述要精準

精準 issue 能明顯減少 agent 的探索與返工。

**不好：**

```text
Fix the login bug
```

**較好：**

```text
Bug: login fails when email contains '+' character.
File: src/auth/login.ts, validateEmail() on L42.
Fix: URL-encode the email before passing to the OAuth provider.
Test: add case for "user+tag@example.com" in login.test.ts.
```

### 4.3.4 保持 PR 留言與 Commit 訊息精簡

Agent 會讀它們，把它們也當成 context。

### 4.3.5 客製化 Agent Profiles

與其一份超大總 instruction，不如按任務類型做聚焦版 profile。

### 4.3.6 用 RTK 壓縮 Shell 輸出

Coding Agent 會跑很多 shell 指令，輸出都會回灌成下一步的輸入 token。RTK 能把這些結果先壓縮再交給 agent。

## 4.4 建立習慣

### 從小做起

1. 第 1 週：加入壓縮版 `copilot-instructions.md`
2. 第 2 週：練習 caveman-lite
3. 第 3 週：升級到 caveman-full
4. 第 4 週：在 code generation 任務加上 `code only`

### 每月維護

- 檢查 `copilot-instructions.md` 是否膨脹
- 檢查其他記憶檔是否變冗長
- 關掉不必要的開啟分頁
- 檢查是否常把高成本模型釘住
- 預設模型變更時，重調 prompts

## 4.5 為效率設定 Agent Mode

### 4.5.1 Ask / Edit / Agent 的成本型態不同

| 模式 | 每次動作的 LLM 呼叫數 | 工具使用 | 最適合 |
|------|-----------------------|----------|--------|
| Ask | 1 | 無 | 問題、解釋 |
| Edit | 1-2 | 讀寫檔案 | 單檔修改 |
| Agent | 5-25 | 完整工具集 | 多步驟、多檔案任務 |

Agent Mode 常比 Ask Mode 貴上很多倍。

### 4.5.2 Agent Mode 的內部迴圈

每多一步，完整 context 都可能再重送一次，而且還會帶上前一步的結果，因此後期步驟會越來越貴。

### 4.5.3 如何減少 Agent 步數

- **Prompt 要精準，並加上 acceptance criteria**
- **複雜任務先寫 plan file**
- **確定性的操作盡量交給 shell 一次完成，不要讓 agent 一步一步探索**

### 4.5.4 VS Code 設定

```json
{
  "chat.agent.maxRequests": 10,
  "github.copilot.chat.agent.model": "auto"
}
```

### 4.5.5 給 Agent 的效率型 Instructions

```text
Minimize tool calls. Read files only when necessary.
Batch related changes. Don't read-modify-read-modify when read-modify-modify works.
Prefer grep_search over sequential read_file for discovery.
```

### 4.5.6 模式選擇框架

```text
問語法／概念／程式用途？
  → Ask

單檔修改？
  → Edit

多檔案且範圍清楚？
  → Agent + 精準 prompt

模糊的 "幫我修一下"？
  → 先用 Ask 釐清，再切 Agent
```

## 4.6 管理員層級防護欄在別處

這一頁是給實作者的。  
如果你在做組織或客戶治理，請看 [Enterprise Governance](12-enterprise-governance.zh-TW.md)。

---

**下一章：** [Enterprise Governance →](12-enterprise-governance.zh-TW.md)
