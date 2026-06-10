# Adaptive Campus Case Study

This repository contains a structured adaptive campus precedent dataset for My GPT / AI Co-Designer workflows.

The current dataset includes 20 campus adaptive reuse or campus renewal cases. Each case has image references, a six-layer Knowledge Precedent classification, Precedent DNA fields, and an adaptive transformation analysis.

## Main Files

| File | Purpose |
|---|---|
| `campus_knowledge_precedents_MyGPT_upload.json` | Recommended single upload file for My GPT. Contains all 20 complete cases. |
| `GPT_Site_Context_Analysis_Prompt.md` | Custom GPT Instructions prompt using the six-layer taxonomy. |
| `json/campus_knowledge_precedents.json` | Full database with taxonomy and all 20 complete case records. |
| `json/case_overview.json` | Compact overview for browsing, filtering, and quick retrieval. |
| `json/taxonomy.json` | Six-layer Knowledge Precedent taxonomy. |
| `json/cases/*.json` | One complete JSON file per case. |
| `classifiction structure.txt` | Human-readable six-layer taxonomy outline. Filename is intentionally kept as originally spelled. |
| `campus_cases.xlsx` | Source spreadsheet. |
| `scripts/extract_campus_precedents.py` | Extraction script that regenerates all JSON outputs. |
| `docs/FOLDER_STRUCTURE.md` | Folder and file guide. |

## Folder Structure

```text
Adaptive-Campus-Case-Study/
+-- README.md
+-- GPT_Site_Context_Analysis_Prompt.md
+-- campus_cases.xlsx
+-- campus_knowledge_precedents_MyGPT_upload.json
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

## Six-Layer Taxonomy

1. `architectural_layer`
2. `urban_context_layer`
3. `temporal_transformation_layer`
4. `functional_layer`
5. `typology_layer`
6. `adaptive_transformation_layer`

The sixth layer contains:

- `adaptation_model`
  - `what_changed`
  - `why_changed`
  - `what_remained`
  - `how_space_adapted`
  - `evidence`
- `behavior`
  - `informal_learning`
  - `group_discussion`
  - `knowledge_sharing`
  - `social_interaction`
- `organizational_driver`
  - `cross_disciplinary_curriculum`
  - `project_based_learning`
  - `shared_facility_management`
  - `community_engagement`
- `transformation_driver`
  - `pedagogical_change`
  - `technology_change`
  - `enrollment_growth`
  - `financial_pressure`
  - `community_outreach`

## Case JSON Fields

Each complete case includes:

- `id`
- `case_name`
- `source`
- `raw_fields`
- `case_images`
- `adaptive_transformation_analysis`
- `knowledge_precedent`
- `precedent_dna`
- `notes`

## My GPT Usage

For My GPT knowledge upload, use:

```text
campus_knowledge_precedents_MyGPT_upload.json
```

For My GPT Instructions, use:

```text
GPT_Site_Context_Analysis_Prompt.md
```

## Regenerate JSON

Run this from the repository root:

```powershell
python scripts\extract_campus_precedents.py
```

The script regenerates:

- `json/taxonomy.json`
- `json/campus_knowledge_precedents.json`
- `json/case_overview.json`
- `json/cases/*.json`
- `campus_knowledge_precedents_MyGPT_upload.json`

## Notes

- Image data is stored as remote reference URLs and source page URLs. Verify source permissions before redistribution.
- Empty spreadsheet values are kept as `null`.
- `classifiction structure.txt` keeps the original misspelled filename to avoid breaking existing references.
