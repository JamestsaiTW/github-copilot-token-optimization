# GitHub Copilot 的 Token 最佳化指南

[English](README.md) | [繁體中文（台灣）](README.zh-TW.md)

> [!IMPORTANT]
> **這不是 GitHub 或 Microsoft 的官方指引。** 這份指南是來自實務現場經驗的社群資源，整理了導入 AI 進行開發時，從實際觀察到的模式、驗證過的方法，以及第一線累積的教訓。它代表的是產業現場自下而上的實務知識，而不是自上而下的產品文件。你可以用它來思考最佳化策略，並依照客戶的情境調整適用做法。官方指引請見 [docs.github.com/copilot](https://docs.github.com/copilot)。

> 這是一份以資料為基礎、重視實務的指南，協助你在維持程式碼品質的同時降低 token 消耗。
> 涵蓋 Chat、Inline 與 Coding Agent 工作流程。

---

## 快速開始：現在就該做的 12 件事

> **2026 年 6 月 1 日，按使用量計費（UBB）已正式上線。** GitHub Copilot 現在不再以請求次數計費，而是改為針對實際 token 用量（input + output + cached）計費，並從共用的 AI 點數池中扣抵（Business 每席次 30 美元、Enterprise 每席次 70 美元）。本指南中的每一項技巧，都可以直接轉換成點數節省，而且在新的計費模式下，對快取友善的使用習慣會比以前更重要。客戶治理與限制建議請參考 [Enterprise Governance](docs/12-enterprise-governance.zh-TW.md)，模型成本建議請參考 [Model Selection & Pricing](docs/11-models-and-pricing.zh-TW.md)。

> **輸出 token 的成本遠高於輸入 token。** 這是本指南最重要的定價事實。Anthropic 公開的定價可以很清楚地說明這種不對稱性（每百萬 token 的輸入／輸出價格分別為：Haiku 1 美元／5 美元、Sonnet 3 美元／15 美元、Opus 5 美元／25 美元）。Copilot 目前尚未公開各模型的 UBB 精確定價表，但在 UBB 模式下，冗長輸出仍然會顯得特別昂貴。大多數輸入 token 其實來自檔案內容、歷史對話與工具 schema，而不是你手動輸入的提示詞。你打的 prompt 只占整體輸入的一小部分。先從控制輸出開始，再處理結構性的輸入最佳化。

如果你沒時間讀完整份指南，今天先做這些事，就能開始降低 token 用量：

| # | 行動 | 主要效果 | 設定時間 |
|---|------|----------|----------|
| 1 | **要求只輸出程式碼**：在 `copilot-instructions.md` 加上 `Code only, no explanation.`。這是每個 token 最值得投資的做法：輸出成本是輸入的 5 倍，這一條能在所有程式任務中永久減少 40-70% 的輸出 | 縮短回應長度 | 0 分鐘 |
| 2 | **預設限制輸出格式**：在 `copilot-instructions.md` 加上 `Bullets over paragraphs. No explanations unless asked.` | 讓回答保持精簡 | 0 分鐘 |
| 3 | **縮小常駐上下文**：壓縮 `copilot-instructions.md`，並把 `AGENTS.md` 修剪到只留下地雷項。這兩個檔案中的每一個 token，都會在每次互動（以及每一步 agent 執行）中被計費。刪掉填充內容、刪掉 agent 看程式碼就能自己發現的資訊、刪掉由 LLM 產生的 `/init` 樣板 | 降低常駐輸入／上下文 | 15 分鐘 |
| 4 | **預設使用 Auto 模型選擇**：把 Auto 當作基準，因為它會從支援的 Auto 模型池中自動挑選，並提供付費方案折扣。只有在任務明確值得時，再手動鎖定較高成本的模型。詳見 [Model Selection & Pricing](docs/11-models-and-pricing.zh-TW.md) | 降低符合條件用量的計費單價 | 0 分鐘 |
| 5 | **簡單問題用 Ask 模式**：多步驟工作再交給 Agent Mode | 避免 agent 額外開銷 | 0 分鐘（只要選對模式） |
| 6 | **用 `applyTo:` 路徑限制上下文**：把一份很大的 instructions 檔拆成數個小檔，只在相關情境載入 | 降低常駐輸入／上下文 | 15 分鐘 |
| 7 | **提示詞要精準**：像是「幫 `getUser()` 加上 null 檢查」，而不是「你可以幫我看看這裡，順便加一些錯誤處理嗎？」注意：你自己輸入的 prompt 只占總輸入的一小部分；精準對品質的幫助，大於它對原始 token 節省的幫助 | 提升任務聚焦程度 | 0 分鐘 |
| 8 | **依目標模型重調提示詞**：不同 provider 的 prompting 指南會隨模型與版本變動。把官方指南網址貼進 Copilot，請它依你實際使用的模型，調整 `.github/copilot-instructions.md`、agent profiles 或 app prompts | 減少返工 | 每次模型變更約 10 分鐘 |
| 9 | **稽核你的 MCP servers**：停用沒在用的 server；每個 server 都可能讓每一步 agent 額外增加約 100-500 個 token | 移除工具／schema 額外負擔 | 5 分鐘 |
| 10 | **先把富格式檔案轉成 Markdown 再交給 AI**：`.docx`、`.pdf`、`.pptx`、`.xlsx`、HTML、圖片、音訊、影片與 ZIP 都帶有格式稅。[Marc Bara 的文章](https://medium.com/@marc.bara.iniesta/your-docx-is-wasting-33-of-your-ai-budget-86a3d229d042) 已示範這類成本；在 chat、agent 或 RAG 匯入前，先用 [Microsoft MarkItDown](https://github.com/microsoft/markitdown) 轉成乾淨的 Markdown | 降低雜訊輸入／上下文 | 5 分鐘 |
| 11 | **每週執行 `/chronicle improve`**（**僅限 Copilot CLI**，實驗性功能）：這個 slash command 只能在互動式 Copilot CLI 工作階段中使用，並不是一般 Copilot Chat 功能。它會找出你 CLI 工作階段歷史中反覆出現的誤解，並產生自訂指令，讓同樣的誤判不再持續浪費 token | 降低重複返工 | 每次 2 分鐘 |
| 12 | **長工具鏈任務可考慮 CodeAct**（**僅限 Copilot CLI**，可選的外部外掛）：[`copilot-codeact-plugin`](https://github.com/jsturtevant/copilot-codeact-plugin) 可以把多步驟工具鏈收斂成一次沙箱執行，減少重複重播 system prompt、先前訊息與工具定義的次數 | 降低工具迴圈重播成本 | 10-15 分鐘 |

**如果你是從企業治理或客戶治理的角度來看，而不是個人設定最佳化？** 請直接從 [Enterprise Governance](docs/12-enterprise-governance.zh-TW.md) 開始。那一章涵蓋 AI 點數預算、針對個別使用者收緊權限、模型存取政策、組織層級指示，以及何時值得為了治理需求拆分成不同組織。

*上表數字僅針對各列所述機制，不可直接相加，也不代表總體帳單降幅。*

輸出控制（#1、#2）會立刻生效，而且會持續累積回報：設定一次，每次呼叫都省。結構性的輸入控制（#3、#6）會在每一次互動中持續累積效益。模型路由（#4、#5）會從計費層級直接降低成本。針對模型調整提示詞（#8）則透過提升首次回應品質來減少浪費。MCP 稽核（#9）可以直接砍掉每次 agent 任務中那些隱藏的 token 成本。Markdown 轉換（#10）則能在模型看到內容前，先移除 DOCX／PDF／HTML 的版面與標記雜訊。

---

## 指南內容

### Part 1：為什麼 Token 很重要

了解 BPE tokenization、token 為何會影響成本／速度／限制，以及 GitHub Copilot 在底層如何使用 token。

→ **[閱讀 Part 1](docs/01-why-tokens-matter.zh-TW.md)**

---

### Part 2：各種技巧

#### [2.1 Prompt Compression](docs/02-prompt-compression.zh-TW.md)

原始人式簡寫、強度分級（lite／full／ultra）、結構化格式、縮寫，以及以程式碼為中心的 prompting。可節省 30-50% 的輸入 token；搭配輸出控制（2.4）時，也能一起減少輸出。

#### [2.2 Language Comparison](docs/03-language-comparison.zh-TW.md)

以資料為基礎的比較：在這些範例裡，英文是最省 token 的語言。CJK 成本高出 1.7-2.4 倍。內含 8 種語言的 tokenization 表格。

#### [2.3 Context Management](docs/04-context-management.zh-TW.md)

壓縮 system instructions、壓縮記憶檔、用 `applyTo` 限定上下文、關閉未使用的編輯器分頁、在 AI 工作前先把非純文字檔轉成 Markdown、設定 Content Exclusion（Business／Enterprise 管理員可用），以及在需要時開新對話。重點是控制實際送進模型的內容。

#### [2.4 Output Control](docs/05-output-control.zh-TW.md)

「`Code only, no explanation.`」限制回應格式，並把精簡輸出設成專案預設。

#### [2.5 Workflow Optimization](docs/06-workflow-optimization.zh-TW.md)

精簡 commit 訊息、單行 PR review、Ask 與 Agent mode 的選擇、針對模型調整提示詞，以及什麼情況下**不該**壓縮。

#### [2.6 The Always-On Context Problem](docs/07-agents-md-problem.zh-TW.md)

關於 LLM 產生的上下文檔案的研究顯示，這些檔案常常在增加 token 成本的同時，還會降低 agent 的正確性。這個教訓同樣適用於 `AGENTS.md` 與 `.github/copilot-instructions.md`：兩者雖然是不同慣例（檔名不同、歷史來源也不同），但在今天的 Copilot 裡，它們都會成為常駐上下文。無論你的 repo 用的是哪一種檔案，都應該採用「只留地雷項」的原則。把上下文檔當成 bug tracker，不要當成 wiki。

#### [2.7 MCP & Tool Costs](docs/08-mcp-tool-costs.zh-TW.md)

隱性的 token 稅：每個 MCP tool 都會讓每一步 agent 額外增加 100-500 個 token。15 個 servers × 15 個步驟 = 26.5 萬個額外 token。內含稽核指南。

---

### Part 3：比較與資料

提示詞的正面對決比較、各語言 tokenization 表格、完整的技巧矩陣（40+ 種技巧），以及搭配效益遞減曲線的品質影響評估。

→ **[閱讀 Part 3](docs/09-comparisons-data.zh-TW.md)**

---

### Part 4：實際設定

逐步說明：如何設定 Copilot、最佳化 Coding Agent、設定 agent mode，以及建立使用習慣。包含 VS Code 設定、決策框架與 4 週導入計畫。

→ **[閱讀 Part 4](docs/10-practical-setup.zh-TW.md)**

---

### Part 4.2：Model Selection & Pricing

專門說明模型、PRU 時代的倍率歷史、目前的 Auto 使用建議、不同方案可用性，以及在 Copilot 尚未公開各模型精確 UBB 費率表的情況下，供應商輸入／輸出 token 定價應如何納入考量。內含 GitHub Docs 官方頁面的連結，涵蓋 Auto 模型選擇、計費，以及方案／模型可用性。

→ **[閱讀 Part 4.2](docs/11-models-and-pricing.zh-TW.md)**

---

### Part 4.3：Enterprise Governance

專為面向客戶的管理情境而寫的章節：涵蓋按使用量計費的防護措施、AI 點數預算、針對個別使用者收緊權限、模型存取政策、組織層級指示，以及何時值得承擔額外負擔、拆分成不同組織。

→ **[閱讀 Part 4.3](docs/12-enterprise-governance.zh-TW.md)**

---

如果你需要 glossary、quick terms、tools，或核心外部連結，請前往 [Guide Home](docs/index.zh-TW.md)。

---

## 影響最大的技巧

依成本影響排序。先看輸出，因為它每個 token 的成本是輸入的 5 倍。

1. **控制輸出**：`Code only, no explanation`，再加上 `copilot-instructions.md` 裡的精簡預設。程式任務可省 40-70% 的輸出，整體互動可省 30-60%。一條指令，永久生效。
2. **縮小常駐上下文**（`copilot-instructions.md` + `AGENTS.md`）：壓縮填充內容、只留地雷項、刪掉 LLM 產生的樣板。這會在每次互動與每一步 agent 執行中持續累積效果；agent 任務可降低 20-23%，而且正確性更好。
3. **簡單問題使用 Ask Mode**：避免 Agent 額外開銷，可節省 60-90%。
4. **稽核 MCP servers**：停用沒在用的 servers，每次 agent 任務可省下 5 千到 19 萬個 token。
5. **使用 Auto 模型選擇**：以更低成本的預設路由加上付費方案折扣達成節省，幾乎零成本導入。
6. **先把富格式檔案轉成 Markdown**：避免在 chat、agent 與 RAG 工作流中為 Word／PDF／HTML 的版面雜訊付費。
7. **依目標模型重調提示詞**：提升第一次輸出的品質，減少來回澄清。
8. **精準提示詞**：可影響使用者提示詞輸入 token 的 20-40%；對品質的幫助通常比對原始節省更重要。

---

*這是一份會持續更新的文件。隨著 tokenizer 技術演進、模型能力改變，以及新技巧出現，這份指南也會持續更新。請查看此 repository 以取得最新版本。*
