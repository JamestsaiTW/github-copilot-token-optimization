# 2.3 Context Management：控制真正送進去的內容

[English](04-context-management.md) | [繁體中文（台灣）](04-context-management.zh-TW.md)

[← 返回指南](index.zh-TW.md)

---

## 2.3.1 System Instruction 壓縮

`.github/copilot-instructions.md` 會被注入到**每一次 Copilot 互動**。裡面的每個字都會在每次 prompt 中付出 token 成本。

> **補充：相關但不同的慣例。** `.github/copilot-instructions.md` 是 GitHub Copilot 原生的 repo 級 instruction 檔；`AGENTS.md` 則是跨工具慣例，Copilot 也會讀。它們不是同一個檔案，但共同點是：都屬於 **always-on context**。如果內容重複，就等於每次互動重複付費。

這也是最值得優化的檔案之一。假設 instruction 檔有 500 字、約 700 tokens，你每次問問題前就先燒掉 700 tokens。

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
- 刪掉冠詞、填充詞、客套話與保留語氣
- 保留程式碼區塊、inline code、URL、路徑與技術詞
- 保持 Markdown 結構不被破壞

## 2.3.3 策略性檔案組織

Copilot 會自動納入工作區中的內容，例如開啟中的檔案、匯入模組與附近檔案。你可以主動控制。

**真正有效的做法：**

- **關掉目前沒在處理的檔案。** 開啟中的 editor tabs 是最常見的 auto-context 來源。
- **讓檔案保持小而聚焦。** 1,000 行的大檔若開著，Copilot 可能會送很多內容進去。
- **對 build output、vendor、generated files 使用 `.gitignore`。**
- **使用 `applyTo:` 範圍化 instruction 檔**，讓特定規則只在相關檔案出現時才載入。
- **Business／Enterprise 環境下**，可請管理員設定 Content Exclusion 做政策與敏感路徑控管。

要小心的高風險檔案包括：

- 大型 README
- 產生檔與打包輸出
- vendor 目錄
- CSV／JSON fixture 等資料檔
- 歷史存檔文件

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
