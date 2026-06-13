# 模型選擇與定價

[English](11-models-and-pricing.md) | [繁體中文（台灣）](11-models-and-pricing.zh-TW.md)

[← 返回指南](index.md)

---

這一頁存在的原因，是因為「模型怎麼選」與「費用怎麼看」很容易被混在一起。這裡其實有三種不同的定價視角：

1. **GitHub Copilot 官方文件**
2. **本 repo 對 UBB 的理解框架**
3. **模型供應商 API 的每 token 定價**

不要把這三者當成同一種單位。

## 你真正想看的官方 GitHub 文件

- [About Copilot auto model selection](https://docs.github.com/en/copilot/concepts/auto-model-selection)
- [Requests in GitHub Copilot](https://docs.github.com/en/copilot/concepts/billing/copilot-requests)
- [Plans for GitHub Copilot](https://docs.github.com/en/copilot/get-started/plans)

這三頁大致上涵蓋實作者最需要知道的：

- 有哪些模型
- 哪些方案可以用
- 哪些是 included、哪些是 premium
- Auto 真正怎麼運作

## 關於 Auto 最重要的澄清

repo 中一直建議把 **Auto** 當預設，這個方向仍然正確，但要更精準理解：

- Auto 會從**支援的 Auto pool** 中選
- 選擇依據是即時系統狀態與模型表現
- 在付費方案中，Copilot Chat 的 Auto 可能有 **10% 折扣**
- Auto 不等於「自動幫你升到每一種 premium 模型」

> **實務後果：** Auto 是低摩擦的預設通道；如果你真的要更高成本 premium 模型，通常要自己手動 pin。

## 三種定價視角各自回答什麼問題

| 視角 | 單位 | 適合回答的問題 |
|------|------|----------------|
| GitHub 公開 Copilot 計費 | 模型倍率、AI credits | Copilot 裡官方怎麼描述這模型的成本？ |
| Repo 的 UBB 框架 | AI credits、預算 | Business / Enterprise 在 2026/06/01 後該怎麼看用量？ |
| Vendor API pricing | 每百萬 token 單價 | 原始 token 成本如何分別體現在輸入與輸出？ |

各視角官方來源：[GitHub Copilot 計費 — Requests](https://docs.github.com/en/copilot/concepts/billing/copilot-requests)、[計量產品預算設定](https://docs.github.com/en/billing/how-tos/budgets/setting-up-budgets-to-control-spending-on-metered-products)、[Anthropic Pricing](https://platform.claude.com/docs/en/about-claude/pricing)。

## 輸入與輸出定價的關係

GitHub 目前沒有公開各 Copilot 模型的「輸入 token 單價 vs 輸出 token 單價」表。  
但 Anthropic API 定價仍然非常適合拿來理解「輸出遠比輸入貴」這件事。

| 模型 | 每百萬輸入 | 每百萬輸出 |
|------|------------|------------|
| Claude Haiku 4.5 | $1 | $5 |
| Claude Sonnet 4.6 | $3 | $15 |
| Claude Opus 4.6 | $5 | $25 |

來源：[Anthropic Pricing](https://platform.claude.com/docs/en/about-claude/pricing)。

這能幫你建立正確直覺：

- 輸出 token 的成本明顯更高
- 冗長回覆比多打一點 prompt 更容易把成本拉高
- 所以輸出控制依然是最有價值的習慣之一

## Reasoning Effort 是另一個成本旋鈕

模型不是唯一選項。對支援推理的模型，**thinking effort / reasoning effort** 也是成本控制項。

| 情境 | 建議 effort | 原因 |
|------|-------------|------|
| 高頻、簡單聊天或分類 | `low` | 最省 |
| 一般 coding、refactor、工具密集工作 | `medium` | 品質與成本平衡最好 |
| 架構、安全審查、全新分解問題 | `high` 或 `max` | 只有真的值得時才拉高 |

> **重點：** 只有支援 reasoning 的模型才有這個旋鈕。

因此完整決策鏈應是：

1. 先選對模型層級
2. 如果該模型支援，再選最低但足夠的 reasoning effort

## 實際上該怎麼做

### 預設立場

1. **日常工作預設用 Auto**
2. **瑣碎任務用 included 或較便宜模型**
3. **只有明顯值得時才手動 pin premium 模型**
4. **組織層面要先看 model policy，再擴大 premium 存取**

### 好用的預設 heuristics

| 任務 | 建議選擇 | 原因 |
|------|----------|------|
| 語法查詢、簡單說明、小修改 | Included model 或 Auto | 最便宜的路就夠用 |
| 一般實作、修 bug、重構 | Auto 或標準模型 | 品質／成本比最好 |
| 架構、threat modeling、全新拆解 | 手動 pin premium | Auto 不會自動跳進 premium lane |

### 反模式

- 整個 session 都釘著昂貴 premium 模型
- 以為 Auto 會在任務變難時自動幫你升到 Opus
- 把 vendor API 價格與 Copilot 價格信號當成同一件事
- 沒確認方案支援就推薦模型
- 還沒確認實際需求就對整個組織開啟所有 premium 模型

## 組織推行原則：啟用前先審查

團隊層面的模型選擇同時是治理問題，不只是 prompt 問題。

實務建議：

1. 先開較便宜模型
2. 依 workflow、團隊與 ROI 審 premium 需求
3. 小範圍啟用 premium
4. 看 usage reports 與 AI credits 消耗，再決定是否擴大

組織擁有者與企業擁有者可用 [Configuring access to AI models in Copilot](https://docs.github.com/en/copilot/using-github-copilot/ai-models/configuring-access-to-ai-models-in-copilot) 控制成員能存取哪些 AI 模型。

## Repo 內交叉參照

- [Practical Setup](10-practical-setup.zh-TW.md)
- [Workflow Optimization](06-workflow-optimization.zh-TW.md)
- [Enterprise Governance](12-enterprise-governance.zh-TW.md)
- [Guide Home](index.md)

---

**下一章：** [Enterprise Governance →](12-enterprise-governance.zh-TW.md)
