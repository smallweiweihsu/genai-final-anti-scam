"""Clean and deduplicate collected phishing dataset cases."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "crawler" / "output"
RAW_CASES = OUT_DIR / "raw_cases.json"
CLEAN_CASES = OUT_DIR / "clean_cases.json"


REQUIRED_TEXT_FIELDS = [
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


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", str(value)).strip()


def normalize_case(case: dict) -> dict:
    item = dict(case)
    for key, value in list(item.items()):
        item[key] = normalize_space(value)
    item["sender_domain"] = item["sender_domain"].lower()
    item["has_link"] = "true" if item["has_link"] == "true" else "false"
    item["has_attachment"] = "true" if item["has_attachment"] == "true" else "false"
    item["urgency_level"] = item["urgency_level"] if item["urgency_level"] in {"low", "medium", "high"} else "medium"
    item["risk_label"] = item["risk_label"] if item["risk_label"] in {"phishing", "normal", "suspicious"} else "suspicious"
    return item


def has_enough_content(case: dict) -> bool:
    content = case.get("email_content", "")
    return len(content) >= 80 and len(content.split()) >= 8


def dedupe_text_cases(cases: list[dict]) -> list[dict]:
    seen: set[str] = set()
    cleaned: list[dict] = []
    for case in cases:
        item = normalize_case(case)
        if not has_enough_content(item):
            continue
        fingerprint = (item["email_subject"] + "|" + item["email_content"]).lower()
        fingerprint = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", fingerprint)
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        cleaned.append({field: item.get(field, "") for field in REQUIRED_TEXT_FIELDS})

    for index, item in enumerate(cleaned, start=1):
        item["id"] = f"T{index:04d}"
    return cleaned


def dedupe_image_cases(cases: list[dict]) -> list[dict]:
    seen: set[str] = set()
    cleaned: list[dict] = []
    for case in cases:
        item = {key: normalize_space(value) for key, value in case.items()}
        fingerprint = (item.get("image_case_type", "") + "|" + item.get("description", "") + "|" + item.get("text_in_image", "")).lower()
        if fingerprint in seen:
            # Keep multiple mock file rows only if the filename differs for planned assets.
            fingerprint = fingerprint + "|" + item.get("image_file", "")
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        cleaned.append(item)

    for index, item in enumerate(cleaned, start=1):
        item["id"] = f"I{index:04d}"
    return cleaned


def main() -> int:
    if not RAW_CASES.exists():
        raise FileNotFoundError(f"Missing {RAW_CASES}. Run search_and_collect.py first.")

    payload = json.loads(RAW_CASES.read_text(encoding="utf-8"))
    clean_payload = {
        "generated_at": payload.get("generated_at"),
        "dataset_policy": payload.get("dataset_policy"),
        "sources": payload.get("sources", []),
        "text_cases": dedupe_text_cases(payload.get("text_cases", [])),
        "image_cases": dedupe_image_cases(payload.get("image_cases", [])),
    }
    CLEAN_CASES.write_text(json.dumps(clean_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    from export_csv import main as export_main

    return export_main()


if __name__ == "__main__":
    sys.exit(main())
