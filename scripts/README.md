# Scripts

## `extract_campus_precedents.py`

This script reads `campus_cases.xlsx` and regenerates the project JSON dataset.

Generated outputs:

- `json/taxonomy.json`
- `json/campus_knowledge_precedents.json`
- `json/case_overview.json`
- `json/cases/*.json`
- `campus_knowledge_precedents_MyGPT_upload.json`

The generated taxonomy uses six layers:

1. `architectural_layer`
2. `urban_context_layer`
3. `temporal_transformation_layer`
4. `functional_layer`
5. `typology_layer`
6. `adaptive_transformation_layer`

Layer 6 includes:

- `adaptation_model`
- `behavior`
- `organizational_driver`
- `transformation_driver`

Each case also includes:

- `case_images`
- `adaptive_transformation_analysis`
- `knowledge_precedent`
- `precedent_dna`

## Run

From the repository root:

```powershell
python scripts\extract_campus_precedents.py
```

The script overwrites generated JSON files. Edit `campus_cases.xlsx` or the extraction rules in `extract_campus_precedents.py`, then rerun the script.
