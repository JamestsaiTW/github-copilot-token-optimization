# 2.2 自然語言選擇：重新檢查 CJK 假設

[English](03-language-comparison.md) | [繁體中文（台灣）](03-language-comparison.zh-TW.md)

[← 返回指南](index.zh-TW.md)

---

## 2.2.1 人類語言的 Token 經濟學

有一種常見假設：**「中文或日文字數比較少，所以 prompt 應該比較省 token。」**

**實際的 token 計數並不支持這個說法。**

測試句子："I met a huge dog" 及其各語言版本：

| 語言 | 句子 | 字元數 | Tokens | 相對英文 |
|------|------|--------|--------|----------|
| **英文** | I met a huge dog | 16 | **5** | 1.0x |
| **西班牙文** | Conocí a un perro enorme | 24 | **8** | 1.6x |
| **波蘭文** | Spotkałem ogromnego psa | 23 | **8** | 1.6x |
| **冰島文** | Ég hitti risastóran hund | 24 | **10** | 2.0x |
| **中文** | 我遇見了一隻大狗 | 8 | **11** | 2.2x |
| **日文** | 大きな犬に出会った | 9 | **11** | 2.2x |
| **俄文** | Я встретил огромную собаку | 26 | **14** | 2.8x |
| **希伯來文** | פגשתי כלב ענק | 13 | **16** | 3.2x |

中文只有 8 個字，但要 11 個 token；英文 16 個字卻只要 5 個 token。

## 2.2.2 為什麼會這樣

BPE tokenizer 的訓練資料多數以英文為主，因此英文通常有最好的壓縮率：

1. **常見英文詞通常就是 1 個 token**
2. **CJK 字元大約是每字 1–1.4 個 token**，不像常見誤解那樣是 2–3 個，但依然比英文每字元成本高很多
3. **非拉丁字母系統**（如西里爾文、希伯來文、阿拉伯文）通常更吃虧

## 2.2.3 大樣本資料

根據 Capodieci／Castillo 的較大規模研究：

| 語言 | 相對英文平均 Token 成本 | 每個 Token 對應字元數 |
|------|------------------------|-----------------------|
| English | 1.0x | 4.75 |
| Spanish | 約 1.3-1.6x | 約 3.5 |
| German | 約 1.4-1.6x | 約 3.2 |
| Mandarin Chinese | 約 1.76x | 1.33 |
| Japanese | 約 2.12x | 1.41 |
| Korean | 約 2.36x | 約 1.2 |
| Russian | 約 2.5-2.8x | 約 2.0 |

## 2.2.4 文言文呢？

文言文本身資訊密度很高。現代中文可能要 8 個字，文言文可能只要 4 個字，但 tokenizer 不看資訊密度，只看位元組序列。

**例子："Explain database connection pooling"**

| 模式 | 文字 | 約 Tokens |
|------|------|-----------|
| 英文（full caveman） | "Pool reuse open DB conn. Skip handshake → fast." | 約 12 |
| 文言文 full | "池reuse conn。skip handshake → fast。" | 約 15 |
| 文言文 ultra | "池reuse conn。skip→fast。" | 約 12 |

最好的情況是和精簡英文打平，最差則更貴。再加上模型對英文的理解通常更穩，因此：

**結論：** 文言文很有創意，也可能適合教學或示範，但**不建議拿來做真正的 token 最佳化**。

## 2.2.5 實務結論

1. **Prompt 與 instructions 盡量使用英文**
2. **不要把 prompt 翻成 CJK 語言以為會省 token**
3. **如果你用母語能寫得更短，品質可能更好，但 token 成本通常仍較高**
4. **程式輸出通常仍會維持英文**
5. **對非拉丁腳本，轉寫成拉丁字母有時能省 token**

### 轉寫效果

| 腳本 | 句子 | Tokens | 相對原文 |
|------|------|--------|----------|
| 俄文（西里爾） | Я встретил огромную собаку | 14 | baseline |
| 俄文（轉寫） | Ya vstretil ogromnuyu sobaku | 11 | 便宜約 21% |
| 希伯來文 | פגשתי כלב ענק | 16 | baseline |
| 希伯來文（轉寫） | pgSti klv 3nq | 9 | 便宜約 44% |

### 核心發現

> **英文是 LLM prompt 最省 token 的自然語言。**
>
> CJK 雖然字數少，但每個字通常要約 1–1.4 個 token。  
> 綜合下來，同樣意思的內容常常會比英文多出 1.7–2.4 倍的 token。

---

**下一章：** [Context Management →](04-context-management.zh-TW.md)
