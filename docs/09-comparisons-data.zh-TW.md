# Part 3：比較與資料

[English](09-comparisons-data.md) | [繁體中文（台灣）](09-comparisons-data.zh-TW.md)

[← 返回指南](index.md)

---

## 3.1 正面對決：同一個 Prompt，不同技巧

**任務：** "Add error handling to this function"

| 技巧 | Prompt | 約略輸入 Tokens | 輸出品質 |
|------|--------|-----------------|----------|
| 冗長英文 | "Hey, could you please add comprehensive error handling..." | 約 40 | 好，但偏冗長 |
| Caveman lite | "Add error handling to this function. Cover null inputs..." | 約 16 | 好 |
| Caveman full | "Add error handling. Cover: null input, bad type..." | 約 12 | 好 |
| Caveman ultra | "Error handling: null/bad-type/net-err." | 約 7 | 好，但更依賴上下文 |
| 結構化 | `fn: add error handling\n- null input\n- invalid type\n- network error` | 約 12 | 好 |
| Code-centric | `# TODO: handle None, TypeError, ConnectionError` | 約 8 | 好 |

這六種寫法都能得到正確方向的程式碼，但成本從 7 到 40 tokens，差了 **5.7 倍**。

## 3.2 語言比較表

### 單句比較

| 語言 | 句子 | 字元數 | UTF-8 Bytes | Tokens | 相對英文成本 |
|------|------|--------|-------------|--------|--------------|
| 英文 | I met a huge dog | 16 | 16 | **5** | 1.0x |
| 西班牙文 | Conocí a un perro enorme | 24 | 25 | **8** | 1.6x |
| 波蘭文 | Spotkałem ogromnego psa | 23 | 24 | **8** | 1.6x |
| 冰島文 | Ég hitti risastóran hund | 24 | 26 | **10** | 2.0x |
| 中文 | 我遇見了一隻大狗 | 8 | 24 | **11** | 2.2x |
| 日文 | 大きな犬に出会った | 9 | 27 | **11** | 2.2x |
| 俄文 | Я встретил огромную собаку | 26 | 49 | **14** | 2.8x |
| 希伯來文 | פגשתי כלב ענק | 13 | 24 | **16** | 3.2x |

### 大樣本平均

| 語言 | 相對英文平均 Token 成本 | 每個 Token 對應字元數 | 判斷 |
|------|------------------------|-----------------------|------|
| English | 1.0x | 4.75 | ✅ 最適合 prompt |
| Spanish | 約 1.3-1.6x | 約 3.5 | ⚠️ 30-60% 更貴 |
| German | 約 1.4-1.6x | 約 3.2 | ⚠️ 40-60% 更貴 |
| Mandarin Chinese | 約 1.76x | 1.33 | ❌ 約 76% 更貴 |
| Japanese | 約 2.12x | 1.41 | ❌ 約 112% 更貴 |
| Korean | 約 2.36x | 約 1.2 | ❌ 約 136% 更貴 |
| Russian | 約 2.5-2.8x | 約 2.0 | ❌ 約 150-180% 更貴 |

## 3.3 技巧總表

以下是本指南涵蓋技巧的高層比較：

| 類別 | 技巧 | 輸入節省 | 輸出節省 | 品質影響 | 最適用情境 |
|------|------|----------|----------|----------|------------|
| Communication | Caveman-speak | 30-50% | 40-55%* | 極低 | 所有 Copilot 互動 |
| Communication | Structured prompts | 20-40% | 30-50% | 多半更好 | 技術性 prompt |
| Prompting | Precise prompts | 30-60% | 30-60% | 多半更好 | 所有互動 |
| Prompting | Constrain output | — | 40-80% | 視格式而定 | 資料抽取、快速回答 |
| Context | Limit context | 50-90% | — | 視情況 | 大型 codebase |
| Context | Compressed instructions | 40-60% of file | — | 幾乎無 | 每個 repo |
| Context | 先把非純文字檔轉成 Markdown | 引用 PDF 範例約 33%；雜訊 HTML 通常更高 | — | 結構更清楚 | DOCX、PDF、PPTX、XLSX、圖片、音訊、RAG 匯入 |
| Output | Code-only responses | — | 40-70% | 好 | 程式產生 |
| Agent | Ask vs Agent mode | 60-90% | — | 好 | 簡單問題 |
| Always-on files | 只留 landmines | 視檔案大小 | — | 多半更好 | 所有 agent 工作流 |
| MCP | Audit servers | 5K-190K/task | — | 無 | Agent mode |

\*輸出節省要搭配 system-level 的精簡輸出設定。

### 影響最大的一批

1. **Caveman-speak**
2. **Precise prompts**
3. **Code-only / constrain output**
4. **縮小 always-on context**
5. **簡單問題用 Ask Mode**
6. **先把非純文字檔轉成 Markdown**
7. **稽核 MCP servers**
8. **依模型調整 prompts**

> C5 來源：Marc Bara 的 [Your .docx Is Wasting 33% of Your AI Budget](https://medium.com/@marc.bara.iniesta/your-docx-is-wasting-33-of-your-ai-budget-86a3d229d042)。當非純文字檔需要進入 AI 工作流時，優先使用 [Microsoft MarkItDown](https://github.com/microsoft/markitdown)。

## 3.4 品質影響評估

壓縮會不會傷害品質？答案通常是：**很少，除非你壓過頭。**

| 壓縮程度 | 品質影響 | 判斷 |
|----------|----------|------|
| Lite | 幾乎無 | 安全 |
| Full | 可忽略 | 最甜蜜點 |
| Ultra | 有小風險 | 複雜指令時要小心 |
| 文言文 | 中度風險 | 不建議用於實務 |
| 極端壓縮 | 高風險 | 易產生歧義 |

### 效益遞減

最前面那 30% 的壓縮幾乎是白撿的：刪掉 filler 就好。  
再往後 20% 也通常很划算。  
超過那個點後，每多壓一點，都更可能帶來誤解。

**建議甜蜜點：** Full caveman。

---

**下一章：** [Practical Setup →](10-practical-setup.zh-TW.md)
