"""Build web mock data and dataset quality report from text_cases.csv.

Run from the repository root:
    python scripts/build_mock_data.py
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_CSV = ROOT / "dataset" / "text_cases.csv"
REPORT_MD = ROOT / "docs" / "dataset_quality_report.md"
MOCK_JS = ROOT / "web" / "mockData.js"

REQUIRED_TYPES = [
    "fake_delivery",
    "account_lock",
    "invoice_attachment",
    "fake_prize",
    "refund_or_payment",
    "qr_phishing",
    "document_signing",
    "legitimate_security_notice",
    "legitimate_delivery_notice",
    "legitimate_it_maintenance",
]

ALL_FIELDS = [
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


def read_cases() -> list[dict]:
    with TEXT_CSV.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def duplicate_values(cases: list[dict], field: str) -> dict[str, int]:
    counter = Counter(row[field].strip() for row in cases if row.get(field, "").strip())
    return {value: count for value, count in counter.items() if count > 1}


def empty_fields(cases: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for field in ALL_FIELDS:
        counts[field] = sum(1 for row in cases if not row.get(field, "").strip())
    return {field: count for field, count in counts.items() if count}


def quality_report(cases: list[dict]) -> str:
    risk_counts = Counter(row["risk_label"] for row in cases)
    type_counts = Counter(row["phishing_type"] for row in cases)
    source_counts = Counter(row["source_type"] for row in cases)
    duplicate_subjects = duplicate_values(cases, "email_subject")
    duplicate_content = duplicate_values(cases, "email_content")
    blanks = empty_fields(cases)

    lines = [
        "# Dataset Quality Report",
        "",
        f"產生日期：{date.today().isoformat()}",
        "",
        "## 總覽",
        "",
        f"- 文字案例總筆數：{len(cases)}",
        f"- risk_label 類別數：{len(risk_counts)}",
        f"- phishing_type 類別數：{len(type_counts)}",
        "",
        "## risk_label 分布",
        "",
        "| risk_label | 筆數 |",
        "| --- | ---: |",
    ]
    for key, count in sorted(risk_counts.items()):
        lines.append(f"| {key} | {count} |")

    lines.extend(["", "## phishing_type 分布", "", "| phishing_type | 筆數 |", "| --- | ---: |"])
    for key, count in type_counts.most_common():
        lines.append(f"| {key} | {count} |")

    lines.extend(["", "## source_type 分布", "", "| source_type | 筆數 |", "| --- | ---: |"])
    for key, count in source_counts.most_common():
        lines.append(f"| {key} | {count} |")

    lines.extend(
        [
            "",
            "## 重複檢查",
            "",
            f"- 重複 email_subject 數量：{len(duplicate_subjects)}",
            f"- 重複 email_content 數量：{len(duplicate_content)}",
            "",
            "## 空欄位檢查",
            "",
        ]
    )

    if blanks:
        lines.extend(["| 欄位 | 空值筆數 |", "| --- | ---: |"])
        for field, count in blanks.items():
            lines.append(f"| {field} | {count} |")
    else:
        lines.append("- 未發現必要欄位空值。")

    lines.extend(
        [
            "",
            "## 品質結論",
            "",
            "- 已涵蓋 phishing 與 normal 類別，適合第一版互動介面展示。",
            "- 目前沒有直接保存活的惡意連結或真實個資。",
            "- 後續可補強 BEC / CEO fraud、求職詐騙、更多台灣銀行官方防詐來源與實際 demo 圖片素材。",
        ]
    )

    return "\n".join(lines) + "\n"


def risk_level(case: dict) -> str:
    if case["risk_label"] == "normal":
        return "low"
    if case["urgency_level"] == "high" or case["has_attachment"] == "true":
        return "high"
    return "medium"


def risk_score(case: dict) -> int:
    level = risk_level(case)
    if level == "low":
        base = 18
        if case["phishing_type"] == "legitimate_it_maintenance":
            return base
        return 24
    if level == "medium":
        score = 48
        if case["has_link"] == "true":
            score += 7
        if case["phishing_type"] in {"qr_phishing", "refund_or_payment"}:
            score += 6
        return min(score, 65)
    score = 78
    if case["has_attachment"] == "true":
        score += 8
    if case["has_link"] == "true":
        score += 5
    if case["urgency_level"] == "high":
        score += 4
    return min(score, 95)


def confidence(case: dict) -> float:
    if case["risk_label"] == "normal":
        return 0.82
    score = 0.74
    if case["has_link"] == "true":
        score += 0.07
    if case["has_attachment"] == "true":
        score += 0.08
    if case["urgency_level"] == "high":
        score += 0.06
    return min(score, 0.94)


def indicators(case: dict) -> list[str]:
    items: list[str] = []
    if case["has_link"] == "true":
        items.append("包含連結或導向外部頁面")
    if case["has_attachment"] == "true":
        items.append("要求開啟附件")
    if case["urgency_level"] == "high":
        items.append("使用急迫語氣")
    elif case["urgency_level"] == "medium":
        items.append("帶有時間壓力")
    keywords = [item.strip() for item in case["suspicious_keywords"].split(";") if item.strip()]
    items.extend(keywords[:3])
    if not items:
        items.append("未發現明顯高風險特徵")
    return list(dict.fromkeys(items))


def manipulation_methods(case: dict) -> list[str]:
    mapping = {
        "account_lock": ["製造帳號停用壓力", "冒充安全通知", "誘導登入驗證"],
        "fake_delivery": ["冒充物流通知", "小額付款誘導", "製造包裹退回壓力"],
        "invoice_attachment": ["商務流程壓力", "附件誘導", "偽裝帳務通知"],
        "fake_prize": ["中獎誘惑", "要求手續費", "製造名額或期限壓力"],
        "refund_or_payment": ["退款誘因", "付款資料更新誘導", "服務中斷壓力"],
        "qr_phishing": ["QR Code 導流", "繞過網址檢查", "行動裝置驗證誘導"],
        "document_signing": ["偽裝文件簽署", "機密文件誘惑", "期限壓力"],
    }
    if case["risk_label"] == "normal":
        return ["無明顯詐騙話術", "建議仍透過官方管道查證"]
    return mapping.get(case["phishing_type"], ["社交工程誘導", "冒充可信來源"])


def personal_data_risk(case: dict) -> str:
    if case["risk_label"] == "normal":
        return "目前未看到要求輸入帳號、密碼、驗證碼或身分資料的跡象。"
    if case["phishing_type"] in {"account_lock", "qr_phishing", "document_signing"}:
        return "可能誘導使用者輸入帳號、密碼、MFA 驗證碼或信箱登入資訊。"
    if case["phishing_type"] in {"fake_delivery", "fake_prize"}:
        return "可能要求姓名、電話、地址、身分資料或其他領取 / 配送資訊。"
    return "可能要求帳務、付款、公司或個人識別資料。"


def payment_risk(case: dict) -> str:
    if case["risk_label"] == "normal":
        return "目前沒有付款、退款、信用卡或轉帳要求。"
    if case["phishing_type"] in {"fake_delivery", "fake_prize", "refund_or_payment"}:
        return "可能要求小額手續費、信用卡資料、退款驗證或其他付款資訊。"
    if case["phishing_type"] == "invoice_attachment":
        return "可能利用帳務壓力誘導付款或開啟惡意附件。"
    return "目前付款風險不是主軸，但可能在後續假頁面中要求付款或金融資料。"


def safe_actions(case: dict) -> list[str]:
    if case["risk_label"] == "normal":
        return ["不要回覆任何帳密", "需要確認時自行開啟官方 App 或網站", "保留通知但不必透過信件捷徑操作"]
    actions = ["不要點擊信件中的連結或按鈕", "不要回覆帳號、密碼、驗證碼或信用卡資料", "改從官方 App、官方網站或既有客服管道查證"]
    if case["has_attachment"] == "true":
        actions.insert(1, "不要開啟未預期的附件")
    if case["phishing_type"] == "qr_phishing":
        actions.insert(1, "不要掃描信件中的不明 QR Code")
    return actions


def to_mock_sample(case: dict, index: int) -> dict:
    label = "legitimate" if case["risk_label"] == "normal" else "phishing"
    return {
        "id": f"sample-{index:03d}",
        "dataset_id": case["id"],
        "inputType": "text",
        "phishingType": case["phishing_type"],
        "title": case["email_subject"],
        "text": f"寄件者：{case['sender']} <{case['sender_domain']}>\n主旨：{case['email_subject']}\n\n{case['email_content']}",
        "result": {
            "is_phishing": case["risk_label"] != "normal",
            "label": label,
            "risk_level": risk_level(case),
            "risk_score": risk_score(case),
            "confidence_score": confidence(case),
            "indicators": indicators(case),
            "manipulation_methods": manipulation_methods(case),
            "personal_data_risk": personal_data_risk(case),
            "payment_risk": payment_risk(case),
            "safe_actions": safe_actions(case),
            "explanation_for_general_users": case["explanation"],
            "model_source": "Rule-based prototype / dataset sample",
            "disclaimer": "目前為 prototype 分析，不代表正式資安判斷。重要操作請透過官方管道查證。",
        },
    }


def select_samples(cases: list[dict]) -> list[dict]:
    by_type: dict[str, list[dict]] = defaultdict(list)
    for case in cases:
        by_type[case["phishing_type"]].append(case)

    chosen: list[dict] = []
    for type_name in REQUIRED_TYPES:
        if by_type[type_name]:
            chosen.append(by_type[type_name][0])

    # Add one extra phishing and one extra normal case for a fuller demo.
    for case in cases:
        if case["phishing_type"] == "account_lock" and case not in chosen:
            chosen.append(case)
            break
    for case in cases:
        if case["risk_label"] == "normal" and case not in chosen:
            chosen.append(case)
            break

    return chosen[:12]


def write_mock_data(samples: list[dict]) -> None:
    payload = [to_mock_sample(case, index) for index, case in enumerate(samples, start=1)]
    image_sample = {
        "id": "image-demo-001",
        "inputType": "image",
        "phishingType": "image_mock",
        "title": "圖片上傳展示案例",
        "text": "圖片分析目前為展示功能，尚未串接 OCR 或多模態模型。",
        "result": {
            "is_phishing": True,
            "label": "suspicious",
            "risk_level": "medium",
            "risk_score": 58,
            "confidence_score": 0.68,
            "indicators": ["圖片可能包含偽登入頁或付款提示", "需進一步 OCR 或多模態模型判讀", "來源與網址無法僅靠圖片確認"],
            "manipulation_methods": ["冒充官方頁面", "製造急迫感", "誘導輸入資料"],
            "personal_data_risk": "圖片可能誘導使用者輸入帳號、密碼、驗證碼或聯絡資料。",
            "payment_risk": "若圖片包含付款按鈕、QR Code 或信用卡欄位，需視為中高風險並改由官方管道確認。",
            "safe_actions": ["不要掃描不明 QR Code", "不要在圖片導向的不明頁面輸入資料", "改從官方 App 或網站查證"],
            "explanation_for_general_users": "圖片功能目前只做展示，尚未讀取圖片文字，也沒有真正判斷頁面真假。",
            "model_source": "Image mock prototype",
            "disclaimer": "圖片分析目前為展示功能，尚未串接 OCR 或多模態模型。",
        },
    }
    payload.append(image_sample)
    js = "export const mockSamples = "
    js += json.dumps(payload, ensure_ascii=False, indent=2)
    js += ";\n"
    MOCK_JS.write_text(js, encoding="utf-8")


def main() -> int:
    cases = read_cases()
    REPORT_MD.write_text(quality_report(cases), encoding="utf-8")
    write_mock_data(select_samples(cases))
    print(f"Wrote {REPORT_MD.relative_to(ROOT)}")
    print(f"Wrote {MOCK_JS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
