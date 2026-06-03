# Folder Structure

這份文件說明 `Adaptive-Campus-Case-Study-main` 裡每個檔案和資料夾的用途。

## 總覽

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
|       +-- case_01_lehigh_university_packer_hall.json
|       +-- case_02_nottingham_trent_university.json
|       +-- case_03_university_of_coimbra.json
|       +-- case_04_national_cheng_kung_university_future_venue.json
|       +-- case_05_feng_chia_university_common_good_hall.json
|       +-- case_06_ntu_humanities_building.json
|       +-- case_07_ntu_liberal_education_classroom_building.json
|       +-- case_08_ncku_industrial_design_history_department.json
|       +-- case_09_scad_hong_kong_campus.json
|       +-- case_10_scad_clark_hall.json
|       +-- case_11_scad_bradley_hall.json
|       +-- case_12_scad_number_nine.json
|       +-- case_13_scad_ruskin_hall.json
|       +-- case_14_university_of_the_arts_london_granary_building.json
|       +-- case_15_university_of_pittsburgh_ford_factory.json
|       +-- case_16_guilford_technical_community_college_advanced_manufacturing_campus.json
|       +-- case_17_tu_delft_bk_city.json
|       +-- case_18_university_of_toronto_daniels_building.json
|       +-- case_19_duke_university_smith_warehouse.json
|       +-- case_20_aalto_university_harald_herlin_learning_centre.json
+-- scripts/
    +-- extract_campus_precedents.py
    +-- README.md
```

## 根目錄檔案

### `README.md`

專案首頁。說明這個資料夾是什麼、最常用哪些檔案、如何重新產生 JSON。

### `GPT_Site_Context_Analysis_Prompt.md`

給 My GPT 使用的 Instructions。

用途：

- 場地脈絡分析
- Knowledge Precedent 分類
- 校園再利用案例檢索
- 將案例策略轉譯成設計建議

使用方式：在 My GPT 的 Instructions 欄位貼上這份內容，並把 `json/campus_knowledge_precedents.json` 上傳為知識檔。

### `campus_cases.xlsx`

原始案例資料表。新增或修改案例時，優先改這個檔案。

目前欄位包含：

- Case
- Original Function
- Current Function
- Key Spatial Features
- Keywords
- Region/Country
- Year
- Location
- Continent
- Floor

### `classifiction structure.txt`

Knowledge Precedent 分類架構的人類可讀版本。

注意：檔名原本拼成 `classifiction`，目前先不改名，避免造成路徑混亂。

### `LICENSE`

授權檔。

## `docs/`

放說明文件。

目前包含：

- `FOLDER_STRUCTURE.md`：你正在看的這份資料夾架構說明。

## `json/`

放已產生的 JSON 知識資料。

### `json/campus_knowledge_precedents.json`

最重要的總資料庫，包含全部 20 筆案例。

內容包含：

- metadata
- taxonomy
- cases

My GPT 如果只能上傳一個知識檔，優先用這個。

### `json/case_overview.json`

20 筆案例的精簡總覽 JSON。

用途：

- 快速瀏覽所有案例
- 依國家、類型、關鍵字建立索引
- 快速查看每案的 taxonomy tags、keywords、spatial vocabulary
- 當完整知識庫太大時，作為輕量上傳檔

### `json/taxonomy.json`

Knowledge Precedent 分類架構的機器可讀版本。

用途：

- 給 GPT 知道分類架構
- 給程式讀取分類層級
- 對照每個案例的 `knowledge_precedent`

### `json/cases/`

每個案例各自一份 JSON。

用途：

- 單獨檢查某個案例
- 分案上傳給 GPT
- 後續人工補資料

如果只想快速使用，不需要逐一打開這個資料夾；直接用總檔 `json/campus_knowledge_precedents.json` 即可。

## `scripts/`

放產生資料的程式。

### `scripts/extract_campus_precedents.py`

從 `campus_cases.xlsx` 讀取案例，產生：

- `json/taxonomy.json`
- `json/campus_knowledge_precedents.json`
- `json/cases/*.json`

執行方式：

```powershell
python scripts\extract_campus_precedents.py
```

## 建議使用順序

1. 先看 `README.md`
2. 要知道整個資料夾怎麼分，看 `docs/FOLDER_STRUCTURE.md`
3. 要給 My GPT，用 `GPT_Site_Context_Analysis_Prompt.md`
4. 要給 My GPT 的知識檔，用 `json/campus_knowledge_precedents.json`
5. 要改案例資料，改 `campus_cases.xlsx`
6. 改完 Excel 後，跑 `scripts/extract_campus_precedents.py`

## 不建議直接改的檔案

通常不要直接手改這些檔案，因為重新跑腳本會覆蓋它們：

- `json/campus_knowledge_precedents.json`
- `json/taxonomy.json`
- `json/cases/*.json`

如果要長期保留人工修正，應該先改 `campus_cases.xlsx` 或修改 `scripts/extract_campus_precedents.py` 的萃取邏輯。
