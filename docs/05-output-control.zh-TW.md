# 2.4 Output Control：告訴模型哪些話不要說

[English](05-output-control.md) | [繁體中文（台灣）](05-output-control.zh-TW.md)

[← 返回指南](index.md)

> **為什麼這章對成本最重要：** 在 Anthropic／Copilot UBB 的定價邏輯下，輸出 token 的單價約是輸入的 **5 倍**。即使回應長度通常小於總輸入，這個價差仍讓輸出控制成為全指南中 ROI 最高的手段之一。只要在 `copilot-instructions.md` 放上一句 `Code only, no explanation.`，許多程式任務的輸出成本就能永久減少 40–70%。

---

## 2.4.1 要求只輸出程式碼

LLM 很愛解釋。你只是要它產生 50 行程式碼，它卻可能多送你 200 tokens 的說明。

**加在 prompt 或 `copilot-instructions.md`：**

```text
Code only, no explanation.
```

也可以直接寫：

```text
Add input validation to processOrder(). Code only.
```

**節省幅度：** 程式產生類任務常可減少 40-70% 的輸出 token。

**取捨：** 如果你正在學習或除錯，就還是需要解釋。當你已經知道自己要什麼，只想拿到實作時，再開 `code only` 最合適。

## 2.4.2 限制回應格式

直接指定格式：

| 指令 | 效果 | 輸出節省 |
|------|------|----------|
| "Answer in one sentence" | 限制冗長程度 | 約 60-80% |
| "3 bullet points max" | 硬性限制項目數 | 約 50-70% |
| "Reply as JSON" | 結構化、無散文 | 約 30-60% |
| "Table format" | 適合比較、較緊湊 | 約 40-60% |
| "Yes or no, then one line why" | 回覆極短 | 約 70-90% |

## 2.4.3 在 System Level 設定精簡輸出

把精簡輸出設成專案預設，例如放進 `copilot-instructions.md`：

```text
Be concise. No explanations unless asked.
Code only for generation tasks.
Bullets over paragraphs.
```

這樣每次互動都自動套用，不用你每次再重打一次。

**節省幅度：** 幾乎每次互動都能省下約 30-60% 的輸出 token。

**何時覆蓋：** 你真的需要解釋時，直接明講即可，例如：`Explain why this approach is better than X.`

---

**下一章：** [Workflow Optimization →](06-workflow-optimization.zh-TW.md)
