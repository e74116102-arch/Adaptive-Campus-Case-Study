# Adaptive Campus Case Study

把 `campus_cases.xlsx` 裡的校園案例，轉成可以給 My GPT / AI Co-Designer 使用的 JSON 知識資料。
自適應校園案例GPT:https://chatgpt.com/g/g-6a1fa01a625481918792d2bdba37cbf1-adaptive-campus-case-study

## 常用的檔案

| 檔案 | 用途 |
|---|---|
| `GPT_Site_Context_Analysis_Prompt.md` | 貼到 My GPT Instructions 的 prompt |
| `json/campus_knowledge_precedents.json` | 20 筆案例的完整 JSON 知識庫 |
| `json/case_overview.json` | 20 筆案例的精簡總覽 JSON |
| `json/taxonomy.json` | Knowledge Precedent 分類架構 |
| `json/cases/*.json` | 每個案例各自一份 JSON |
| `campus_cases.xlsx` | 原始案例 Excel |
| `scripts/extract_campus_precedents.py` | 從 Excel 重新產生 JSON 的腳本 |
| `docs/FOLDER_STRUCTURE.md` | 完整資料夾架構說明 |

## 資料夾架構

```text
Adaptive-Campus-Case-Study-main/
+-- README.md
+-- GPT_Site_Context_Analysis_Prompt.md
+-- campus_cases.xlsx
+-- classifiction structure.txt
+-- LICENSE
+-- docs/
|   +-- FOLDER_STRUCTURE.md
+-- json/
|   +-- campus_knowledge_precedents.json
|   +-- case_overview.json
|   +-- taxonomy.json
|   +-- README.md
|   +-- cases/
|       +-- case_01_*.json
|       +-- ...
|       +-- case_20_*.json
+-- scripts/
    +-- extract_campus_precedents.py
    +-- README.md
```

## 工作流程

1. 在 `campus_cases.xlsx` 補或改案例資料。
2. 執行腳本重新產生 JSON：

```powershell
python scripts\extract_campus_precedents.py
```

3. 使用 `json/campus_knowledge_precedents.json` 作為 My GPT 的完整知識檔。
4. 使用 `GPT_Site_Context_Analysis_Prompt.md` 作為 My GPT 的 Instructions。

## JSON 內容

每個案例都有兩個主要部分：

- `knowledge_precedent`：依五層分類架構標記案例特徵。
- `precedent_dna`： Precedent DNA 邏輯整理案例。

五層分類架構：

1. Architectural Layer（建築層）
2. Urban Context Layer（都市脈絡層）
3. Temporal Transformation Layer（時間轉化層）
4. Functional Layer（機能層）
5. Typology Layer（類型層）
