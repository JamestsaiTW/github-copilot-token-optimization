# 2.5 工作流程最佳化

[English](06-workflow-optimization.md) | [繁體中文（台灣）](06-workflow-optimization.zh-TW.md)

[← 返回指南](index.md)

---

## 2.5.1 Commit 訊息

建議用 Conventional Commits。標題 ≤ 50 字；只有在「為什麼」不明顯時才寫 body。

**冗長版：**

```text
feat: Added a new feature to allow users to reset their passwords through
the settings page, which also sends a confirmation email
```

**精簡版：**

```text
feat: add password reset via settings page

Sends confirmation email on reset.
```

每則 commit 省的不多，但 Coding Agent 會讀 git history，整個 repo 累積起來就有差。

## 2.5.2 PR Review

比起長段評論，單行格式通常更省又同樣可執行：

```text
L42: bug: user can be null here. Add null guard before .email access.
```

常見嚴重度前綴：

- `🔴` Bug / security，必修
- `🟡` Suggestion，建議修
- `🔵` Nit，可選最佳化
- `❓` Question，需要釐清

## 2.5.3 Ask Mode vs. Agent Mode

這是整份指南裡省 token 效果很大的決策之一。

**Agent Mode** 可能為每個可見動作觸發 3-10 次以上內部模型呼叫。  
**Ask Mode** 通常就是一次呼叫、一個回答。

| 任務 | 建議模式 | 原因 |
|------|----------|------|
| "What does this function do?" | Ask | 單次回答，不需要工具 |
| "What's the TypeScript syntax for generics?" | Ask | 單純知識問題 |
| "Refactor this module to use dependency injection" | Agent | 多檔案變更 |
| "Create a REST API with tests and docs" | Agent | 多步驟建立 |
| "Why is this test failing?" | Ask（通常） | 多半只需要你提供錯誤與上下文 |

**簡單問題選 Ask**，通常能省下 60-90%。

### Copilot CLI 的例外：CodeAct

如果你主要是在 **Copilot CLI** 裡跑很多工具鏈，外部外掛 [`copilot-codeact-plugin`](https://github.com/jsturtevant/copilot-codeact-plugin) 值得評估。它把原本多輪的 model → tool → model 循環收斂成一次沙箱執行。

它可能節省 token 的原因：

- 減少 system prompt、歷史訊息與工具定義的重播次數
- MCP 工具 catalog 載入次數也會跟著下降
- 整合後的結果通常比逐步敘述每一步更短

### 互補：用 RTK 壓縮工具輸出

CodeAct 減少的是工具呼叫的**次數**；[**RTK (Rust Token Killer)**](https://github.com/rtk-ai/rtk) 減少的則是每次工具結果的**大小**，兩者可搭配使用。RTK 是 CLI proxy，會攔截 `git`、`cargo test`、`grep`、`ls` 等 100+ 種開發指令，在輸出回灌給 agent 前先壓縮，每個指令可省 60–90%。設定方式與完整指令清單見 [MCP & Tool Costs §2.7.7](08-mcp-tool-costs.zh-TW.md#277-rtk)。

## 2.5.4 預設使用 Auto 模型選擇

模型選擇器本身就是重要的成本控制介面。把高成本模型長時間釘住，代表連最簡單的互動都會用高費率計價。

**正確預設是 Auto。**

- Auto 會從支援的 Auto pool 中選擇
- 在付費方案上，符合條件時會套用折扣
- 它不是「自動幫你升到最貴模型」，高成本 premium 模型通常仍要手動 pin

只有在你清楚知道任務很簡單或很重，才手動指定模型。

## 2.5.5 依目標模型重調 Prompt

這不是每次都能直接減少單次 token，而是透過提升第一次回答品質，減少補問、修正與 agent 返工。

建議流程：

```text
打開目標模型的官方 prompting guide。
把網址貼進 Copilot。
請 Copilot 依這份指南調整你的 instruction / prompt files。
保留行為不變，但減少錯誤回合與澄清成本。
```

各家官方 prompting guide 起點：

| 供應商 | 模型家族 | Prompting guide |
|---|---|---|
| Anthropic | Claude Sonnet / Opus / Haiku | [Prompt engineering 總覽](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)、[Claude 最新模型最佳實務](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) |
| OpenAI | GPT-5.5 / GPT-5 | [GPT-5.5 prompting guide](https://developers.openai.com/api/docs/guides/prompt-guidance)、[GPT-5 prompting guide](https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide) |
| Google | Gemini | [Gemini prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) |

適用時機：

- 換了預設模型
- 原本在某模型表現不錯的 prompt，在新模型變得太囉唆、太死板或太積極
- agent 換模型後開始反覆做同一種錯誤假設

## 2.5.6 什麼時候不該壓縮

以下情境不要過度壓縮：

- 安全警告
- 不可逆操作
- 新人 onboarding
- 容易因順序或歧義導致誤解的多步驟指令
- 法規／合規文字

## 2.5.7 用 `/chronicle` 關閉回饋迴路

Token 浪費不只發生在單一 prompt，也會發生在你沒察覺的重複模式上。  
[`/chronicle`](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/chronicle) 能分析你的本機 session 歷史，找出 Copilot 常誤解你的地方。

最有價值的是：

- **`/chronicle improve`**：找出反覆誤判，產生 custom-instruction 建議
- **`/chronicle tips`**：依你的使用模式給個人化改善建議
- **`/chronicle standup`**：整理工作狀態，偏流程幫助，非直接省 token

`improve` 的價值最大，因為它能把一再重複的浪費，轉成一次性的 instruction 修正。

## 2.5.8 VS Code 用量分析：AI Engineering Coach

`/chronicle` 偏向 Copilot CLI。  
對 VS Code，對應工具是 [AI Engineering Coach](https://github.com/microsoft/AI-Engineering-Coach)。

它會從本機的 VS Code AI session logs 中分析：

- 常見反模式
- token 使用型態
- context 健康度
- 技能與工作流缺口

它與 `/chronicle` 的關係是互補：

- `/chronicle` 修 prompt／instruction 的反覆失誤
- AI Engineering Coach 稽核整體 VS Code 使用結構

---

**下一章：** [The AGENTS.md Problem →](07-agents-md-problem.zh-TW.md)
