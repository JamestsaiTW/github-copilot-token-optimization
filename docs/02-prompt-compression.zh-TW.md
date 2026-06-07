# 2.1 Prompt Compression：用更少的 Token 表達同一件事

[English](02-prompt-compression.md) | [繁體中文（台灣）](02-prompt-compression.zh-TW.md)

[← 返回指南](index.zh-TW.md)

---

## 2.1.1 原始人式簡寫

最有效的 token 最佳化技巧，就是把不增加資訊的語言骨架拿掉。

**該刪掉的：**

- 冠詞：a、an、the
- 填充詞：just、really、basically、actually、simply
- 客套話："Sure, I'd be happy to help!"、"Of course!"、"Certainly!"
- 模糊保留："I think maybe"、"it's probably"、"you might want to consider"

**該保留的：**

- 所有技術名詞，要精確
- 程式碼，不要改動
- 明確性，要更精準，不是更模糊

**前後對照：**

| 風格 | Prompt | 約略輸入 Token |
|------|--------|----------------|
| 冗長 | "Hey, could you please help me refactor this function? I think it might have some issues with how it handles the authentication, and I'd really like it to be more efficient. Thanks!" | 約 40 |
| 原始人式 | "Refactor function. Fix auth handling. Make efficient." | 約 10 |

這個例子可節省 **75%**。對本來就寫得相對精簡的開發者 prompt，常見節省幅度通常是 **30–50%**。

**常見模式：** `[物件] [動作] [原因]。[下一步]`

更多例子：

| 冗長版 | 原始人版 | 節省 |
|---|---|---|
| "Can you explain what this error message means and how I should fix it?" | "Explain error. How fix." | 約 69% |
| "I'd like you to add comprehensive error handling to this API endpoint, including validation of the request body." | "Add error handling to endpoint. Validate request body." | 約 55% |
| "Could you please review this pull request and let me know if there are any issues?" | "Review PR. Flag issues." | 約 71% |

## 2.1.2 壓縮強度分級

不是每個情境都適合同一種壓縮程度。這份指南採用三種英文強度：

### Lite：專業但精簡

刪掉填充詞與保留語氣，但保留冠詞與完整句子。

```text
"Your component re-renders because you create a new object reference
each render. Wrap it in useMemo."
```

適合：對外文件、需要完整清晰表達的情境。

### Full：經典原始人模式（預設）

拿掉冠詞，允許片語化，用更短的同義詞。

```text
"New object ref each render. Inline object prop = new ref = re-render.
Wrap in useMemo."
```

適合：日常開發、多數 Copilot 互動。

### Ultra：最大壓縮

常見術語直接縮寫，刪掉連接詞，用箭頭表示因果。

```text
"Inline obj prop → new ref → re-render. useMemo."
```

適合：高頻互動、你對領域非常熟時。

| 等級 | 輸入節省 | 輸出節省† | 品質影響 |
|------|----------|-----------|----------|
| Lite | 15-25% | 15-25% | 幾乎無 |
| Full | 30-50% | 40-55% | 可忽略 |
| Ultra | 55-70% | 55-70% | 複雜指令可能變模糊 |

†輸出節省要搭配 system-level 的精簡輸出設定，見 [Output Control](05-output-control.zh-TW.md)。

## 2.1.3 用結構取代散文

條列與 key-value 幾乎總是比段落省 token。

**散文版：**

```text
I need you to create a REST API endpoint that accepts POST requests at /api/users.
It should validate that the request body contains a name field (string, required)
and an email field (string, required, must be valid email format). If validation
fails, return a 400 status with error details. On success, save to the database
and return 201 with the created user object.
```

**結構化版：**

```text
POST /api/users
Validate:
- name: string, required
- email: string, required, valid format
400 on validation fail (include errors)
201 on success (return created user)
Save to DB
```

結構化寫法通常更省，也更清楚。

## 2.1.4 縮寫與簡寫

模型通常能很好理解這些常見縮寫：

| 縮寫 | 意義 |
|------|------|
| DB | Database |
| auth | Authentication/authorization |
| config | Configuration |
| req/res | Request/response |
| fn | Function |
| impl | Implementation |
| env | Environment |
| deps | Dependencies |
| repo | Repository |
| PR | Pull request |
| e2e | End-to-end |

**有幫助的情境：** 長指令裡反覆出現的術語。  
**會出問題的情境：** 模型沒看過的專案內部縮寫。

## 2.1.5 以程式碼為中心的 Prompt

有時候，程式碼比自然語言更省 token。

**自然語言：**

```text
Create a function that takes a list of numbers, filters out the negative ones,
doubles each remaining number, and returns the sum.
```

**偽碼：**

```text
fn(nums) → filter(>0) → map(*2) → sum
```

**型別簽章：**

```python
def process(nums: list[int]) -> int:
    # filter positive, double, sum
```

**「像 X，但改成 Y」：**

```text
Like getUserById but for emails. Return 404 if missing.
```

這幾種方式通常都能讓模型理解，但後三種更省。

## 2.1.6 重質不重量：縮小範圍，不要一直加規則

模型做錯時，常見直覺是再加更多規則。這幾乎都會更貴，通常也更差。

應該做的是：**提高 context 品質，而不是增加數量。**

| 症狀 | 錯誤作法 | 正確作法 |
|------|----------|----------|
| 模型漏掉 edge case | 把這個 edge case 永久加進 always-on instructions | 只在這次 prompt 提到 |
| 模型回覆太冗長 | 用五種不同說法一直要求簡潔 | 直接限制格式，例如「一行回答」 |
| Agent 走偏 | 再加更多全域規範 | 收緊這次 prompt：指定檔案、函式、完成條件 |
| 模型忘了慣例 | 每次都把慣例貼進 prompt | 放進 `applyTo` 範圍化 instruction 檔 |

小而明確的 prompt，通常也比較不會把 agent 帶進長時間的失焦探索。

## 2.1.7 宣告式護欄

比起逐步命令模型怎麼做，直接說明輸出必須滿足哪些條件，通常更短、更穩。

| 命令式 | 宣告式 |
|---|---|
| "First read the file, then identify all the public functions..." | "All exported functions: JSDoc required." |
| "Make sure that whenever you write a SQL query..." | "SQL: parameterized queries only. No concatenation." |
| "Please write tests for any new code..." | "New code → tests. Cover happy + error paths." |

宣告式規則也比較容易疊加，不會互相打架。

## 2.1.8 把 Instructions 當成程式碼整理

兩個原則：

**1. Minify。** 把所有 filler 拿掉，像壓縮 production JS 一樣壓縮 instructions。  
**2. 結構化重用。** 不要把同一段規則複製到三個 instruction 檔。

建議做法：

- 共用慣例 → 一份 `applyTo: "**/*"` 的共用檔
- 各層規則 → 用 `applyTo` 做範圍化
- 工作流特定規則 → 做成按需載入的 note 或 prompt file

這樣每次互動載入的 context 更小，也更容易維護。

---

**下一章：** [Language Comparison →](03-language-comparison.zh-TW.md)
