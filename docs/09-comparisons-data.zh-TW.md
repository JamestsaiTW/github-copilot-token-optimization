```markdown
# Part 3：比較與資料

[English](09-comparisons-data.md) | [繁體中文（台灣）](09-comparisons-data.zh-TW.md)

[← 返回指南](index.md)

---

## 3.1 正面對決：同一個 Prompt，不同技巧

**任務：** "Add error handling to this function"

| 技巧 | Prompt | 約略輸入 Tokens | 輸出品質 |
|------|--------|-----------------|----------|
| 冗長英文 | "Hey, could you please add comprehensive error handling to this function? I'd like it to handle all edge cases including null inputs, invalid types, and network errors. Please explain your changes." | 約 40 | 好，但偏冗長 |
| Caveman lite | "Add error handling to this function. Cover null inputs, invalid types, network errors." | 約 16 | 好 |
| Caveman full | "Add error handling. Cover: null input, bad type, network error." | 約 12 | 好 |
| Caveman ultra | "Error handling: null/bad-type/net-err." | 約 7 | 好（可能需要上下文） |
| 結構化 | `fn: add error handling\n- null input\n- invalid type\n- network error` | 約 12 | 好 |
| Code-centric | `# TODO: handle None, TypeError, ConnectionError` | 約 8 | 好 |

這六種寫法都能得到正確方向的程式碼，但成本從 7 到 40 tokens，差了 **5.7 倍**。

## 3.2 語言比較表

### 單句比較

來源：Ivan Krivyakov 使用 HuggingFace tokenizer playground（GPT-4 設定）分析。

| 語言 | 句子 | 字元數 | UTF-8 Bytes | Tokens | 相對英文成本 |
|------|------|--------|-------------|--------|--------------|
| 🇬🇧 English | I met a huge dog | 16 | 16 | **5** | 1.0x |
| 🇪🇸 Spanish | Conocí a un perro enorme | 24 | 25 | **8** | 1.6x |
| 🇵🇱 Polish | Spotkałem ogromnego psa | 23 | 24 | **8** | 1.6x |
| 🇮🇸 Icelandic | Ég hitti risastóran hund | 24 | 26 | **10** | 2.0x |
| 🇨🇳 Chinese | 我遇见了一只大狗 | 8 | 24 | **11** | 2.2x |
| 🇯🇵 Japanese | 大きな犬に出会った | 9 | 27 | **11** | 2.2x |
| 🇷🇺 Russian | Я встретил огромную собаку | 26 | 49 | **14** | 2.8x |
| 🇮🇱 Hebrew | פגשתי כלב ענק | 13 | 24 | **16** | 3.2x |

### 大樣本平均

來源：Capodieci/Castillo 針對較大文字樣本的研究。

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

本指南涵蓋的所有技巧完整比較：

| # | 技巧 | 輸入節省 | 輸出節省 | 品質影響 | 努力 | 最適用情境 |
|---|------|:--------:|:--------:|:--------:|:----:|------------|
| **溝通風格** |
| A1 | Caveman-speak（完整） | 30-50% | 40-55%† | 極低 | 低 | 所有 Copilot 互動 |
| A2 | 強度等級（lite→ultra） | 15-70% | 15-55%† | 視等級而異 | 低 | 調整壓縮 |
| A3 | 文言文模式 | ❌ 負面 | ❌ 負面 | 降低品質 | 低 | 僅示範用 |
| A4 | 結構化模式 | 20-40% | 30-50% | 改善 | 低 | 技術性 prompt |
| **Prompt 工程** |
| B1 | 精準 prompt | 30-60% | 30-60% | 改善 | 低 | 所有互動 |
| B2 | 要求差異，不要重寫 | — | 50-90% | 中性以上 | 低 | 程式碼修改 |
| B3 | 一次一任務 | 20-40% | 20-40% | 改善 | 低 | 複雜請求 |
| B4 | 限制輸出格式 | — | 40-80% | 視情況 | 低 | 資料抽取 |
| B5 | 系統指令要求簡潔 | — | 30-60% | 良好 | 中 | 所有互動 |
| B6 | 少量示範 vs 零示範 | +20-50% | -30-60% 浪費 | 改善 | 中 | 新模式 |
| B7 | 針對模型調整 prompt | 間接 | 間接 | 改善 | 低 | 模型升級、應用提示 |
| **上下文管理** |
| C1 | 限制上下文（檔案選擇） | 50-90% | — | 視情況 | 中 | 大型程式碼庫 |
| C2 | 壓縮指令檔 | 40-60% 檔案大小 | — | 無 | 低 | 每個 repo |
| C3 | 漸進式按需指導 | 60-90% 選用指導 | — | 正面 | 高 | 可重用提示檔案團隊 |
| C4 | 開新對話 | 80% 以上 | — | 失去上下文 | 低 | 長時間會話 |
| C5 | 先轉非文字檔為 Markdown | PDF 範例約 33%；雜訊 HTML 通常更高 | — | 改善結構 | 低 | DOCX、PDF、PPTX、XLSX、圖片、音訊、RAG 匯入 |
| **輸出控制** |
| D1 | 僅程式碼回應 | — | 40-70% | 良好 | 低 | 程式碼產生 |
| D2 | 結構化輸出（JSON/表格） | — | 30-60% | 視情況 | 低 | 資料任務 |
| D3 | 限制回應長度 | — | 變動 | 有截斷風險 | 低 | 快速回答 |
| **Agent 專用** |
| E1 | `copilot-setup-steps.yml` | 10-30% | — | 改善 | 中 | 程式碼 Agent |
| E2 | 精確問題描述 | 20-50% | — | 改善 | 低 | 程式碼 Agent |
| E3 | 自訂 Agent 設定檔 | 10-30% | — | 改善 | 中 | 程式碼 Agent |
| E4 | 計畫檔案 | 15-40% | — | 視情況 | 中 | 複雜 Agent 任務 |
| **記憶/狀態** |
| F1 | 壓縮記憶檔案 | 每次載入 40-60% | — | 無 | 低 | 持續上下文 |
| F2 | 簡短提交訊息 | 約 5-15 tokens | — | 無 | 低 | Agent 讀 git |
| F3 | 簡短審查意見 | — | 60-80% | 無 | 低 | PR 工作流程 |
| **模型選擇** |
| G1 | 低成本模型處理簡單任務 | 不適用 | 不適用 | 視情況 | 低 | 簡單任務 |
| G2 | 自動模型選擇 | 不適用 | 不適用 | 良好 | 無 | 預設選擇 |
| G3 | 草稿用便宜模型，潤飾用高階模型 | 不適用 | 不適用 | 良好 | 低 | 反覆工作 |
| G4 | 按任務類型混合模型 | 38-79% 請求數 | — | 無（SWE-bench 資料） | 低 | 所有工作流程 |
| G5 | 推理努力 / 思考努力 | 廠商報告節省 | — | 廠商推薦，無基準 | 低 | Copilot、CLI、API 支援推理模型 |
| **工作階段管理** |
| H1 | Ask 模式處理簡單問題 | 60-90% | — | 良好 | 低 | 簡單問題 |
| **上下文檔案管理**（涵蓋 `copilot-instructions.md`、`AGENTS.md`、`CLAUDE.md` — 永遠開啟的上下文） |
| I1 | 修剪永遠開啟上下文，只留地雷 | 依檔案大小變動 | — | 改善 | 低 | 所有 Agent 工作流程 |
| I2 | 刪除 LLM 產生的上下文檔案 | 總計 20-23% | — | 改善 | 低 | 有 /init 輸出專案 |
| I3 | Bug-tracker 方式管理上下文 | 變動 | — | 改善 | 低 | 活躍專案 |
| I4 | 合併重複上下文檔案（一份，不是兩份） | 重複成本 | — | 中性 | 低 | 同時有 AGENTS.md + copilot-instructions.md 的 repo |
| **MCP 與工具管理** |
| J1 | 稽核 MCP 伺服器（停用未用） | 5K-190K/tokens | — | 無 | 低 | Agent 模式用戶 |
| J2 | 依工作區設定 MCP | 變動 | — | 無 | 中 | 多專案設定 |
| J3 | 最小化工具呼叫（指令） | 10-30% | — | 中性 | 低 | Agent 模式 |
| J4 | 用 [RTK](https://github.com/rtk-ai/rtk) 壓縮工具輸出 | 60-90% shell 指令輸出 | — | 無 | 低 | Agent / 程式碼 Agent — 任意 AI 工具 |
| **Agent 模式設定** |
| K1 | 精準 prompt + 接受標準 | 30-60% | — | 改善 | 低 | Agent 任務 |
| K2 | 複雜任務用計畫檔 | 15-40% | — | 改善 | 中 | 多步驟 Agent 任務 |
| K3 | 限制 Agent 最大請求數 | 變動 | — | 有截斷風險 | 低 | 所有 Agent 任務 |
| K4 | 模式選擇（Ask/Edit/Agent） | 60-90% | — | 良好 | 低 | 所有互動 |

> †A1/A2 輸出節省需搭配系統層級的簡潔輸出指令（見 B5）。僅寫簡潔 prompt 只能節省輸入 tokens，輸出 tokens 只有在模型被指示簡潔回應時才會減少。

> C5 來源：Marc Bara 的 [Your .docx Is Wasting 33% of Your AI Budget](https://medium.com/@marc.bara.iniesta/your-docx-is-wasting-33-of-your-ai-budget-86a3d229d042)。當非純文字檔需要進入 AI 工作流程時，優先使用 [Microsoft MarkItDown](https://github.com/microsoft/markitdown)。

### 大贏家

如果只能做這幾件事，請優先做這八項。依影響力與努力比排序：

1. **Caveman-speak** — 30-50% 輸入 token 節省；搭配 B5 可達 40-55% 輸出節省
2. **精準 prompt** — 30-60% 節省，只要改習慣
3. **僅程式碼 / 限制輸出** — 40-80% 輸出節省，一句指令搞定
4. **縮小永遠開啟上下文**（`copilot-instructions.md` + `AGENTS.md`）— 壓縮 filler，修剪只留地雷，刪除 LLM 產生的樣板。每次互動與 Agent 步驟都疊加；節省 20-23% Agent 任務，且正確率更高
5. **簡單問題用 Ask Mode** — 避免 Agent 開銷，節省 60-90%
6. **稽核 MCP 伺服器** — 停用未用伺服器，每個 Agent 任務節省 5K-190K tokens
7. **先把非純文字檔轉成 Markdown** — 避免 DOCX/PDF/HTML 格式稅，讓內容進入聊天、Agent 或 RAG 前更乾淨
8. **依模型調整 prompt** — 非每次請求都壓縮；提升首輪品質，避免模型變更後重工

## 3.4 品質影響評估

壓縮會不會傷害輸出品質？研究顯示：**很少，且只有在極端壓縮時才會。**

| 壓縮程度 | 品質影響 | 證據 |
|----------|----------|------|
| Lite（刪 filler） | 無 | 模型訓練於多元文本，理解乾淨文句 |
| Full（刪冠詞、片段） | 可忽略 | 模型能處理片段，技術詞彙保留 |
| Ultra（縮寫、箭頭） | 小風險 | 複雜多步指令可能誤解 |
| 文言文 | 中度風險 | 模型理解文言不如英文穩定 |
| 極端（只留單字） | 高風險 | 歧義增加，模型可能誤判 |

**門檻：** 當你發現自己要重複解釋或結果錯誤，就是壓縮過頭了。退回一個層級。

**模型特定備註：** 主要模型（GPT-4、Claude、Gemini）都能良好處理 caveman-full。Ultra 適合熟悉領域的使用者。文言文不適合程式碼產生任務。

### 效益遞減

節省曲線非線性。前 30% 壓縮（刪 filler）是免費的。接下來 20%（片段、縮寫）幾乎免費。超過後，每多壓一點，品質風險增加。

<div class="guide-visual" role="img" aria-label="壓縮節省與品質風險的關係圖">
  <p class="guide-visual__title">效益與風險曲線</p>
  <div class="guide-visual__curve">
    <div class="guide-visual__curve-row">
      <span class="guide-visual__curve-label">品質</span>
      <div class="guide-visual__curve-bar">
        <div class="guide-visual__curve-fill" style="width: 82%;"></div>
      </div>
    </div>
    <div class="guide-visual__curve-row">
      <span class="guide-visual__curve-label">風險</span>
      <div class="guide-visual__curve-bar">
        <div class="guide-visual__curve-fill guide-visual__curve-fill--risk" style="width: 62%;"></div>
      </div>
    </div>
  </div>
  <div class="guide-visual__scale">
    <span>0%</span>
    <span>20%</span>
    <span>40%</span>
    <span>60%</span>
    <span>80%</span>
  </div>
  <div class="guide-visual__ticks">
    <span>lite</span>
    <span>full</span>
    <span>ultra</span>
    <span>extreme</span>
  </div>
</div>

**建議甜蜜點：** Full caveman（30-50% 輸入 token 節省；搭配簡潔系統指令可達 40-55% 輸出節省）。最大效益，風險極低。

---

**下一章：** [Practical Setup →](10-practical-setup.zh-TW.md)
```
