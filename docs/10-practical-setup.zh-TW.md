```markdown
# Part 4：實際設定

[English](10-practical-setup.md) | [繁體中文（台灣）](10-practical-setup.zh-TW.md)

[← 返回指南](index.md)

---

## 4.1 如何把 GitHub Copilot 設定得更省 Token

### Step 1：建立 `copilot-instructions.md`

在 repo 根目錄建立 `.github/copilot-instructions.md`。這個檔案會在每次 Copilot 互動都被載入。

```bash
mkdir -p .github
touch .github/copilot-instructions.md
```

**建議起手式（token 最佳化）：**

```markdown
Terse like caveman. Technical substance exact. Only fluff die.
Drop: articles, filler (just/really/basically), pleasantries, hedging.
Fragments OK. Short synonyms. Code unchanged.
Pattern: [thing] [action] [reason]. [next step].
ACTIVE EVERY RESPONSE. No revert after many turns. No filler drift.
Code/commits/PRs: normal. Off: "stop caveman" / "normal mode".
```

這種版本大約 50 tokens，遠小於自然英文版的 120+ tokens。你在每次互動都能省下 70+ tokens。

### Step 2：用壓縮風格加入專案規則

用同樣壓縮的風格加入你的專案上下文：

```markdown
Stack: Node.js 20, TypeScript 5.4, PostgreSQL 16, Redis.
Test: Vitest. Lint: ESLint flat config.
Style: functional core, imperative shell. No classes.
Naming: camelCase vars/fns, PascalCase types, UPPER_SNAKE constants.
Errors: Result<T,E> pattern, no thrown exceptions in business logic.
```

對比自然英文版：

```markdown
This project uses Node.js version 20 with TypeScript 5.4. We use PostgreSQL 16
as our primary database and Redis for caching. For testing, we use Vitest, and
for linting, we use ESLint with the new flat configuration format.

We follow a functional core, imperative shell architecture. Please don't use
classes. For variable and function naming, use camelCase. Types should be in
PascalCase, and constants should be in UPPER_SNAKE_CASE.

For error handling, we use the Result<T,E> pattern. Don't throw exceptions in
business logic code.
```

兩者資訊一致，壓縮版約 40 tokens，詳細版約 110 tokens。**節省 64%，每次互動都適用。**

### Step 3：選擇預設模式

在 VS Code 中，Copilot Chat 提供模式選擇。預設策略：

| 任務類型 | 模式 | 原因 |
|----------|------|------|
| 快問快答 | Ask | 單次 LLM 呼叫，無工具負擔 |
| 程式說明 | Ask | 不需修改檔案 |
| Bug 診斷 | Ask（通常） | 你提供上下文 |
| 單檔修改 | Edit | 目標明確，負擔較低 |
| 多檔案重構 | Agent | 需跨檔案讀寫 |
| 新功能實作 | Agent | 多步驟建立 |
| Issue-to-PR 自動化 | Coding Agent | 完整自主流程 |

### Step 4：有策略地選模型

GitHub Copilot 價格依模型與計費模式而異。選擇符合任務**實際努力程度**的模型。詳細價格與計費時程見 [Model Selection & Pricing](11-models-and-pricing.md)。

| 模型層級 | 相對 Token 成本 | 適用情境 |
|----------|:---------------:|----------|
| 輕量（GPT-4.1 mini, Haiku） | 最低 | 自動完成、簡單語法、查詢式問題 |
| 標準（GPT-4.1, Sonnet） | 中等 | 大多數程式任務：實作、重構、修正 |
| 高努力（Claude Opus, o-series reasoning） | 最高 | 架構設計、深度推理、新問題拆解 |
| **Auto** | 預設較低 | 預設：Copilot 從支援的 Auto 池中選擇，付費方案符合條件時套用折扣 |

**預設用 Auto。** Auto 是最佳通用基線，減少選擇疲勞，且付費方案符合條件時套用 GitHub 折扣。視為預設路徑，不是自動升級到高努力模型。需要高努力模型時，請手動釘選。詳見 [Model Selection & Pricing](11-models-and-pricing.md)。

**切勿用高努力模型回答「X 的語法是什麼」這類問題**，因為你會為原本最便宜模型就能正確回答的答案付出更高費用。

### Step 5：依任務混用模型（模型路由）

一個有效的成本槓桿是：**同一工作流程中，不同子任務用不同模型**。詳細價格背景、歷史倍數參考、方案可用性與官方文件連結見 [Model Selection & Pricing](11-models-and-pricing.md)。此處聚焦實務路由習慣。

#### 模型混用策略

依任務認知負荷匹配模型：

| 任務類型 | 推薦模型 | 相對成本 | 原因 |
|----------|:--------:|:--------:|------|
| 「這函式做什麼？」 | GPT-4.1 / GPT-5 mini | **內含** | 知識擷取，不需推理 |
| 「X 的語法是什麼？」 | GPT-4.1 / GPT-5 mini | **內含** | 記憶知識 |
| 快速說明、摘要 | Claude Haiku 4.5 | **0.33x** | 快速、便宜、足夠好 |
| 程式碼審查、Lint 建議 | Claude Haiku 4.5 | **0.33x** | 模式匹配，不深度推理 |
| 實作功能、修 bug | Claude Sonnet 4.5 | **1x** | SWE 基準建議實務預設 |
| 多檔案重構 | Claude Sonnet 4.5 | **1x** | 真實程式任務與 Opus 相當 |
| 架構決策、系統設計 | Claude Opus 4.6 | **3x** | 深度推理值得花費 |
| 複雜多步驟規劃 | Claude Opus 4.6 | **3x** | 新穎問題拆解 |
| 安全審計、威脅建模 | Claude Opus 4.6 | **3x** | 細節與全面性重要 |

#### 實際節省範例

典型每日工作流（30 次互動），以標準層等效 token 成本表示：

| 不混用（全 Sonnet） | 混用 | 節省 |
|:-------------------:|:----:|:----:|
| 30 × 1x = **30 成本單位** | 10 × 內含 + 8 × 0.33x + 10 × 1x + 2 × 3x = **18.6 成本單位** | **38%** |

若全部用 Opus：30 × 3x = 90 成本單位。混用降至 18.6，**節省 79%**。

#### Auto 模型選擇應是預設

Copilot 的 **Auto** 模式會根據系統狀態與模型效能，從支援的 Auto 池中選擇。付費方案符合條件時，GitHub 文件記載 Copilot Chat Auto 使用享有 **10% 折扣**。視 Auto 為低摩擦預設路徑；高成本 premium 模型仍需手動釘選。

**預設用 Auto，必要時才覆寫。** 這是團隊的高槓桿預設，保持日常使用在較低成本路徑。除非你有明確理由釘選模型（例如，知道任務簡單，強制用最便宜層；或知道需要深度推理，手動釘選 premium 模型）。詳見 [Model Selection & Pricing](11-models-and-pricing.md)。

#### 反模式：所有事都用高努力模型

昂貴習慣：每次互動都用 Opus 或其他高努力模型。因為「模型越好＝結果越好」的誤解。大多數日常開發任務，額外模型成本難以合理化。

高努力模型應保留給真正擅長的任務：新穎推理、架構判斷、1-2% 品質差異值得 3-5 倍成本的任務。

#### 推理努力：另一個槓桿

除模型選擇外，推理能力模型還有第二個成本調節：**思考努力（reasoning effort）**。控制模型在回應前花多少 token 思考，影響文字、工具呼叫與延伸思考。

| 努力等級 | 行為 | Anthropic 推薦用法 |
|:--------:|------|--------------------|
| `max` | 不限 token 花費 | 最深度推理、全面分析 |
| `high`（預設） | 總是深度思考 | 複雜推理、困難程式、代理任務 |
| `medium` | 適度省 token，可能跳過思考 | **Anthropic 推薦 Sonnet 4.6 預設** — 代理程式、工具密集工作流、程式碼生成 |
| `low` | 大幅省 token，簡單任務跳過思考 | 高量、低延遲、聊天、簡單分類 |

資料來源：[Anthropic Effort 參數文件](https://platform.claude.com/docs/en/build-with-claude/effort)、[VS Code Language Models 文件](https://code.visualstudio.com/docs/copilot/concepts/language-models)、[GitHub Copilot CLI 程式化參考](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-programmatic-reference)。

重要事實：

- **努力影響所有花費，不只思考 token。** 努力越低＝回應越短、工具呼叫越少、行動前前置越少。比 `budget_tokens` 更廣泛的槓桿。
- **Anthropic 推薦 Sonnet 4.6 預設用 `medium`，非 `high`。** 文件明確說 medium 是「速度、成本與效能最佳平衡」，適合代理程式碼。
- **Copilot 多個推理模型族群支援此設定。** VS Code 中，選擇推理模型後可在子選單調整思考努力。非推理模型（如 GPT-4.1、GPT-4o）不顯示此選項。Copilot CLI 也有部分模型支援 `reasoning_effort` 設定，GitHub 文件以 `gpt-5.3-codex` 為例。Claude API 及相關工具也有此槓桿。Sonnet `medium` 努力對比 Opus `high` 努力，等效程式任務成本差異仍可達 3-5 倍以上。
- **不需開啟延伸思考模式也有效。** 不用開啟獨立思考模式，努力設定即控制總 token 花費。
- **無公開基準數據。** Anthropic 提供質性指引（上表），未公開品質與努力的具體數字。為廠商推薦，非獨立基準。

**Copilot 在多數推理模型支援此功能。** VS Code 中，選擇推理模型後開啟思考努力子選單調整。Copilot CLI 也有部分模型支援 `reasoning_effort` 設定。Claude API 及相關工具同樣提供。Sonnet `medium` 努力對比 Opus `high` 努力，等效任務成本差異可達 3-5 倍以上。

### Step 6：依實際使用模型重調 Instructions

換模型時，不要假設舊 prompt stack 仍最佳。各家供應商提示指南版本專屬，常說明行為變化：冗長度、工具積極度、結構偏好、推理努力、停止條件。

快速流程：

```text
貼官方指南網址到 Copilot。
指定目標模型與檔案。
請 Copilot 調整提示與指令，保留行為。
檢查差異，只保留減少錯誤的具體改動。
```

範例：

```text
目標模型：Claude Sonnet 4.6。
指南：https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
檔案：.github/copilot-instructions.md、.github/instructions/*.instructions.md
調整指令以適合此模型。保留 repo 行為。減少返工。保持簡潔。
```

詳見 [Workflow Optimization §2.5.5](06-workflow-optimization.md#255-retune-prompts-to-the-target-model) 供應商指南網址與 Sonnet、GPT-5.5、Gemini 範例並列。

### Step 7：把組織防護放在 Prompt 外

不要只靠 prompt 文字治理。Prompt 檔案塑造行為，計費控制在別處。

若你在推動組織或企業導入，請先看 [Enterprise Governance](12-enterprise-governance.md)。該章涵蓋管理指引：AI 點數預算、用戶限制、模型存取政策、組織指令、分組權衡。

本頁聚焦實作者設定。企業治理請參考企業章節。

### Step 8：先把非純文字輸入轉成 Markdown 再交給 AI

工作流若起點是 `.docx`、`.pdf`、`.pptx`、`.xlsx`、HTML 匯出、圖片、音訊、影片、ZIP 壓縮檔，請先轉換再送 Copilot 或 RAG pipeline。富格式檔案帶版面與中繼資料，增加輸入 token，卻不提升模型理解。

[Marc Bara 格式稅文章](https://medium.com/@marc.bara.iniesta/your-docx-is-wasting-33-of-your-ai-budget-86a3d229d042) 原則清楚：Markdown 是 AI 工作格式，Word/PDF 是人類流程交付格式。文中 10 頁 PDF 範例，轉成乾淨 Markdown 後，token 從約 12,400 降到 8,350，資訊不變，輸入少約 33%。

[Microsoft MarkItDown](https://github.com/microsoft/markitdown) 是預設推薦工具。可將 PDF、Word、PowerPoint、Excel、圖片、音訊、HTML、CSV/JSON/XML、ZIP、YouTube URL、EPUB 等轉成適合 LLM 與文字分析的 Markdown。

```bash
pip install 'markitdown[all]'

markitdown report.docx -o report.md
markitdown slides.pptx -o slides.md
markitdown spreadsheet.xlsx -o spreadsheet.md
markitdown source.pdf > source.md
```

正式流程盡量只安裝需要的 extras：

```bash
pip install 'markitdown[pdf,docx,pptx,xlsx]'
```

再將 `.md` 檔送入模型，或用 `.md` 做 chunk/index；最後交付階段再產出 `.docx` 或 `.pdf`。不受信任來源先驗證路徑與 URL；MarkItDown 以執行程序權限做 I/O。

## 4.2 把可重用指引留在 Always-On Context 之外

本 repo 不再內建可安裝 workflow packs，但原則不變：偶爾用的工作指引放在 always-on prompt 外，只有任務需要時才拉進來。

好候選：

- PR 審查清單
- 發版或回滾範本
- 除錯手冊
- 子系統遷移筆記

只要大多數互動不需要，就別一直付 token 費用。

### MCP 與 Skills：急載與懶載

| 機制 | 每輪載入內容 | 何時載入完整內容 |
|------|--------------|------------------|
| **MCP** | 完整工具結構 | 永遠載入 |
| **Skill** | 標題與描述 | 只有被使用時 |

**規則：** 常用能力用 MCP；偶爾用能力用 Skill。

## 4.3 GitHub Coding Agent 注意事項

### 4.3.1 壓縮 `copilot-instructions.md`

Agent 也會讀此檔，壓縮指令檔可在每步規劃節省 token。

### 4.3.2 使用 `copilot-setup-steps.yml`

預先寫死依賴安裝與建置，避免 agent 反覆試錯。

```yaml
# .github/copilot-setup-steps.yml
steps:
  - name: Install dependencies
    run: npm ci
  - name: Build
    run: npm run build
```

無此檔，agent 會試錯安裝依賴，增加 LLM 呼叫與 token 費用。**節省約 10-30% 總 session token。**

### 4.3.3 Issue 描述要精準

模糊 issue 會讓 agent 廣泛探索（讀多檔案＝多 token）且可能誤解需求（返工＝更多 token）。

**模糊：**

```text
Fix the login bug
```

**精準：**

```text
Bug: login fails when email contains '+' character.
File: src/auth/login.ts, validateEmail() on L42.
Fix: URL-encode the email before passing to the OAuth provider.
Test: add case for "user+tag@example.com" in login.test.ts.
```

**節省 20-50%** 總 session token，減少探索與返工。

### 4.3.4 保持 PR 留言與 Commit 訊息精簡

Agent 會讀 PR 評論與 git 歷史，冗長訊息增加 token 費用。

### 4.3.5 客製化 Agent Profiles

與其用一份龐大總指令，不如依任務類型做聚焦版指令。

### 4.3.6 用 RTK 壓縮 Shell 輸出

Coding Agent 執行許多 shell 指令，輸出會回灌成下一步輸入 token。[RTK (Rust Token Killer)](https://github.com/rtk-ai/rtk) 可先壓縮結果再交給 agent，行為不變但輸出更精簡。安裝：

```bash
brew install rtk   # 或：curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
```

設定與指令減幅詳見 [MCP & Tool Costs §2.7.7](08-mcp-tool-costs.zh-TW.md#277-rtk)。

## 4.4 建立習慣

### 從小做起

1. 第 1 週：加入壓縮版 `copilot-instructions.md`
2. 第 2 週：練習 caveman-lite，刪除贅詞，精準表達
3. 第 3 週：升級到 caveman-full，刪除冠詞，使用片語
4. 第 4 週：在程式碼生成任務加上「code only」指令，並將可重用簡潔範本放在 always-on context 外

### 每月維護

- 檢查 `copilot-instructions.md` 是否膨脹，必要時壓縮
- 檢查其他記憶檔是否冗長，必要時壓縮
- 關閉不必要的開啟分頁（開啟分頁會自動帶入 context）
- （企業用戶）檢查 repo / 組織 **內容排除** 設定，避免敏感路徑
- 檢查模型使用狀況，避免高成本模型被長期釘選
- 預設模型變更時，重新調整提示與指令
- 檢查用戶／團隊 token 使用，注意代理與高用戶是否過度消耗，詳見 [Enterprise Governance](12-enterprise-governance.zh-TW.md)

### 何時調整

| 訊號 | 措施 |
|------|------|
| 結果錯誤 | 降低壓縮等級 |
| 頻繁重複解釋 | 指令太簡短，加入一行說明 |
| 達到速率限制 | 採用更多矩陣技巧 |
| 新成員困惑 | 在程式碼中加完整英文註解，指令保持簡潔 |
| 長時間代理失敗 | 檢查 issue 描述精準度，加入 `copilot-setup-steps.yml` |

## 4.5 為效率設定 Agent Mode

### 4.5.1 Ask / Edit / Agent 的成本型態不同

| 模式 | 每次動作的 LLM 呼叫數 | 工具使用 | 最適合 |
|------|-----------------------|----------|--------|
| **Ask** | 1 | 無 | 問題、解釋 |
| **Edit** | 1-2 | 讀寫檔案 | 單檔修改 |
| **Agent** | 5-25 | 完整工具集 | 多步驟、多檔案任務 |

**成本倍數：** Agent 模式比 Ask 模式同一 prompt 貴 5-25 倍。Agent 模式的簡單問題會觸發檔案讀取、工具評估與多步推理，Ask 模式不需這些。

### 4.5.2 Agent Mode 的內部迴圈

理解迴圈有助減少步驟：

<div class="guide-visual" role="img" aria-label="Agent Mode 會在多步驟中重複重送 context 與工具結果">
  <p class="guide-visual__title">Agent Mode 迴圈</p>
  <div class="guide-visual__grid guide-visual__grid--3">
    <section class="guide-visual__card guide-visual__card--step">
      <h4><span class="guide-visual__step-label">Step 1：</span><span class="guide-visual__step-copy">載入 context</span></h4>
      <ul class="guide-visual__list">
        <li>System prompt（約 500 tokens）</li>
        <li><code>copilot-instructions.md</code>（約 50-1500 tokens）</li>
        <li>工具定義（約 2,000-20,000 tokens）</li>
        <li>對話歷史（持續增加）</li>
        <li>你的 prompt</li>
      </ul>
      <p class="guide-visual__note">送進 LLM → 取得回應</p>
    </section>
    <section class="guide-visual__card guide-visual__card--step">
      <h4><span class="guide-visual__step-label">Step 2：</span><span class="guide-visual__step-copy">呼叫工具</span></h4>
      <ul class="guide-visual__list">
        <li>工具呼叫（函式 + 參數）→ 輸出 tokens</li>
        <li>工具結果 → 下一步輸入 tokens</li>
        <li>對結果推理 → 輸出 tokens</li>
      </ul>
    </section>
    <section class="guide-visual__card guide-visual__card--step">
      <h4><span class="guide-visual__step-label">Step 3：</span><span class="guide-visual__step-copy">重複</span></h4>
      <ul class="guide-visual__list">
        <li>Step 1 的所有 context 重新載入</li>
        <li>+ 先前工具呼叫與結果</li>
        <li>+ 持續成長的對話內容</li>
      </ul>
      <p class="guide-visual__metric">重複 5-25 次</p>
    </section>
  </div>
</div>

**關鍵洞察：** 每步 context 都會成長。第 15 步會帶著第 1-14 步所有 context 加上原始 prompt，這就是長時間代理會快速變貴的原因。

### 4.5.3 如何減少 Agent 步數

每省一步，就省一次完整 context 重送。技巧：

**精準 prompt 並加接受標準：**

```text
# 不好 — agent 會探索、讀檔、猜需求
"Fix the user registration"

# 好 — agent 知道確切要做什麼
"File: src/auth/register.ts L42.
 Bug: email validation rejects valid '+' chars.
 Fix: use RFC 5322 regex.
 Test: add 'user+tag@example.com' case in register.test.ts.
 Done when: test passes, no other tests break."
```

精準版可能 3-5 步完成，模糊版可能 10-20 步探索。

**複雜任務先寫計畫檔：**

先寫計畫檔再叫 agent：

```markdown
# plan.md
1. Add `validateEmail()` to src/utils/validation.ts
2. Import and use in src/auth/register.ts L42
3. Add test cases in tests/auth/register.test.ts
4. Run `npm test` — expect all pass
```

再提示：「執行 plan.md。」agent 按計畫執行，少探索步驟＝少 token。

**確定性操作用 CLI 組合代替代理工具迴圈：**

多步瀏覽器或資料操作由 agent 觸發，每步一個 LLM 呼叫，且每步重送完整累積 context。單次產生 CLI 指令可一次 shell 執行同樣工作：

```bash
# 瀏覽器自動化 — 一次 LLM 呼叫產生，一次 shell 執行
playwright goto https://example.com && wait 1000 && click '#submit-btn' && screenshot out.png

# 串接篩選 — 不需 agent 迴圈
gh issue list --json number,title,labels | jq '.[] | select(.title | test("bug"; "i"))'

# 管線資料轉換
cat logs/app.log | grep ERROR | awk '{print $1, $5}' | sort | uniq -c | sort -rn | head -20
```

CLI 指令可組合、檢視、重跑、版本控管。改選擇器、篩選器或 URL 只需改一行文字，不用再透過 agent 多步迴圈重提問。代理工具用於真正需要動態決策的任務，確定性序列交給 shell。

### 4.5.4 VS Code 設定以節省 Token

相關設定影響 agent token 使用：

```json
{
  // 代理可呼叫工具的最大請求數（預設 25）
  "chat.agent.maxRequests": 10,

  // 使用自動模型選擇 — 簡單子任務用較便宜模型
  "github.copilot.chat.agent.model": "auto"
}
```

**`maxRequests`** 限制代理可呼叫工具的次數。數字越低＝token 越少，但複雜任務可能無法完成。建議從 10-15 起，必要時再調高。

### 4.5.5 給 Agent 的效率型指令

加入 `.github/copilot-instructions.md`：

```text
Minimize tool calls. Read files only when necessary.
Batch related changes. Don't read-modify-read-modify when read-modify-modify works.
Prefer grep_search over sequential read_file for discovery.
```

這些指令減少不必要工具呼叫。每跳過一次工具呼叫，節省 100-2,000+ tokens 的輸入輸出。

### 4.5.6 模式選擇框架

```text
問語法／概念／程式用途？
  → Ask 模式（1 次呼叫，約 500-2,000 tokens）

單檔修改？
  → Edit 模式（1-2 次呼叫，約 1,000-4,000 tokens）

多檔案且範圍清楚？
  → Agent 模式 + 精準 prompt（約 5-10 步，約 15,000-50,000 tokens）

模糊的「幫我修一下」？
  → 先用 Ask 釐清，再切 Agent
```

**昂貴的模式：** 用 Agent 模式處理模糊 prompt，讓它探索 20 步，發現誤解再重來。這會讓 token 用量翻倍，卻不見得結果更好。

## 4.6 管理員層級防護欄在別處

本頁為實作者設定。若你在做組織或企業推動，請參考 [Enterprise Governance](12-enterprise-governance.zh-TW.md)。

該章涵蓋：

- 用戶層級 AI 點數預算
- 高用量監控
- 模型存取政策
- 組織自訂指令
- 6 月 1 日切換指引

---

**下一章：** [Enterprise Governance →](12-enterprise-governance.zh-TW.md)
```
