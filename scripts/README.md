# Scripts

這個資料夾放資料產生腳本。

## `extract_campus_precedents.py`

用途：從根目錄的 `campus_cases.xlsx` 萃取案例，產生 JSON 知識庫。

會產生：

- `json/taxonomy.json`
- `json/campus_knowledge_precedents.json`
- `json/case_overview.json`
- `json/cases/*.json`

## 執行方式

請在專案根目錄執行：

```powershell
python scripts\extract_campus_precedents.py
```

## 建議執行

- 新增案例到 `campus_cases.xlsx`
- 修改案例欄位
- 修改分類邏輯
- JSON 被刪除或需要重新整理

## 注意

腳本會覆寫 `json/` 裡自動產生的 JSON 檔案。
