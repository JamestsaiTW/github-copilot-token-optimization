# Part 1：為什麼 Token 很重要

[English](01-why-tokens-matter.md) | [繁體中文（台灣）](01-why-tokens-matter.zh-TW.md)

[← 返回指南](index.md)

---

## 1.1 什麼是 Token？

Token 是大型語言模型讀寫時使用的基本單位。它不是單字，也不是字元，而是由 Byte-Pair Encoding（BPE）切分出來的**子詞**。

### BPE 如何運作

1. 從原始位元組開始（共 256 種可能值）
2. 找出訓練資料中最常出現的位元組配對
3. 把這些配對合併成新的 token
4. 持續重複，直到詞彙表規模達到約 10 萬個 token

結果就是：常見英文單字通常會變成單一 token，而較少見或較長的詞則會被拆成多段。

### 範例

| 文字 | Token | 數量 |
|------|--------|------|
| `hello` | `hello` | 1 |
| `unhappiness` | `un` + `happiness` | 2-3 |
| `authentication` | `authentication` | 2-3 |
| `I met a huge dog` | `I` `met` `a` `huge` `dog` | 5 |
| `Sure, I'd be happy to help you with that!` | （每個詞與標點） | 約 10 |

最後這個例子很關鍵：10 個 token，幾乎沒有資訊量。這就是 token 最佳化的核心洞察。

**關鍵事實：** 在 Claude 3 tokenizer 中，最常見的 10,000 個英文詞裡，有 8,311 個會被切成單一 token。常見字詞很便宜；填充詞雖然也常只要 1 個 token，但幾乎沒有價值。

## 1.2 為什麼你該在意

你送出或收到的每一個 token 都有成本：

| 面向 | 影響 |
|------|------|
| **成本** | Token 就是錢。API 定價以 token 為基礎，GitHub Copilot 的使用限制也和 token 有關。**最重要的不對稱點是：輸出 token 每個 token 的成本約是輸入的 5 倍**（Anthropic：每百萬 token 的輸入／輸出價格為 Haiku 1／5 美元、Sonnet 3／15 美元、Opus 5／25 美元）。Copilot 的 UBB 也採用相同桶位概念，因此每一句你其實不需要的回覆，都可能比你 prompt 裡同一句話貴上 5 倍。輸出控制是本指南中每個 token ROI 最高的技巧。 |
| **速率限制** | 每次請求用越少 token，在觸發上限前能發出的請求就越多。 |
| **Context window** | 輸入（prompt + context）與輸出（回應）共享有限空間。輸入浪費越多，輸出可用空間就越少。 |
| **速度** | 輸入 token 越少，第一個 token 出現得越快，回覆真的會更快。 |
| **計費** | 自 2026 年 6 月 1 日起，GitHub Copilot 針對用量採用 **usage-based billing（UBB）**。每次互動會落在三種計費桶：輸入 token（prompt + context + history）、輸出 token（回應內容）、以及快取 token（重複利用的 context，通常以輸入費率約 10% 計費）。成本 =（輸入 × 輸入費率）+（快取 × 快取費率）+（輸出 × 輸出費率）。Business 與 Enterprise 席次則含有組織共用的 AI credits（CB 每席次 30 美元、CE 每席次 70 美元）。程式碼補全（code completion）維持不計入用量。 |

**複利效應：** 你的輸入 token 大多不是來自你打的字，而是來自檔案內容、對話歷史、system prompt 與 MCP 工具 schema。你自己輸入的 prompt 常常只有 5–100 個 token，但 agent mode 的總輸入可能到 5,000–50,000+。最大的輸入槓桿通常是結構性調整，例如 instruction 檔大小、分頁管理與 context 範圍控制。每 token 成本影響最大的則是輸出：因為價格高 5 倍，而且可以靠 `copilot-instructions.md` 裡一行設定直接控制。

## 1.3 GitHub Copilot 如何使用 Token

了解 Copilot 背後實際做了什麼，才能知道該怎麼最佳化：

```text
┌─────────────────────────────────────────────────┐
│                 Context Window                  │
│                                                 │
│  ┌──────────────────┐  ┌─────────────────────┐  │
│  │  INPUT TOKENS    │  │  OUTPUT TOKENS      │  │
│  │                  │  │                     │  │
│  │  System prompt   │  │   你收到的回應       │  │
│  │  + copilot-      │  │                     │  │
│  │    instructions  │  │                     │  │
│  │  + file context  │  │                     │  │
│  │  + conversation  │  │                     │  │
│  │    history       │  │                     │  │
│  │  + 你的 prompt   │  │                     │  │
│  └──────────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────┘
```

- **System prompt：** Copilot 自身的內建指示（你無法控制）
- **`copilot-instructions.md`：** 專案層級指示，**每次互動都會載入**
- **File context：** 你用 `#file` 指到的檔案，以及 Copilot 自動帶入的內容（開啟分頁、imports、附近檔案）
- **Conversation history：** 目前對話中的所有先前訊息
- **你的 prompt：** 你實際輸入的內容

**隱性負擔：** Copilot 還會加入你看不到的 context，例如 repo 結構、檔案內容與 import graph。這就是為什麼你打了 20 個字，實際輸入卻可能消耗 2,000+ token。

**Coding Agent 的乘數效應：** GitHub Coding Agent 會執行多步驟工作階段。每一步都要讀檔、判斷、寫程式，因此從 issue 到 PR 的一次工作流程，常常就會吃掉數萬個 token。任何節省都會在這些步驟中持續放大。

## 1.4 這份指南適合誰

- **GitHub Copilot Chat 使用者**：主要讀者，大多數技巧都適用
- **GitHub Copilot Inline／Edits 使用者**：部分技巧適用（prompt 控制較有限）
- **GitHub Coding Agent 使用者**：高價值族群，因為長工作階段會把節省放大
- **任何重視效率的人**：即使你沒有碰到限制，更快回應與更乾淨的互動仍然值得

---

**下一章：** [Prompt Compression →](02-prompt-compression.zh-TW.md)
