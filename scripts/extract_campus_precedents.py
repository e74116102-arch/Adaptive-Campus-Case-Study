from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SOURCE_XLSX = ROOT / "campus_cases.xlsx"
OUTPUT_DIR = ROOT / "json"
CASES_DIR = OUTPUT_DIR / "cases"

NS = {
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


CASE_IMAGE_REFERENCES: dict[str, list[dict[str, str]]] = {
    "case_01_lehigh_university_packer_hall": [
        {
            "label": "Primary case image",
            "url": "https://thebrownandwhite.com/wp-content/uploads/2018/09/University-Center-1.jpg",
            "source_url": "https://thebrownandwhite.com/2018/09/16/uc-renovations-lehigh-packer-hall-path-to-prominence-university-center/",
            "source_name": "The Brown and White",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_02_nottingham_trent_university": [
        {
            "label": "Primary case image",
            "url": "https://architizer-prod.imgix.net/mediadata/projects/442011/de7a34bd.jpg?w=1680&q=60&auto=format,compress&cs=strip",
            "source_url": "https://architizer.com/projects/newton-arkwright-buildings-nottingham-trent-university/",
            "source_name": "Architizer",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_03_university_of_coimbra": [
        {
            "label": "Primary case image",
            "url": "https://whc.unesco.org/uploads/thumbs/site_1387_0001-1200-630-20130603143340.jpg",
            "source_url": "https://whc.unesco.org/en/list/1387/",
            "source_name": "UNESCO World Heritage Centre",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_04_national_cheng_kung_university_future_venue": [
        {
            "label": "Primary case image",
            "url": "https://web.ncku.edu.tw/var/file/0/1000/pictures/416/m/mczh-tw1920x800_small200439_664259522433.jpg",
            "source_url": "https://web.ncku.edu.tw/p/406-1000-200439,r2663.php?Lang=zh-tw",
            "source_name": "National Cheng Kung University",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_05_feng_chia_university_common_good_hall": [
        {
            "label": "Primary case image",
            "url": "https://s3.ap-southeast-1.amazonaws.com/web-content.fcu.edu.tw/wp-content/uploads/sites/161/2025/02/24153506/%E5%85%B1%E5%96%84%E6%A8%93%E5%95%9F%E7%94%A8%E5%85%B8%E7%A6%AE-3.jpg",
            "source_url": "https://www.fcu.edu.tw/virtuosihall/about/",
            "source_name": "Feng Chia University",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_06_ntu_humanities_building": [
        {
            "label": "Primary case image",
            "url": "https://static.wixstatic.com/media/1d8676_9efee203e4de4cb6b2ba032df5e40cb4~mv2.jpg/v1/fill/w_4272,h_2848,al_c,q_90/L1220594_W.jpg",
            "source_url": "https://www.davision-design.com/portfolio-1-1/%E5%9C%8B%E7%AB%8B%E8%87%BA%E7%81%A3%E5%A4%A7%E5%AD%B8%E4%BA%BA%E6%96%87%E9%A4%A8",
            "source_name": "Da Vision Design",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_07_ntu_liberal_education_classroom_building": [
        {
            "label": "Primary case image",
            "url": "https://icrvb3jy.xinmedia.com/solomo/article/B/A/B/BAB45791-3DDD-3D8E-DE26-947676C72B25.jpeg",
            "source_url": "https://www.xinmedia.com/article/133942",
            "source_name": "Xinmedia",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_08_ncku_industrial_design_history_department": [
        {
            "label": "Primary case image",
            "url": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiBJwxpQ0jzMLCPjit0ZTBC7CQMm4d5zvfWq8uN-N2AFcn0bKUyAbgE3pmSG-MqBU_95LSjT79IWrTykQ5Go4deR5fQbk_W_3OdBoWP2dpazUOkRX7Kyeo3Hpc-HNaIUoPZAcJIyklToQk/s1600/jk%253Bbj%2527k.jpg",
            "source_url": "https://justabalcony.blogspot.com/2018/05/just-old_34.html",
            "source_name": "Just Old",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_09_scad_hong_kong_campus": [
        {
            "label": "Primary case image",
            "url": "https://zolimacitymag.com/wp-content/uploads/2019/05/1400_933.thumbnail.SCAD_zolima-citymag.webp",
            "source_url": "https://zolimacitymag.com/hong-kongs-modern-heritage-part-v-scad-the-former-north-kowloon-magistracy/",
            "source_name": "Zolima CityMag",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_10_scad_clark_hall": [
        {
            "label": "Primary case image",
            "url": "https://www.scad.edu/sites/default/files/Facilities/Savannah/Eichberg%20Hall%20and%20Eichberg%20Extension/Eichberg-Hall-Exterior-Spring-2019-AF_005_SN_SOLARPANELS_v1.jpg",
            "source_url": "https://www.scad.edu/life/buildings-and-facilities/clark-hall",
            "source_name": "SCAD",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_11_scad_bradley_hall": [
        {
            "label": "Primary case image",
            "url": "https://images.squarespace-cdn.com/content/v1/5d3202f82528ec00019477d6/1660831629512-8PK5Z6BV6REQBWISE9CH/YORK_TITLE.jpg",
            "source_url": "https://www.hansensavannah.com/ren-scad-bradley",
            "source_name": "Hansen Architects",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_12_scad_number_nine": [
        {
            "label": "Primary case image",
            "url": "https://www.scad.edu/sites/default/files/Facilities/Savannah/Number-Nine/Number-Nine-exterior-Fall-2019-AS-2.jpg",
            "source_url": "https://www.scad.edu/life/buildings-and-facilities/number-nine",
            "source_name": "SCAD",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_13_scad_ruskin_hall": [
        {
            "label": "Primary case image",
            "url": "https://www.lyncharch.com/wp-content/uploads/2021/04/portfolio-scad-ruskin-hall-01.jpg",
            "source_url": "https://www.lyncharch.com/projects/scad-ruskin-hall",
            "source_name": "Lynch Associates Architects",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_14_university_of_the_arts_london_granary_building": [
        {
            "label": "Primary case image",
            "url": "https://fsn1.your-objectstorage.com/stantonwilliams/223/conversions/stanton-williams-central-saint-martins-medium.jpg",
            "source_url": "https://stantonwilliams.com/en/works/central-saint-martins-college-of-art-and-design",
            "source_name": "Stanton Williams",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_15_university_of_pittsburgh_ford_factory": [
        {
            "label": "Primary case image",
            "url": "https://www.tradelineinc.com/sites/default/files/styles/article_feature/public/2023-09/Exterior_RESIZED.jpg?itok=dN3FvUcb",
            "source_url": "https://www.tradelineinc.com/reports/2023-9/adaptive-reuse-historic-industrial-building-helps-urban-university-keep-growing",
            "source_name": "Tradeline",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_16_guilford_technical_community_college_advanced_manufacturing_campus": [
        {
            "label": "Primary case image",
            "url": "https://cplteam.com/wp-content/uploads/2022/11/Guilford-Technical-College-CAM-Exterior.jpg",
            "source_url": "https://cplteam.com/blog/adaptive-reuse-reimagining-existing-campus-assets-in-creative-ways/",
            "source_name": "CPL",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_17_tu_delft_bk_city": [
        {
            "label": "Primary case image",
            "url": "https://europeanheritageawards-archive.eu/fileadmin/_processed_/3/1/csm_3a_temple_2006_64c5bb574a.jpg",
            "source_url": "https://europeanheritageawards-archive.eu/laureates-1978-2022/detail/the-making-of-bk-city-delft",
            "source_name": "European Heritage Awards Archive",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_18_university_of_toronto_daniels_building": [
        {
            "label": "Primary case image",
            "url": "https://images.adsttc.com/media/images/5ccc/4ab7/284d/d11e/3700/00c7/medium_jpg/03.jpg?1556892326",
            "source_url": "https://www.archdaily.com/916301/daniels-building-at-university-of-toronto-nadaaa",
            "source_name": "ArchDaily",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_19_duke_university_smith_warehouse": [
        {
            "label": "Primary case image",
            "url": "https://schooldesigns.com/wp-content/uploads/2019/09/1411asu056b-1.jpg",
            "source_url": "https://schooldesigns.com/Projects/duke-university-smith-warehouse-2/",
            "source_name": "SchoolDesigns",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
    "case_20_aalto_university_harald_herlin_learning_centre": [
        {
            "label": "Primary case image",
            "url": "https://images.adsttc.com/media/images/5983/1a00/b22e/3889/1400/0208/medium_jpg/Tuomas_Uusheimo-161103-aalto-oppimiskeskus-051.jpg?1501764057",
            "source_url": "https://www.archdaily.com/876977/aalto-university-library-harald-herlin-learning-centre-jkmm",
            "source_name": "ArchDaily",
            "source_type": "remote_reference",
            "usage_note": "Remote reference image; verify source permissions before redistribution.",
        }
    ],
}


TAXONOMY: list[dict[str, Any]] = [
    {
        "id": "1",
        "key": "architectural_layer",
        "label_en": "Architectural Layer",
        "label_zh": "建築層",
        "groups": [
            {
                "id": "1-1",
                "key": "structural_system",
                "label_en": "Structural System",
                "label_zh": "結構系統",
                "criteria": [
                    {
                        "key": "structural_regularity",
                        "label_zh": "結構規律性",
                        "terms": ["structure", "structural", "beams", "rhythm", "linear", "corridor", "arcade", "modular"],
                    },
                    {
                        "key": "large_span_space",
                        "label_zh": "大跨度空間",
                        "terms": ["large", "large-span", "large span", "industrial halls", "warehouse", "factory", "assembly plant", "manufacturing", "open industrial roof"],
                    },
                    {
                        "key": "modular_degree",
                        "label_zh": "模組化程度",
                        "terms": ["modular", "linear", "rhythm", "classrooms", "grid", "enclosed rooms", "workshop"],
                    },
                    {
                        "key": "floor_height_condition",
                        "label_zh": "層高條件",
                        "terms": ["large industrial halls", "large industrial", "warehouse", "factory", "skylights", "atrium", "open industrial roof", "industrial scale"],
                    },
                ],
            },
            {
                "id": "1-2",
                "key": "spatial_organization",
                "label_en": "Spatial Organization",
                "label_zh": "空間構成",
                "criteria": [
                    {
                        "key": "plan_composition",
                        "label_zh": "平面構成",
                        "terms": ["open plan", "linear layout", "courtyard", "cloister", "atrium", "double-loaded", "public ground", "sunken plaza", "terraced", "separate circulation"],
                    },
                    {
                        "key": "circulation_system",
                        "label_zh": "動線系統",
                        "terms": ["corridor", "circulation", "arcade", "skybridges", "axis", "ground floor", "public ground", "long corridor", "staggered"],
                    },
                    {
                        "key": "atrium_courtyard_corridor",
                        "label_zh": "中庭／迴廊",
                        "terms": ["atrium", "courtyard", "cloister", "corridor", "arcade"],
                    },
                    {
                        "key": "spatial_openness",
                        "label_zh": "空間開放性",
                        "terms": ["open", "openness", "permeable", "permeability", "transparent", "shared", "public ground", "light-filled", "airy"],
                    },
                ],
            },
            {
                "id": "1-3",
                "key": "spatial_character",
                "label_en": "Spatial Character",
                "label_zh": "空間特質",
                "criteria": [
                    {
                        "key": "spatial_scale",
                        "label_zh": "空間尺度",
                        "terms": ["large", "industrial scale", "monumentality", "multi-level", "terraced", "warehouse", "large industrial halls"],
                    },
                    {
                        "key": "publicness",
                        "label_zh": "公共性",
                        "terms": ["public", "shared", "community", "open", "learning commons", "collaborative", "interdisciplinary"],
                    },
                    {
                        "key": "rituality",
                        "label_zh": "儀式性",
                        "terms": ["ritual", "monumentality", "axis", "cloister", "courtyards and cloisters"],
                    },
                    {
                        "key": "industrial_historical_atmosphere",
                        "label_zh": "工業／歷史氛圍",
                        "terms": ["historic", "historical", "heritage", "victorian", "industrial", "factory", "warehouse", "hospital", "court", "barracks", "preserved", "stone", "timber"],
                    },
                ],
            },
        ],
    },
    {
        "id": "2",
        "key": "urban_context_layer",
        "label_en": "Urban Context Layer",
        "label_zh": "都市脈絡層",
        "groups": [
            {
                "id": "2-1",
                "key": "historical_context",
                "label_en": "Historical Context",
                "label_zh": "歷史脈絡",
                "criteria": [
                    {
                        "key": "industrial_heritage",
                        "label_zh": "工業遺產",
                        "terms": ["railroad", "industrial", "warehouse", "factory", "assembly plant", "manufacturing", "grain warehouse"],
                    },
                    {
                        "key": "military_heritage",
                        "label_zh": "軍事遺產",
                        "terms": ["military", "barracks"],
                    },
                    {
                        "key": "campus_history",
                        "label_zh": "校園歷史",
                        "terms": ["historic academic", "historic university", "university complex", "university", "campus", "academic building"],
                    },
                    {
                        "key": "local_memory",
                        "label_zh": "地方記憶",
                        "terms": ["heritage", "historic", "historical", "preserved", "victorian", "hospital", "court", "magistracy", "barracks", "old", "warehouse", "factory"],
                    },
                ],
            },
            {
                "id": "2-2",
                "key": "urban_relationship",
                "label_en": "Urban Relationship",
                "label_zh": "都市關係",
                "criteria": [
                    {
                        "key": "urban_interface",
                        "label_zh": "都市介面",
                        "terms": ["transparent facade", "facade", "public ground", "ground floor", "strip center", "street", "indoor-outdoor"],
                    },
                    {
                        "key": "campus_openness",
                        "label_zh": "校園開放性",
                        "terms": ["openness", "open", "permeable", "permeability", "transparent", "public ground", "shared"],
                    },
                    {
                        "key": "community_connection",
                        "label_zh": "社區連結",
                        "terms": ["community", "public interaction", "common good", "public ground", "learning commons", "collaborative", "shared", "interdisciplinary"],
                    },
                    {
                        "key": "public_accessibility",
                        "label_zh": "公共可達性",
                        "terms": ["public", "public ground", "open", "shared", "long corridor connecting public spaces", "separate circulation"],
                    },
                ],
            },
            {
                "id": "2-3",
                "key": "environmental_condition",
                "label_en": "Environmental Condition",
                "label_zh": "環境條件",
                "criteria": [
                    {
                        "key": "natural_daylighting",
                        "label_zh": "自然採光",
                        "terms": ["daylight", "daylighting", "skylight", "skylights", "light-filled", "transparent", "open facade"],
                    },
                    {
                        "key": "natural_ventilation",
                        "label_zh": "自然通風",
                        "terms": ["airy", "open", "atrium", "courtyard", "permeable"],
                    },
                    {
                        "key": "microclimate",
                        "label_zh": "微氣候",
                        "terms": ["landscape roof", "sunken plaza", "courtyard", "courtyards", "terraced", "indoor-outdoor", "transparent facade"],
                    },
                    {
                        "key": "green_environment",
                        "label_zh": "綠化環境",
                        "terms": ["landscape", "landscape roof", "roof", "courtyard", "courtyards", "terraced landscape", "green"],
                    },
                ],
            },
        ],
    },
    {
        "id": "3",
        "key": "temporal_transformation_layer",
        "label_en": "Temporal Transformation Layer",
        "label_zh": "時間轉化層",
        "groups": [
            {
                "id": "3-1",
                "key": "historical_evolution",
                "label_en": "Historical Evolution",
                "label_zh": "歷史演變",
                "criteria": [
                    {"key": "building_year", "label_zh": "建築年代", "mode": "year"},
                    {"key": "renovation_year", "label_zh": "改建年代", "mode": "year"},
                    {
                        "key": "historical_layering",
                        "label_zh": "歷史疊加",
                        "terms": ["historic", "historical", "preserved", "layered", "renovation", "adaptive reuse", "heritage", "victorian", "old"],
                    },
                    {
                        "key": "spatial_evolution",
                        "label_zh": "空間演變",
                        "mode": "transformation",
                    },
                ],
            },
            {
                "id": "3-2",
                "key": "functional_transformation",
                "label_en": "Functional Transformation",
                "label_zh": "機能轉化",
                "criteria": [
                    {
                        "key": "teaching_space",
                        "label_zh": "教學空間",
                        "terms": ["teaching", "classroom", "classrooms", "university", "learning", "academic", "college", "departments", "research"],
                    },
                    {
                        "key": "public_exchange",
                        "label_zh": "公共交流",
                        "terms": ["public", "shared", "community", "learning commons", "collaborative", "interdisciplinary", "open shared"],
                    },
                    {
                        "key": "exhibition_performance",
                        "label_zh": "展演活動",
                        "terms": ["art", "arts", "design", "exhibition", "performance", "history department"],
                    },
                    {
                        "key": "mixed_use",
                        "label_zh": "混合使用",
                        "terms": ["student housing / university use", "teaching and research", "departments", "collaborative learning", "public learning", "university facility"],
                    },
                ],
            },
            {
                "id": "3-3",
                "key": "adaptive_capacity",
                "label_en": "Adaptive Capacity",
                "label_zh": "持續利用能力",
                "criteria": [
                    {
                        "key": "spatial_flexibility",
                        "label_zh": "空間彈性",
                        "terms": ["flexible", "modular", "open plan", "open interior", "collaborative", "workshop", "permeable"],
                    },
                    {
                        "key": "structural_neutrality",
                        "label_zh": "結構中性",
                        "terms": ["large industrial halls", "warehouse", "factory", "open industrial roof", "open plan", "large", "industrial scale"],
                    },
                    {
                        "key": "functional_convertibility",
                        "label_zh": "機能可轉換性",
                        "mode": "transformation",
                    },
                    {
                        "key": "long_term_sustainability",
                        "label_zh": "長期永續性",
                        "terms": ["sustainability", "energy-efficient", "daylight", "renovation", "adaptive reuse", "preserved", "reuse"],
                    },
                ],
            },
        ],
    },
    {
        "id": "4",
        "key": "functional_layer",
        "label_en": "Functional Layer",
        "label_zh": "機能層",
        "groups": [
            {
                "id": "4-1",
                "key": "educational_function",
                "label_en": "Educational Function",
                "label_zh": "教育機能",
                "criteria": [
                    {"key": "classroom", "label_zh": "教室", "terms": ["classroom", "classrooms", "teaching", "academic", "university", "learning"]},
                    {"key": "studio", "label_zh": "Studio", "terms": ["studio", "art", "arts", "design", "industrial design", "scad"]},
                    {"key": "workshop", "label_zh": "Workshop", "terms": ["workshop", "manufacturing", "technical college", "factory", "industrial design"]},
                    {"key": "lecture_hall", "label_zh": "Lecture Hall", "terms": ["lecture hall", "lecture"]},
                ],
            },
            {
                "id": "4-2",
                "key": "public_function",
                "label_en": "Public Function",
                "label_zh": "公共機能",
                "criteria": [
                    {"key": "atrium", "label_zh": "中庭", "terms": ["atrium"]},
                    {"key": "lounge", "label_zh": "Lounge", "terms": ["lounge", "shared spaces", "learning commons", "public spaces", "common good"]},
                    {"key": "exhibition_space", "label_zh": "展覽空間", "terms": ["exhibition", "art", "arts", "design", "history department"]},
                    {"key": "cafe", "label_zh": "Cafe", "terms": ["cafe", "café"]},
                ],
            },
            {
                "id": "4-3",
                "key": "mixed_use_function",
                "label_en": "Mixed-use Function",
                "label_zh": "混合使用",
                "criteria": [
                    {"key": "administration", "label_zh": "行政", "terms": ["departments", "university facility", "campus facility"]},
                    {"key": "community_shared", "label_zh": "社區共享", "terms": ["community", "public", "shared", "common good", "public interaction"]},
                    {"key": "performance", "label_zh": "展演活動", "terms": ["performance", "exhibition", "art", "arts", "design"]},
                    {"key": "interdisciplinary_exchange", "label_zh": "跨域交流", "terms": ["interdisciplinary", "collaborative", "learning commons", "teaching and research", "art and design"]},
                ],
            },
        ],
    },
    {
        "id": "5",
        "key": "typology_layer",
        "label_en": "Typology Layer",
        "label_zh": "類型層",
        "groups": [
            {
                "id": "5-1",
                "key": "campus_renewal",
                "label_en": "Campus Renewal",
                "label_zh": "校園更新",
                "criteria": [
                    {"key": "public_connectivity", "label_zh": "Public Connectivity", "terms": ["public", "shared", "open", "corridor", "public ground", "campus publicness"]},
                    {"key": "flexible_learning", "label_zh": "Flexible Learning", "terms": ["flexible", "modular", "learning", "classrooms", "collaborative", "studio", "workshop"]},
                    {"key": "historic_integration", "label_zh": "Historic Integration", "terms": ["historic", "historical", "heritage", "preserved", "adaptive reuse", "renovation", "victorian", "old"]},
                ],
            },
            {
                "id": "5-2",
                "key": "industrial_reuse",
                "label_en": "Industrial Reuse",
                "label_zh": "工業再利用",
                "criteria": [
                    {"key": "large_span", "label_zh": "Large-span", "terms": ["large", "large-span", "large span", "industrial halls", "warehouse", "factory", "open industrial roof"]},
                    {"key": "linear_modular", "label_zh": "Linear Modular", "terms": ["linear", "modular", "rhythm", "railroad", "assembly plant", "manufacturing"]},
                    {"key": "factory_conversion", "label_zh": "Factory Conversion", "terms": ["factory", "assembly plant", "manufacturing", "industrial manufacturing", "industrial reuse"]},
                ],
            },
            {
                "id": "5-3",
                "key": "military_reuse",
                "label_en": "Military Reuse",
                "label_zh": "軍事再利用",
                "criteria": [
                    {"key": "barrack_conversion", "label_zh": "Barrack Conversion", "terms": ["barracks", "military barracks"]},
                    {"key": "corridor_type", "label_zh": "Corridor Type", "terms": ["corridor", "arcade"]},
                    {"key": "courtyard_type", "label_zh": "Courtyard Type", "terms": ["courtyard"]},
                ],
            },
            {
                "id": "5-4",
                "key": "institutional_reuse",
                "label_en": "Institutional Reuse",
                "label_zh": "機構再利用",
                "criteria": [
                    {"key": "hospital", "label_zh": "Hospital", "terms": ["hospital"]},
                    {"key": "court", "label_zh": "Court", "terms": ["court", "courtroom", "magistracy", "jail"]},
                    {"key": "government_building", "label_zh": "Government Building", "terms": ["government", "magistracy", "court", "jail"]},
                    {"key": "commercial_building", "label_zh": "Commercial Building", "terms": ["commercial", "strip center"]},
                ],
            },
        ],
    },
    {
        "id": "6",
        "key": "adaptive_transformation_layer",
        "label_en": "Adaptive Transformation Layer",
        "label_zh": "適應轉型層",
        "groups": [
            {
                "id": "6-1",
                "key": "adaptation_model",
                "label_en": "Adaptation Model",
                "label_zh": "適應模式",
                "criteria": [
                    {"key": "what_changed", "label_zh": "改變內容", "mode": "adaptation_model"},
                    {"key": "why_changed", "label_zh": "改變原因", "mode": "adaptation_model"},
                    {"key": "what_remained", "label_zh": "保留內容", "mode": "adaptation_model"},
                    {"key": "how_space_adapted", "label_zh": "空間如何適應", "mode": "adaptation_model"},
                    {"key": "evidence", "label_zh": "證據", "mode": "adaptation_model"},
                ],
            },
            {
                "id": "6-2",
                "key": "behavior",
                "label_en": "Spatial Behavior",
                "label_zh": "空間行為",
                "criteria": [
                    {"key": "informal_learning", "label_zh": "非正式學習", "terms": ["university", "learning commons", "public learning", "adaptive learning", "study", "groupwork", "library", "lounge", "shared spaces", "open shared", "open plan", "open interior", "airy interior", "studio", "workshop", "cafe", "corridor", "arcade"]},
                    {"key": "group_discussion", "label_zh": "群體討論", "terms": ["groupwork", "collaborative", "studio", "workshop", "classroom", "classrooms", "seminar", "public exchange", "interdisciplinary", "open shared", "enclosed rooms", "departments", "architecture", "design", "technical college"]},
                    {"key": "knowledge_sharing", "label_zh": "知識分享", "terms": ["university", "exhibition", "public programming", "learning commons", "library", "shared", "public", "interdisciplinary", "collaborative", "teaching and research", "art", "arts", "design", "departments", "heritage"]},
                    {"key": "social_interaction", "label_zh": "社交互動", "terms": ["university", "public", "community", "shared", "lounge", "cafe", "atrium", "courtyard", "corridor", "arcade", "openness", "open interior", "public ground", "campus-city interface", "campus gateway", "common good"]},
                ],
            },
            {
                "id": "6-3",
                "key": "organizational_driver",
                "label_en": "Organizational Driver",
                "label_zh": "組織機制",
                "criteria": [
                    {"key": "cross_disciplinary_curriculum", "label_zh": "跨域課程", "terms": ["interdisciplinary", "art and design", "architecture", "landscape and design", "built environment", "departments", "collaborative", "common good"]},
                    {"key": "project_based_learning", "label_zh": "專題式學習", "terms": ["teaching and research", "modular learning", "classroom", "classrooms", "studio", "workshop", "design", "manufacturing", "technical college", "collaborative learning", "architecture school", "art", "arts"]},
                    {"key": "shared_facility_management", "label_zh": "共享設施管理", "terms": ["shared", "learning commons", "library", "public spaces", "campus facility", "university facility", "university building", "student housing / university use", "university use", "common good", "public interior streets"]},
                    {"key": "community_engagement", "label_zh": "社群參與", "terms": ["community", "public", "public programming", "campus-city interface", "campus gateway", "public interaction", "common good", "public ground"]},
                ],
            },
            {
                "id": "6-4",
                "key": "transformation_driver",
                "label_en": "Transformation Driver",
                "label_zh": "轉型動力",
                "criteria": [
                    {"key": "pedagogical_change", "label_zh": "教學模式改變", "terms": ["learning", "teaching", "classroom", "classrooms", "studio", "workshop", "collaborative", "flexible learning", "architecture faculty", "technical college"]},
                    {"key": "technology_change", "label_zh": "技術需求改變", "terms": ["technical", "technology", "manufacturing", "advanced manufacturing", "workshop", "industrial design", "daylight", "skylights", "energy-efficient"]},
                    {"key": "enrollment_growth", "label_zh": "成長與擴充需求", "terms": ["campus renewal", "university facility", "university building", "learning centre", "large", "large-span", "campus facility", "public connectivity"]},
                    {"key": "financial_pressure", "label_zh": "資源與成本壓力", "terms": ["reuse", "adaptive reuse", "renovation", "preserved", "sustainability", "energy-efficient", "existing campus assets", "factory reuse", "warehouse reuse", "heritage reuse"]},
                    {"key": "community_outreach", "label_zh": "公共與社區連結", "terms": ["public", "community", "public programming", "campus-city interface", "campus gateway", "public ground", "public interaction", "common good"]},
                ],
            },
        ],
    },
]


def normalize(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def slugify(value: str) -> str:
    value = normalize(value)
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_") or "unnamed"


def column_index(cell_ref: str) -> int:
    letters = "".join(ch for ch in cell_ref if ch.isalpha())
    index = 0
    for ch in letters:
        index = index * 26 + ord(ch.upper()) - 64
    return index - 1


def read_xlsx_rows(path: Path) -> list[dict[str, Any]]:
    with zipfile.ZipFile(path) as archive:
        shared_strings: list[str] = []
        shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
        for item in shared_root.findall("a:si", NS):
            shared_strings.append("".join(text.text or "" for text in item.findall(".//a:t", NS)))

        sheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
        table: list[list[str]] = []
        max_col = 0
        for row in sheet.findall(".//a:sheetData/a:row", NS):
            values: dict[int, str] = {}
            for cell in row.findall("a:c", NS):
                ref = cell.attrib.get("r", "")
                index = column_index(ref)
                max_col = max(max_col, index)
                cell_type = cell.attrib.get("t")
                value_node = cell.find("a:v", NS)
                value = "" if value_node is None else (value_node.text or "")
                if cell_type == "s" and value:
                    value = shared_strings[int(value)]
                elif cell_type == "inlineStr":
                    value = "".join(text.text or "" for text in cell.findall(".//a:t", NS))
                values[index] = value.strip()
            table.append([values.get(index, "") for index in range(max_col + 1)])

    if not table:
        return []

    headers = [slugify(header) for header in table[0]]
    rows: list[dict[str, Any]] = []
    for row_number, row in enumerate(table[1:], start=2):
        record = {headers[index]: row[index].strip() if index < len(row) else "" for index in range(len(headers))}
        if not record.get("case"):
            continue
        record["source_row"] = row_number
        rows.append(record)
    return rows


def source_phrases(case: dict[str, Any]) -> list[tuple[str, str]]:
    phrase_fields = {
        "case": [case.get("case", "")],
        "original_function": [case.get("original_function", "")],
        "current_function": [case.get("current_function", "")],
        "key_spatial_features": re.split(r"\s*,\s*", case.get("key_spatial_features", "")),
        "keywords": re.split(r"\s*,\s*", case.get("keywords", "")),
        "region_country": [case.get("region_country", "")],
        "location": [case.get("location", "")],
    }
    phrases: list[tuple[str, str]] = []
    for field, values in phrase_fields.items():
        for value in values:
            value = str(value or "").strip()
            if value:
                phrases.append((field, value))
    return phrases


def find_evidence(case: dict[str, Any], terms: list[str]) -> list[str]:
    matches: list[str] = []
    normalized_terms = [normalize(term) for term in terms]
    for field, phrase in source_phrases(case):
        text = normalize(phrase)
        if any(term and term in text for term in normalized_terms):
            evidence = f"{field}: {phrase}"
            if evidence not in matches:
                matches.append(evidence)
    return matches


def is_reuse_transformation(case: dict[str, Any]) -> bool:
    original = normalize(case.get("original_function"))
    current = normalize(case.get("current_function"))
    if not original or not current:
        return False
    if original == current:
        return False
    if original.startswith("new ") or "contemporary campus building" in original:
        return False
    return True


def year_node(case: dict[str, Any], key: str, label_zh: str) -> dict[str, Any]:
    year = str(case.get("year") or "").strip() or None
    return {
        "label_zh": label_zh,
        "present": bool(year),
        "confidence": "high" if year else "none",
        "value": year,
        "evidence": [f"year: {year}"] if year else [],
        "inference": "Excel Year 欄位目前空白。" if not year else "",
    }


def transformation_node(case: dict[str, Any], label_zh: str) -> dict[str, Any]:
    original = case.get("original_function", "")
    current = case.get("current_function", "")
    present = is_reuse_transformation(case)
    evidence = [f"original_function -> current_function: {original} -> {current}"] if present else []
    return {
        "label_zh": label_zh,
        "present": present,
        "confidence": "medium" if present else "none",
        "value": present,
        "evidence": evidence,
        "inference": "由原機能與現機能不同推論為再利用／轉用案例。" if present else "原機能顯示為新建或資料不足，未判定為轉用。",
    }


def combined_source_text(case: dict[str, Any]) -> str:
    return normalize(" ".join(phrase for _, phrase in source_phrases(case)))


def contains_any(text: str, terms: list[str]) -> bool:
    return any(normalize(term) in text for term in terms)


def build_adaptation_model(case: dict[str, Any]) -> dict[str, str]:
    original = case.get("original_function") or "Existing campus asset"
    current = case.get("current_function") or "new campus use"
    features = case.get("key_spatial_features") or ""
    keywords = split_items(case.get("keywords", ""))
    text = combined_source_text(case)

    if is_reuse_transformation(case):
        what_changed = f"{original} was transformed into {current}."
    else:
        what_changed = f"The campus asset was configured or renewed to support {current}."

    reasons: list[str] = []
    if contains_any(text, ["learning", "teaching", "classroom", "studio", "workshop", "collaborative", "flexible"]):
        reasons.append("support contemporary pedagogy, flexible learning, and collaborative work")
    if contains_any(text, ["historic", "heritage", "victorian", "preserved", "renovation", "adaptive reuse", "old"]):
        reasons.append("retain historical value while introducing updated university functions")
    if contains_any(text, ["public", "community", "open", "shared", "public ground", "campus-city", "campus gateway"]):
        reasons.append("strengthen campus publicness and social exchange")
    if contains_any(text, ["industrial", "warehouse", "factory", "manufacturing", "large-span", "large industrial"]):
        reasons.append("reuse robust large-scale structures for academic and creative programs")
    why_changed = "; ".join(reasons) or "respond to updated campus program needs and long-term spatial adaptability"

    remained: list[str] = []
    if is_reuse_transformation(case):
        remained.append(f"the memory and spatial identity of the former {original}")
    if contains_any(text, ["corridor", "arcade"]):
        remained.append("linear circulation logic")
    if contains_any(text, ["courtyard", "cloister"]):
        remained.append("courtyard or cloister organization")
    if contains_any(text, ["industrial", "warehouse", "factory", "timber", "stone", "gothic", "victorian", "preserved"]):
        remained.append("heritage material or structural character")
    what_remained = "; ".join(remained) or "the campus role and spatial continuity of the existing setting"

    if features:
        how_space_adapted = f"Spatial features such as {features} were used to accommodate {current}."
    else:
        how_space_adapted = f"The space was reprogrammed to accommodate {current}."

    evidence_parts = [
        f"original_function: {case.get('original_function')}" if case.get("original_function") else "",
        f"current_function: {case.get('current_function')}" if case.get("current_function") else "",
        f"key_spatial_features: {features}" if features else "",
        f"keywords: {', '.join(keywords)}" if keywords else "",
    ]

    return {
        "what_changed": what_changed,
        "why_changed": why_changed,
        "what_remained": what_remained,
        "how_space_adapted": how_space_adapted,
        "evidence": " | ".join(part for part in evidence_parts if part),
    }


def adaptation_model_node(case: dict[str, Any], key: str, label_zh: str) -> dict[str, Any]:
    value = build_adaptation_model(case).get(key, "")
    return {
        "label_zh": label_zh,
        "present": bool(value),
        "confidence": "medium" if value else "none",
        "value": value or None,
        "evidence": [value] if value else [],
        "inference": "Rule-based adaptation model synthesized from source fields." if value else "",
    }


def criterion_node(case: dict[str, Any], criterion: dict[str, Any]) -> dict[str, Any]:
    key = criterion["key"]
    label_zh = criterion.get("label_zh", key)
    if criterion.get("mode") == "year":
        return year_node(case, key, label_zh)
    if criterion.get("mode") == "transformation":
        return transformation_node(case, label_zh)
    if criterion.get("mode") == "adaptation_model":
        return adaptation_model_node(case, key, label_zh)

    evidence = find_evidence(case, criterion.get("terms", []))
    present = bool(evidence)
    return {
        "label_zh": label_zh,
        "present": present,
        "confidence": "high" if present else "none",
        "value": present,
        "evidence": evidence,
        "inference": "" if present else "來源欄位未出現可判定關鍵詞。",
    }


def build_knowledge_precedent(case: dict[str, Any]) -> dict[str, Any]:
    knowledge: dict[str, Any] = {}
    for layer in TAXONOMY:
        layer_data: dict[str, Any] = {
            "id": layer["id"],
            "label_en": layer["label_en"],
            "label_zh": layer["label_zh"],
            "groups": {},
            "present_tags": [],
        }
        for group in layer["groups"]:
            group_data: dict[str, Any] = {
                "id": group["id"],
                "label_en": group["label_en"],
                "label_zh": group["label_zh"],
                "criteria": {},
                "present_tags": [],
            }
            for criterion in group["criteria"]:
                result = criterion_node(case, criterion)
                group_data["criteria"][criterion["key"]] = result
                if result["present"]:
                    tag = {
                        "group": group["key"],
                        "criterion": criterion["key"],
                        "label_zh": result["label_zh"],
                    }
                    group_data["present_tags"].append(tag)
                    layer_data["present_tags"].append(tag)
            layer_data["groups"][group["key"]] = group_data
        knowledge[layer["key"]] = layer_data
    return knowledge


def split_items(value: str) -> list[str]:
    return [item.strip() for item in re.split(r"\s*,\s*", value or "") if item.strip()]


def infer_semantic_relations(case: dict[str, Any]) -> list[dict[str, Any]]:
    features = normalize(case.get("key_spatial_features"))
    current = case.get("current_function") or "campus use"
    relations: list[dict[str, Any]] = []

    def add(subject: str, relation: str, relation_type: str, obj: str, evidence: str) -> None:
        item = {
            "subject": subject,
            "relation": relation,
            "relation_type": relation_type,
            "object": obj,
            "evidence": evidence,
        }
        if item not in relations:
            relations.append(item)

    if "corridor" in features:
        add("Corridor", "connects", "Circulation Relation", "public or teaching spaces", case.get("key_spatial_features", ""))
    if "atrium" in features:
        add("Atrium", "brings daylight into", "Environmental Relation", current, case.get("key_spatial_features", ""))
    if "courtyard" in features or "cloister" in features:
        add("Courtyard/Cloister", "organizes", "Spatial Relation", "public campus movement", case.get("key_spatial_features", ""))
    if "transparent facade" in features or "open facade" in features:
        add("Transparent facade", "connects visually with", "Perceptual Relation", "campus public realm", case.get("key_spatial_features", ""))
    if "open plan" in features or "open interior" in features:
        add("Open plan/interior", "supports", "Functional Relation", "flexible learning use", case.get("key_spatial_features", ""))
    if "landscape roof" in features or "terraced landscape" in features:
        add("Landscape roof/terrain", "integrates", "Environmental Relation", "green campus environment", case.get("key_spatial_features", ""))
    if "skybridges" in features:
        add("Skybridges", "link", "Circulation Relation", "multi-level campus spaces", case.get("key_spatial_features", ""))
    if "arcade" in features:
        add("Arcade corridor", "extends along", "Circulation Relation", "linear plan", case.get("key_spatial_features", ""))
    if "separate circulation" in features:
        add("Separate circulation systems", "organize", "Circulation Relation", "reused institutional spaces", case.get("key_spatial_features", ""))
    if "large industrial halls" in features:
        add("Large industrial halls", "accommodate", "Functional Relation", "collaborative learning space", case.get("key_spatial_features", ""))
    if "workshop" in features:
        add("Workshop spaces", "expose", "Functional Relation", "technical learning activities", case.get("key_spatial_features", ""))
    if "skylight" in features or "skylights" in features:
        add("Skylights", "bring daylight into", "Environmental Relation", current, case.get("key_spatial_features", ""))
    if "preserved" in features:
        add("Preserved structure/layout", "anchors", "Conceptual Relation", "historic integration", case.get("key_spatial_features", ""))

    return relations


def build_precedent_dna(case: dict[str, Any]) -> dict[str, Any]:
    features = split_items(case.get("key_spatial_features", ""))
    keywords = split_items(case.get("keywords", ""))
    c1 = []
    for item in features + keywords:
        if item not in c1:
            c1.append(item)

    return {
        "Gene_A": {
            "location": case.get("location") or case.get("region_country") or None,
            "site_conditions": None,
            "functional_needs": case.get("current_function") or None,
            "cultural_context": case.get("original_function") or None,
        },
        "Gene_B": {
            "issue": "校園更新或既有建築再利用需求。",
            "concept": "以既有空間特徵轉化為教學、公共交流或跨域學習資源。",
            "strategy": "依來源欄位中的結構、動線、開放性、歷史脈絡與機能轉化線索進行分類。",
        },
        "Gene_C1": c1,
        "Gene_C2": infer_semantic_relations(case),
        "Gene_D": {
            "user_behavior": None,
            "media_feedback": None,
            "designer_reflection": None,
        },
    }


def case_images_for(case_id: str) -> list[dict[str, str]]:
    return [image.copy() for image in CASE_IMAGE_REFERENCES.get(case_id, [])]


def sixth_layer_group_criteria(group_key: str) -> list[dict[str, Any]]:
    for layer in TAXONOMY:
        if layer.get("key") != "adaptive_transformation_layer":
            continue
        for group in layer.get("groups", []):
            if group.get("key") == group_key:
                return group.get("criteria", [])
    return []


def active_sixth_layer_values(case: dict[str, Any], group_key: str) -> list[str]:
    values: list[str] = []
    for criterion in sixth_layer_group_criteria(group_key):
        if criterion.get("mode"):
            continue
        if find_evidence(case, criterion.get("terms", [])):
            values.append(criterion["key"])
    return values


def build_adaptive_transformation_analysis(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "adaptation_model": build_adaptation_model(case),
        "behavior": active_sixth_layer_values(case, "behavior"),
        "organizational_driver": active_sixth_layer_values(case, "organizational_driver"),
        "transformation_driver": active_sixth_layer_values(case, "transformation_driver"),
    }


def build_case(case: dict[str, Any], index: int) -> dict[str, Any]:
    case_name = case.get("case", "")
    case_id = f"case_{index:02d}_{slugify(case_name)}"
    knowledge_precedent = build_knowledge_precedent(case)
    precedent_dna = build_precedent_dna(case)
    adaptive_transformation_analysis = build_adaptive_transformation_analysis(case)
    return {
        "id": case_id,
        "case_name": case_name,
        "source": {
            "file": "campus_cases.xlsx",
            "sheet": "Campus Adaptive Reuse Cases",
            "row": case.get("source_row"),
        },
        "raw_fields": {
            "original_function": case.get("original_function") or None,
            "current_function": case.get("current_function") or None,
            "key_spatial_features": case.get("key_spatial_features") or None,
            "keywords": split_items(case.get("keywords", "")),
            "region_country": case.get("region_country") or None,
            "year": case.get("year") or None,
            "location": case.get("location") or None,
            "continent": case.get("continent") or None,
            "floor": case.get("floor") or None,
        },
        "case_images": case_images_for(case_id),
        "adaptive_transformation_analysis": adaptive_transformation_analysis,
        "knowledge_precedent": knowledge_precedent,
        "precedent_dna": precedent_dna,
        "notes": "Rule-based extraction from sparse spreadsheet data. Empty Excel fields are kept as null; inferred tags include evidence.",
    }


def taxonomy_for_output() -> dict[str, Any]:
    return {
        "name": "Campus Adaptive Reuse Knowledge Precedent Taxonomy",
        "description": "Six-layer taxonomy for campus adaptive reuse case extraction, including adaptive transformation behavior and drivers.",
        "layers": TAXONOMY,
    }


def collect_layer_tags(case: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    tags: dict[str, list[dict[str, Any]]] = {}
    for layer_key, layer in case["knowledge_precedent"].items():
        tags[layer_key] = [
            {
                "group": tag["group"],
                "criterion": tag["criterion"],
                "label_zh": tag["label_zh"],
            }
            for tag in layer.get("present_tags", [])
        ]
    return tags


def relation_summary(case: dict[str, Any]) -> list[str]:
    summaries = []
    for relation in case["precedent_dna"].get("Gene_C2", []):
        summaries.append(
            f"{relation['subject']} -> {relation['relation']} "
            f"({relation['relation_type']}) -> {relation['object']}"
        )
    return summaries


def add_to_index(index: dict[str, list[str]], key: str | None, case_id: str) -> None:
    if not key:
        return
    index.setdefault(key, [])
    if case_id not in index[key]:
        index[key].append(case_id)


def build_case_overview(cases: list[dict[str, Any]]) -> dict[str, Any]:
    overview_cases = []
    by_region_country: dict[str, list[str]] = {}
    by_typology: dict[str, list[str]] = {}
    by_keyword: dict[str, list[str]] = {}
    by_behavior: dict[str, list[str]] = {}
    by_organizational_driver: dict[str, list[str]] = {}
    by_transformation_driver: dict[str, list[str]] = {}

    for index, case in enumerate(cases, start=1):
        raw = case["raw_fields"]
        adaptive_analysis = case.get("adaptive_transformation_analysis", {})
        layer_tags = collect_layer_tags(case)
        typology_tags = layer_tags.get("typology_layer", [])
        typology_keys = [tag["criterion"] for tag in typology_tags]
        case_id = case["id"]

        add_to_index(by_region_country, raw.get("region_country"), case_id)
        for tag in typology_keys:
            add_to_index(by_typology, tag, case_id)
        for keyword in raw.get("keywords", []):
            add_to_index(by_keyword, keyword, case_id)
        for behavior in adaptive_analysis.get("behavior", []):
            add_to_index(by_behavior, behavior, case_id)
        for driver in adaptive_analysis.get("organizational_driver", []):
            add_to_index(by_organizational_driver, driver, case_id)
        for driver in adaptive_analysis.get("transformation_driver", []):
            add_to_index(by_transformation_driver, driver, case_id)

        overview_cases.append(
            {
                "case_no": index,
                "id": case_id,
                "case_name": case["case_name"],
                "original_function": raw.get("original_function"),
                "current_function": raw.get("current_function"),
                "region_country": raw.get("region_country"),
                "year": raw.get("year"),
                "location": raw.get("location"),
                "key_spatial_features": raw.get("key_spatial_features"),
                "keywords": raw.get("keywords", []),
                "case_images": case.get("case_images", []),
                "adaptive_transformation_analysis": adaptive_analysis,
                "typology_tags": typology_keys,
                "layer_tags": layer_tags,
                "spatial_vocabulary": case["precedent_dna"].get("Gene_C1", []),
                "semantic_relations": relation_summary(case),
                "transformation_summary": {
                    "from": raw.get("original_function"),
                    "to": raw.get("current_function"),
                },
            }
        )

    return {
        "metadata": {
            "name": "Adaptive Campus Case Overview",
            "source_file": "campus_cases.xlsx",
            "case_count": len(cases),
            "purpose": "Compact overview for browsing, filtering, and uploading to My GPT when the full knowledge database is too large.",
        },
        "indexes": {
            "by_region_country": by_region_country,
            "by_typology": by_typology,
            "by_keyword": by_keyword,
            "by_behavior": by_behavior,
            "by_organizational_driver": by_organizational_driver,
            "by_transformation_driver": by_transformation_driver,
        },
        "cases": overview_cases,
    }


def main() -> None:
    rows = read_xlsx_rows(SOURCE_XLSX)
    cases = [build_case(row, index) for index, row in enumerate(rows, start=1)]

    OUTPUT_DIR.mkdir(exist_ok=True)
    CASES_DIR.mkdir(exist_ok=True)

    taxonomy = taxonomy_for_output()
    (OUTPUT_DIR / "taxonomy.json").write_text(json.dumps(taxonomy, ensure_ascii=False, indent=2), encoding="utf-8")

    database = {
        "metadata": {
            "name": "Adaptive Campus Case Study Knowledge Precedents",
            "source_file": "campus_cases.xlsx",
            "case_count": len(cases),
            "extraction_method": "Rule-based extraction aligned with the midterm Precedent DNA workflow and the six-layer campus taxonomy.",
        },
        "taxonomy": taxonomy,
        "cases": cases,
    }
    (OUTPUT_DIR / "campus_knowledge_precedents.json").write_text(
        json.dumps(database, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (ROOT / "campus_knowledge_precedents_MyGPT_upload.json").write_text(
        json.dumps(database, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    overview = build_case_overview(cases)
    (OUTPUT_DIR / "case_overview.json").write_text(
        json.dumps(overview, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    for case in cases:
        (CASES_DIR / f"{case['id']}.json").write_text(json.dumps(case, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Generated {len(cases)} cases")
    print(OUTPUT_DIR / "campus_knowledge_precedents.json")
    print(OUTPUT_DIR / "case_overview.json")
    print(OUTPUT_DIR / "taxonomy.json")
    print(CASES_DIR)


if __name__ == "__main__":
    main()
