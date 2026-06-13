# 2.6 Always-On Context 問題：為什麼更少通常更好

[English](07-agents-md-problem.md) | [繁體中文（台灣）](07-agents-md-problem.zh-TW.md)

[← 返回指南](index.zh-TW.md)

---

> **不同慣例，相同成本型態。** `AGENTS.md`、`.github/copilot-instructions.md`、`CLAUDE.md` 各自有不同來源與用途，但共同點是：只要工具會在每次互動載入它，它們就屬於 **always-on context**。本章雖然以 `AGENTS.md` 研究為主，但原理也適用於任何常駐 instruction 檔。

## 2.6.1 研究發現：Context Files 常常有害

很多人預設認為：**更多 context = 更好結果。**

ETH Zurich 的研究（Gloaguen 等，AGENTBENCH，2026 年 2 月）在 12 個 repositories、138 個任務與 4 種 coding agents 上測試後，得到的結果是：

| 發現 | 資料 |
|------|------|
| LLM 產生的 context files 會降低表現 | 8 種設定中有 5 種表現下滑 |
| 平均正確率變化 | **−2%** |
| 使用 LLM 產生 context file 的成本增加 | **多 20-23% tokens** |
| GPT-5.2 reasoning overhead | **多 22% reasoning tokens** |

結論不是中性，而是：**常見的 LLM 產生 context files 會讓 agent 更差，還更貴。**

## 2.6.2 人寫的檔案也只是小幅幫助

人工撰寫的 context files 表現稍好，但不穩定：

| 模型 | 人工 context file 的效果 |
|------|--------------------------|
| 跨模型平均 | 約提升 4%，但不一致 |
| Claude Code | 反而更差 |
| 檔案發現率 | 有無 context file 幾乎一樣 |

最後一點很重要：agent 本來就會 `ls`、`grep`，它不需要 context file 才知道怎麼找檔案。

## 2.6.3 為什麼更多 Context 反而會傷害效果

四個常見機制：

1. **Redundancy tax：** 檔案裡的資訊，agent 本來就能從程式碼自己找到
2. **Attention tax：** 太長的檔案會讓重要規則埋在中間被忽略
3. **Anchoring trap：** Agent 會過度服從過時或次佳的指示
4. **Signal-to-noise ratio 下降：** 低價值 context 會稀釋真正重要的專案地雷

## 2.6.4 效率與正確率不是同一件事

有研究指出人工撰寫的 `AGENTS.md` 可以降低執行時間與輸出 token，但那測的是**效率**，不是**正確率**。

重點不是 agent 能不能更快到答案，而是能不能到**對的答案**。  
而且更快的導航節省，常常會被處理 context file 本身增加的成本抵銷。

## 2.6.5 那到底該放什麼

Addy Osmani 的篩選法很實用：

> **「Agent 能不能光靠讀程式碼自己發現？如果可以，就刪掉。」**

| 保留 | 刪掉 |
|------|------|
| "Use `uv` instead of `pip`" | "This is a Python project" |
| "Run tests with `--no-cache`" | "Tests are in the `tests/` directory" |
| "Don't refactor the auth module" | "We use JWT for authentication" |
| "Deploy requires VPN connection" | "Main branch is protected" |
| "DB migrations must run in order" | "We use PostgreSQL" |

**模式很簡單：只留地雷，不留可發現資訊。**

## 2.6.6 把它當成 Bug Tracker

理想的維護方式：

```text
一開始幾乎空白。
Agent 踩到一次坑 → 補一行。
根因被修掉 → 刪掉那一行。
```

Context file 應該像 bug tracker 一樣增減，而不是像 wiki 一樣只增不減。

## 2.6.7 這個 Repo 的做法：6 行、約 50 Tokens

本專案的 `.github/copilot-instructions.md` 大約只有 6 行、約 50 tokens。

拿來對比典型 `/init` 產物：

- `/init`：200+ 行、約 1,500 tokens
- 本 repo：6 行、約 50 tokens

在 50 次互動或長 agent session 中，這種差距會非常驚人。

| 類型 | 每次載入 Tokens | 50 次互動 | Agent（20 steps） |
|------|----------------|-----------|-------------------|
| `/init` 產生 | 約 1,500 | 75,000 | 30,000 |
| 一般人工撰寫 | 約 400 | 20,000 | 8,000 |
| 極簡壓縮版 | 約 50 | 2,500 | 1,000 |

---

**下一章：** [MCP & Tool Costs →](08-mcp-tool-costs.zh-TW.md)
