"""Export cleaned phishing dataset cases to CSV and sources.md."""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "crawler" / "output"
CLEAN_CASES = OUT_DIR / "clean_cases.json"
DATASET = ROOT / "dataset"

TEXT_FIELDS = [
    "id",
    "email_subject",
    "email_content",
    "sender",
    "sender_domain",
    "has_link",
    "has_attachment",
    "urgency_level",
    "suspicious_keywords",
    "phishing_type",
    "risk_label",
    "explanation",
    "source_url",
    "source_type",
]

IMAGE_FIELDS = [
    "id",
    "image_file",
    "case_title",
    "image_case_type",
    "risk_label",
    "description",
    "visual_risk_points",
    "text_in_image",
    "source_url",
    "source_type",
    "license_note",
    "can_be_public_demo",
]


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def write_sources(path: Path, payload: dict) -> None:
    sources = payload.get("sources", [])
    source_counter = Counter(case["source_url"] for case in payload.get("text_cases", []))
    image_counter = Counter(case["source_url"] for case in payload.get("image_cases", []))

    lines = [
        "# 資料來源紀錄",
        "",
        f"蒐集日期：{payload.get('generated_at')}",
        "",
        "本資料集採用可信來源導向的安全改寫策略：不重新散布真實釣魚信全文、不保存活的惡意連結、不包含真實個資或真實登入資料。案例內容為依照來源中描述的攻擊型態進行去品牌化、去連結與改寫後的教學 / demo 資料。",
        "",
        "## 來源清單",
        "",
        "| 資料來源 | URL | 類型 | 是否可信 | HTTP 狀態 | 備註 | 文字案例數 | 圖片案例數 |",
        "| --- | --- | --- | --- | --- | --- | ---: | ---: |",
    ]

    for source in sources:
        url = source["url"]
        trusted = "是" if source.get("trusted") else "待確認"
        status = source.get("http_status") or "未取得"
        notes = str(source.get("notes", "")).replace("|", " ")
        lines.append(
            f"| {source['name']} | {url} | {source['source_type']} | {trusted} | {status} | {notes} | {source_counter[url]} | {image_counter[url]} |"
        )

    lines.extend(
        [
            "",
            "## 使用限制",
            "",
            "- 可用於期末專案、模型 prototype、介面展示與教育用途。",
            "- 不應將此資料集視為原始威脅情資或可執法證據。",
            "- 不得加入 API key、真實個資、真實信用卡、真實驗證碼、真實釣魚頁內容或可疑附件。",
            "- 若後續新增外部原文案例，必須先確認授權，授權不明者只記錄來源，不重新散布內容。",
        ]
    )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if not CLEAN_CASES.exists():
        raise FileNotFoundError(f"Missing {CLEAN_CASES}. Run clean_dataset.py first.")

    payload = json.loads(CLEAN_CASES.read_text(encoding="utf-8"))
    DATASET.mkdir(exist_ok=True)
    write_csv(DATASET / "text_cases.csv", payload.get("text_cases", []), TEXT_FIELDS)
    write_csv(DATASET / "image_cases.csv", payload.get("image_cases", []), IMAGE_FIELDS)
    write_sources(DATASET / "sources.md", payload)

    summary = {
        "text_cases": len(payload.get("text_cases", [])),
        "image_cases": len(payload.get("image_cases", [])),
        "risk_labels": Counter(case["risk_label"] for case in payload.get("text_cases", [])),
        "phishing_types": Counter(case["phishing_type"] for case in payload.get("text_cases", [])),
        "source_types": Counter(case["source_type"] for case in payload.get("text_cases", [])),
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
