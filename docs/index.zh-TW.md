# Token 最佳化指南

[English](index.md) | [繁體中文（台灣）](index.zh-TW.md)

實務導向的 GitHub Copilot token 成本降低指南，同時維持回答與程式碼的實用性。

[從 Part 1 開始](01-why-tokens-matter.zh-TW.md){ .md-button .md-button--primary }
[直接看實際設定](10-practical-setup.zh-TW.md){ .md-button }

## 這份指南涵蓋什麼

- 為什麼在 Usage-Based Billing 下，token 真的會影響成本
- 為什麼輸出控制通常比 prompt 壓縮更有直接 ROI
- 如何縮小 always-on context、歷史訊息與工具負擔
- 為什麼依模型調整 prompt guide 能提升第一次回答品質並減少返工
- Ask、Edit、Agent Mode 分別何時最划算
- 如何建立企業治理，而不是依賴未被官方支援的控制方式
- 如何把這些做法變成可重複的團隊習慣

## 最快見效的做法

1. 預設限制輸出：`Code only, no explanation.` 與 `No explanations unless asked.`
2. 讓 `.github/copilot-instructions.md` 保持小而精準。
3. 不需要工具的問題就用 Ask Mode。
4. 依目標模型的官方指南重調 prompts 與 instructions。
5. 停用沒在用的 MCP servers。
6. 稽核長時間 agent sessions 與重複來回澄清。
7. 安裝 [RTK](https://github.com/rtk-ai/rtk)，壓縮 shell 指令輸出。

## 依主題閱讀

### Foundations

- [Why Tokens Matter](01-why-tokens-matter.zh-TW.md)
- [Comparisons & Data](09-comparisons-data.zh-TW.md)

### Techniques

- [Context Management](04-context-management.zh-TW.md)
- [Output Control](05-output-control.zh-TW.md)
- [Workflow Optimization](06-workflow-optimization.zh-TW.md)
- [MCP & Tool Costs](08-mcp-tool-costs.zh-TW.md)

### Implementation

- [Practical Setup](10-practical-setup.zh-TW.md)
- [Model Selection & Pricing](11-models-and-pricing.zh-TW.md)
- [Enterprise Governance](12-enterprise-governance.zh-TW.md)

## 快速詞彙

- **UBB**：usage-based billing。Copilot Business 與 Enterprise 的花費會透過 AI credit 用量計算。
- **AI credits**：切換後的共用計費單位。
- **Auto mode**：Copilot 預設模型選擇器。多數情境下是合理的預設通道。
- **Ask Mode**：單次互動。最省成本。
- **Agent Mode**：多步驟互動。槓桿高，但成本也高。
- **Content Exclusion**：管理員用來讓特定 repo 內容不進 Copilot context 的控制項。

## 實用連結

- [Official GitHub Copilot docs](https://docs.github.com/copilot)
- [Usage-based billing for organizations and enterprises](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-organizations-and-enterprises)
- [OpenAI Tokenizer](https://platform.openai.com/tokenizer)
- [Awesome GitHub Copilot Customizations](https://github.com/github/awesome-copilot-customizations)
- [LLMLingua](https://github.com/microsoft/LLMLingua)
- [Caveman project](https://github.com/JuliusBrussee/caveman)
- [RTK — Rust Token Killer](https://github.com/rtk-ai/rtk)
- [Dina Berry：How I Cut Token Usage from 52% to 13%](https://dfberry.github.io/2026-05-06-tuning-up-copilot-context)

## 備註

- 完整 `/chronicle` 是 **Copilot CLI** 功能；`/chronicle:tips` 也可在 **VS Code** 使用。
- 本 repo 中的 Usage-Based Billing 縮寫為 **UBB**。
