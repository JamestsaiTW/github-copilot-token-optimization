# 2.3 Context Management：控制真正送進去的內容

[English](04-context-management.md) | [繁體中文（台灣）](04-context-management.zh-TW.md)

[← 返回指南](index.zh-TW.md)

---

## 2.3.1 System Instruction 壓縮

`.github/copilot-instructions.md` 會被注入到**每一次 Copilot 互動**。裡面的每個字都會在每次 prompt 中付出 token 成本。

> **補充：相關但不同的慣例。** `.github/copilot-instructions.md` 是 GitHub Copilot 原生的 repo 級 instruction 檔；`AGENTS.md` 則是跨工具慣例，Copilot 也會讀。它們不是同一個檔案，但共同點是：都屬於 **always-on context**。如果內容重複，就等於每次互動重複付費。

這也是最值得最佳化的檔案之一。假設 instruction 檔有 500 字、約 700 tokens，你每次問問題前就先燒掉 700 tokens。

**壓縮前：**

```text
You should write terse responses like a caveman. Make sure all technical substance
remains exact. Only remove unnecessary filler words. Drop articles and hedging.
Use fragments when appropriate. Keep code unchanged. Use short synonyms where possible.
```

**壓縮後：**

```text
Terse like caveman. Technical substance exact. Only fluff die.
Drop: articles, filler (just/really/basically), pleasantries, hedging.
Fragments OK. Short synonyms. Code unchanged.
```

這類調整常能節省超過一半，而且每次互動都會複利生效。

## 2.3.2 記憶檔壓縮

除了 `copilot-instructions.md`／`AGENTS.md`，很多專案還會累積 `CLAUDE.md`、project notes、coding guidelines、`.cursorrules` 等記憶檔。如果它們會進 context，就要一併計入成本。

**原則：**

- 先合併重複內容，再做壓縮
- 刪掉冠詞、填充詞、模糊保留與客套話
- 保留程式碼區塊、inline code、URL、路徑與技術詞
- 保持 Markdown 結構不被破壞

## 2.3.3 策略性檔案組織

Copilot 會自動納入工作區中的內容，例如開啟中的檔案、匯入模組與附近檔案。你可以主動控制。

**真正有效的做法：**

- **關掉目前沒在處理的檔案。** 開啟中的 editor tabs 是最常見的 auto-context 來源。
- **讓檔案保持小而聚焦。** 1,000 行的大檔若開著，Copilot 可能會送很多內容進去。
- **對 build output、vendor、generated files 使用 `.gitignore`。**
- **使用 `applyTo:` 範圍化 instruction 檔**，讓特定規則只在相關檔案出現時才載入。
- **在 AI 工作前，先把非純文字檔轉成 Markdown。** 這是處理富格式輸入時，最直接的 token 節省。
- **Business／Enterprise 環境下**，可請管理員設定 Content Exclusion 做政策與敏感路徑控管，詳見 [GitHub Docs — 從 Copilot 排除內容](https://docs.github.com/en/copilot/how-tos/configure-content-exclusion/exclude-content-from-copilot)。它只在 Copilot Business 與 Enterprise 提供，且不適用於 Copilot CLI、cloud agent 或 IDE Chat 的 Agent Mode；請把它當成隱私／政策控制，而非每位開發者的省 token 旋鈕。

要小心的高風險檔案包括：

- 大型 README
- 產生檔與打包輸出
- vendor 目錄
- CSV／JSON fixture 等資料檔
- 歷史存檔文件
- 富格式文件（`.docx`、`.pdf`、`.pptx`、`.xlsx`、HTML 匯出、掃描圖片、音訊／影片逐字稿）

### 先把非純文字輸入轉成 Markdown

當來源是 Word、PDF、PowerPoint、試算表、圖片、音訊檔，或匯出的 HTML 時，只要流程允許，就不要直接把富格式內容丟進 AI。先轉成乾淨的 Markdown，再把 Markdown 送進去。

[Marc Bara 的文章](https://medium.com/@marc.bara.iniesta/your-docx-is-wasting-33-of-your-ai-budget-86a3d229d042) 把這件事稱為**格式稅**：Word、PDF 與 HTML 會夾帶字型資料、XML、頁面定位中繼資料、版面殘渣、內嵌物件與 tag soup。模型得處理這些內容，卻通常不需要它們。文中舉的例子是：同一份 10 頁報告，從 PDF 抽取後大約用了 12,400 tokens；轉成乾淨 Markdown 後約 8,350 tokens，資訊相同，輸入卻少了約 33%。HTML 匯出往往更糟，因為語意內容外面還包著一長串 tags、classes、IDs 與版面骨架。

實務規則很簡單：Markdown 才是 AI 互動時的**工作格式**；Word／PDF／PowerPoint 則是最後交付給人看的格式。草稿、審閱、摘要、切 chunk、RAG 擷取，都先用 Markdown。只有在客戶、法規或內部流程真的需要時，最後才輸出 `.docx` 或 `.pdf`。

[Microsoft MarkItDown](https://github.com/microsoft/markitdown) 是最實用的橋接工具。它是把各種檔案與 Office 文件轉成 Markdown 的 Python 工具，專門給 LLM 與文字分析流程使用。它會保留標題、清單、表格、連結與實用中繼資料，同時避開高保真的視覺版面雜訊。目前支援 PDF、Word、PowerPoint、Excel、具 EXIF／OCR 的圖片、可轉錄的音訊、HTML、CSV／JSON／XML、ZIP 內容、YouTube URL、EPUB 等。

快速路徑：

```bash
pip install 'markitdown[all]'
markitdown report.docx -o report.md
markitdown deck.pptx -o deck.md
markitdown source.pdf > source.md
```

如果是正式流程，且你知道自己只會碰哪些格式，盡量安裝較小的 extras：

```bash
pip install 'markitdown[pdf,docx,pptx,xlsx]'
```

安全提醒：MarkItDown 會以目前程序的權限讀取檔案、串流與 URL。面對不受信任的輸入時，先驗證路徑與 URL，再使用最小化的轉換能力。

## 2.3.4 有意識地縮小 Context：條件式優於常駐式

多數 context 檔都會在**每次互動**載入，即使和目前問題無關也是如此。

解法是：**優先使用條件式 context，而不是 always-on context。**

### 用 `applyTo:` 路徑範圍化 custom instructions

`.github/instructions/*.instructions.md` 支援 `applyTo` frontmatter。Copilot 只會在對話涉及符合 glob 的檔案時載入它。

```markdown
---
applyTo: "src/api/**/*.ts"
---
API conventions:
- Routes in src/api/routes/. Handlers thin, logic in services/.
- Validate with zod. Errors via Result<T,E>, never throw.
- All endpoints return { data, error } envelope.
```

不加 `applyTo`，這段內容會在每次 Copilot 呼叫都出現。加上之後，只有真的在處理 API 檔案時才會付費。

### 工作流指引也要按需載入

像 PR review checklist、release template、debugging playbook 這種不是每次都用的內容，不應該永遠放在 `copilot-instructions.md`。

規則可以分三類：

- **Always-on：** 每次都真的適用的少數規則
- **Conditional（`applyTo`）：** 依路徑範圍出現的規則
- **On-demand：** 工作流特定內容，只在需要時載入

## 2.3.5 善用快取

最便宜的 token，是平台不用重新處理的 token。穩定的 context 前綴，通常能獲得較好的快取效果。

兩個實用模式：

1. **穩定內容放前面，變動內容放後面。**
2. **重複使用已命名的共用 context。**

快取同時帶來兩個好處：

- **更快**
- **更便宜**

## 2.3.6 適時開新對話

對話歷史會持續累積。20+ 則訊息後，每次新訊息可能都帶著 50K+ tokens 的歷史一起送出。

**適合開新對話的時機：**

- 題目切換
- 已經拿到你需要的答案
- 回應開始變慢
- 模型明顯被舊 context 干擾

**怎麼保留延續性：** 在新對話用一小段摘要承接即可。

---

**下一章：** [Output Control →](05-output-control.zh-TW.md)
