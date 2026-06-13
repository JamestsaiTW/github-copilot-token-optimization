# Copilot 成本控制的企業治理

[English](12-enterprise-governance.md) | [繁體中文（台灣）](12-enterprise-governance.zh-TW.md)

[← 返回指南](index.zh-TW.md)

---

這一頁是寫給組織與企業管理員的。目標是：**在 GitHub 有文件支援的前提下控制成本，不自己發明不存在的控制機制。**

## 真正控制成本的是什麼

最重要的三個槓桿：

1. 預算上限
2. 使用者層級預算控制
3. 模型可用性

Prompt 壓縮依然重要，但那是**用量效率**槓桿，不是管理員計費控制。

## 1. 先設定預算

在 2026 年 6 月 1 日之後，Business 與 Enterprise 的治理主軸改成 AI credits 與 usage-based billing。可參考 GitHub 的[組織與企業 usage-based billing 指南](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-organizations-and-enterprises)與[計量產品的預算設定文件](https://docs.github.com/en/billing/how-tos/budgets/setting-up-budgets-to-control-spending-on-metered-products)。

GitHub 文件中的重點：

- 可以在 organization、enterprise 或 cost center 層級設預算
- 可以設定達到預算時停止使用
- 也有 user-level budgets
- **使用者預算設為 `$0`** 代表該使用者無法使用 usage-based 功能

要注意一個重點：預算**不會**讓 prompt 變小，也**不會**減少每個 prompt 的 token，它只是替 AI credit 支出設上限。

實務預設：

1. 先用非零測試預算啟動 rollout
2. 提早開 alerts
3. 觀察報表正常後，再開 stop usage
4. 每月固定檢查，不要等超支才看

## 2. 用 User-Level Budgets 做每人收緊

對 Business / Enterprise 來說，2026/06/01 之後最乾淨的每人上限，就是 GitHub [usage-based billing 指南](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-organizations-and-enterprises)所記載的 **user-level AI credit budget**。文件明確指出：使用者預算設為 **`$0`** 代表該使用者無法使用 usage-based 功能。

管理思維應轉成：

- 先看 AI credit 用量
- 再看模型選擇、聊天深度、agent 時長

實務模式：

1. 一般使用者配低一些的 user-level 預算
2. 重度使用者只有在工作需要明確時才提高
3. 每月檢查，價值不明顯的使用者再降回來

> **舊制備註：** 若你還在為 6/1 之前的客戶做準備，[premium request management](https://docs.github.com/en/copilot/concepts/billing/premium-request-management) 說明的是即將淘汰的控制模型，只能當成過渡期指引。

## 3. 啟用模型前先審查

GitHub 支援由 organization 或 enterprise owner 控制成員可用的 AI 模型，做法見[在 Copilot 中設定 AI 模型存取](https://docs.github.com/en/copilot/using-github-copilot/ai-models/configuring-access-to-ai-models-in-copilot)。
把這當成**官方支援的模型治理方式**。

建議的審查清單：

1. 哪些 workflow 真的需要 premium 模型
2. 哪些團隊會產生可量化價值
3. 哪些使用者維持 Auto 或 included models 就足夠
4. 啟用後要看哪份 usage report
5. 若成本跳升卻沒有品質收益，要用什麼 rollback 條件

## 4. 把 Custom Instructions 放在正確層級

GitHub 文件區分：

- **repository instructions**（見[新增 repository custom instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)）
- **organization instructions**（見[新增 organization custom instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-organization-instructions)）

重要的是它們的套用範圍不同。  
尤其對成本控制來說，要注意：

- 組織層級 instructions 不要假設在 IDE 一定生效
- 如果你想讓 VS Code 或 JetBrains 也有精簡行為，應該把關鍵 always-on 規則放在 **repo instructions**

建議分工：

- **Org instructions：** 廣泛政策、review 提醒、GitHub.com surfaces 的跨 repo 規則
- **Repo instructions：** coding、build、精簡輸出等 IDE 也需要的規則
- **Path-specific instructions：** 只有局部需要的細規則

## 5. 分開組織可行，但只是有條件的做法

若你需要不同的 org-level model policies 或獨立 billing boundary，拆成不同 organizations 可能有用。

但這不是萬靈丹，代價包括：

- 更多管理成本
- license 分配更複雜
- 使用者若跨多 org，流程更麻煩

只有當政策或計費邊界真的值得時，才考慮這條路。

## 6. 量測正確的東西

請看 GitHub usage reports 與 AI-credit reporting，重點問這四件事：

1. 哪些團隊最常超過基線支出
2. 哪些使用者消耗最多 AI credits
3. 哪些模型真的和更好結果有關，而不是只是習慣
4. 哪些 agent workflows 花很多錢，卻沒有相稱交付價值

外部 benchmark 可以做補充，但不能取代你自己的 Copilot usage data。[llm-stats.com](https://llm-stats.com/) 可當成獨立的參考點，但請把它當成**補充性 benchmark**，既不是 GitHub 官方指引，也不能取代你自己的 Copilot usage reports。

## 7. 6 月 1 日切換清單

如果你在幫客戶準備 2026 年 6 月 1 日的切換：

1. 把管理思維從 request counters 轉成 AI-credit budgets
2. 先決定哪些使用者需要緊 user-level budgets
3. 在 frontier models 變成直接成本前，先審模型可用性
4. 提醒團隊：code completions 與 next edit suggestions 不計入 AI credits
5. 優先觀察長 chat 與 agent workflows，因為它們最容易放大支出

## 建議的企業預設

1. 預設模型路徑用 Auto
2. 廣泛 rollout 前先設預算
3. 需要時用 user-level AI credit budgets 做更細控制
4. premium 模型先審後開
5. repo instructions 保持小而精
6. 只有在 cost center／政策邊界真的合理時才拆 org

這套做法刻意很無聊：**先用便宜預設，再用例外方式擴 premium，最後用量測結果決定是否擴張。**
