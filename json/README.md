# JSON Output

這個資料夾放由 `scripts/extract_campus_precedents.py` 產生的案例知識資料。

## 檔案說明

| 檔案 / 資料夾 | 用途 |
|---|---|
| `campus_knowledge_precedents.json` | 所有案例的完整知識庫，可上傳給 My GPT |
| `case_overview.json` | 所有案例的精簡總覽，適合快速瀏覽、索引、輕量上傳 |
| `taxonomy.json` | Knowledge Precedent 五層分類架構 |
| `cases/` | 每個案例各自一份 JSON |

## 使用建議

給 My GPT 使用，優先上傳：

```text
json/campus_knowledge_precedents.json
```

如果 My GPT 只需要快速掌握案例清單、分類標籤、關鍵字和索引，建議上傳：

```text
json/case_overview.json
```

看特定案例：

```text
json/cases/
```

## `case_overview.json`

每筆資料包含以下包含：

- case number
- case id
- case name
- original function
- current function
- region / country
- year
- location
- key spatial features
- keywords
- typology tags
- five-layer taxonomy tags
- spatial vocabulary
- semantic relations

- `by_region_country`
- `by_typology`
- `by_keyword`

## 注意

這裡的 JSON 是自動產生的。重新執行下面指令後，這個資料夾裡的 JSON 會被更新：

```powershell
python scripts\extract_campus_precedents.py
```

如果要修改案例內容，建議先改根目錄的 `campus_cases.xlsx`，再重新產生 JSON。
