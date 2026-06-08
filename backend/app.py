import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse

import joblib
from flask import Flask, jsonify, request
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "phishing_model"
CLASSIFIER_PATH = MODEL_DIR / "phishing_classifier.pkl"
VECTORIZER_PATH = MODEL_DIR / "vectorizer.pkl"
METRICS_PATH = MODEL_DIR / "metrics.json"

ALLOWED_ORIGINS = os.environ.get(
    "ALLOWED_ORIGINS",
    "http://localhost:5501,http://127.0.0.1:5501,https://smallweiweihsu.github.io,https://smallweiweihsu.github.io/genai-final-anti-scam",
).split(",")

app = Flask(__name__)
CORS(app, origins=ALLOWED_ORIGINS)

STRICT_OFFICIAL_DOMAINS = {
    "gov.tw", "edu.tw", "thsrc.com.tw", "railway.gov.tw", "tra.gov.tw",
    "post.gov.tw", "cht.com.tw", "ntu.edu.tw", "ccu.edu.tw", "ncku.edu.tw",
    "nthu.edu.tw", "nycu.edu.tw", "ncu.edu.tw", "ntust.edu.tw", "ntnu.edu.tw",
    "bot.com.tw", "landbank.com.tw", "firstbank.com.tw", "huananbank.com.tw",
    "esunbank.com", "cathaybk.com.tw", "ctbcbank.com", "taishinbank.com.tw",
    "fubon.com", "fubon.com.tw", "megabank.com.tw", "sinopac.com.tw",
}

TRUSTED_SERVICE_DOMAINS = {
    "momo.com.tw", "pchome.com.tw", "shopee.tw", "books.com.tw",
    "ruten.com.tw", "yahoo.com", "google.com", "microsoft.com",
    "apple.com", "paypal.com", "ibon.com.tw", "ticket.com.tw",
}

SHORT_URL_DOMAINS = {
    "bit.ly", "tinyurl.com", "reurl.cc", "lihi.cc", "ppt.cc", "goo.gl", "t.co"
}

classifier = None
vectorizer = None
metrics = {}
model_load_error = None


def load_model():
    global classifier, vectorizer, metrics, model_load_error

    missing = []
    for path in [CLASSIFIER_PATH, VECTORIZER_PATH]:
        if not path.exists():
            missing.append(str(path.relative_to(BASE_DIR)))

    if missing:
        model_load_error = f"Missing model files: {', '.join(missing)}"
        return

    try:
        classifier = joblib.load(CLASSIFIER_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)

        if METRICS_PATH.exists():
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                metrics = json.load(f)

        model_load_error = None
    except Exception as exc:
        classifier = None
        vectorizer = None
        model_load_error = str(exc)


def extract_urls(text):
    return re.findall(r"https?://[^\s<>()\"']+", text or "")


def extract_domain(value):
    if not value:
        return ""

    value = str(value).strip()

    if "@" in value and not value.lower().startswith(("http://", "https://")):
        value = value.rsplit("@", 1)[-1]

    if not value.lower().startswith(("http://", "https://")):
        value = "https://" + value

    try:
        parsed = urlparse(value)
        domain = (parsed.hostname or "").lower().strip().rstrip(".")
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except Exception:
        return ""


def domain_matches(domain, allowed_domains):
    if not domain:
        return []

    domain = str(domain).lower().strip().rstrip(".")
    matched = []
    for allowed in allowed_domains:
        allowed = str(allowed).lower().strip().rstrip(".")
        if domain == allowed or domain.endswith("." + allowed):
            matched.append(allowed)
    return matched


def get_sender_domain(sender):
    return extract_domain(sender)


def get_url_domains(text):
    return sorted({extract_domain(url) for url in extract_urls(text) if extract_domain(url)})


def has_domain_mismatch(sender_domain, url_domains):
    if not sender_domain or not url_domains:
        return False

    for url_domain in url_domains:
        if sender_domain == url_domain:
            return False
        if sender_domain.endswith("." + url_domain) or url_domain.endswith("." + sender_domain):
            return False

    return True


def analyze_rule_indicators(text, sender_domain, url_domains):
    lower = (text or "").lower()
    indicators = []
    methods = []
    strong = []

    if any(k in lower for k in ["立即", "馬上", "限時", "24小時", "24 小時", "緊急", "urgent", "immediately"]):
        indicators.append("急迫語氣")
        methods.append("製造急迫感")

    if any(k in lower for k in ["停用", "凍結", "鎖定", "異常登入", "suspend", "suspended", "locked"]):
        indicators.append("帳戶威脅")
        methods.append("威脅帳戶停用")
        strong.append("帳戶停用威脅")

    if any(k in lower for k in ["密碼", "驗證碼", "信用卡", "身分證", "帳號密碼", "password", "credit card"]):
        indicators.append("敏感資料要求")
        methods.append("要求提供敏感資料")
        strong.append("敏感資料要求")

    if any(k in lower for k in ["點擊", "點選", "登入連結", "完成驗證", "click here", "verify your account"]):
        indicators.append("連結誘導")
        methods.append("誘導點擊或重新登入")

    if any(k in lower for k in ["中獎", "退款", "補助", "禮品", "reward", "refund", "bonus", "prize"]):
        indicators.append("獎勵或退款話術")
        methods.append("利用獎勵誘因")

    if any(domain_matches(d, SHORT_URL_DOMAINS) for d in url_domains):
        indicators.append("可疑短網址")
        methods.append("使用短網址隱藏目的地")
        strong.append("可疑短網址")

    return list(dict.fromkeys(indicators)), list(dict.fromkeys(methods)), list(dict.fromkeys(strong))


def get_phishing_probability(features):
    if not hasattr(classifier, "predict_proba"):
        pred = classifier.predict(features)[0]
        return 0.9 if str(pred).lower() in ["1", "phishing"] else 0.1

    probs = classifier.predict_proba(features)[0]
    classes = list(classifier.classes_)

    phishing_index = None
    for i, cls in enumerate(classes):
        if str(cls).lower() in ["1", "phishing", "spam"]:
            phishing_index = i
            break

    if phishing_index is None:
        phishing_index = len(classes) - 1

    return float(probs[phishing_index])


def build_response(subject, sender, body):
    text = f"主旨：{subject}\n寄件者：{sender}\n內容：{body}"
    features = vectorizer.transform([text])

    prediction = classifier.predict(features)[0]
    phishing_probability = get_phishing_probability(features)

    label = "phishing" if str(prediction).lower() in ["1", "phishing", "spam"] else "legitimate"
    is_phishing = label == "phishing"

    sender_domain = get_sender_domain(sender)
    url_domains = get_url_domains(text)
    domain_mismatch = has_domain_mismatch(sender_domain, url_domains)

    matched_official = []
    matched_trusted = []

    for domain in [sender_domain] + url_domains:
        matched_official.extend(domain_matches(domain, STRICT_OFFICIAL_DOMAINS))
        matched_trusted.extend(domain_matches(domain, TRUSTED_SERVICE_DOMAINS))

    matched_official = sorted(set(matched_official))
    matched_trusted = sorted(set(matched_trusted))

    indicators, methods, strong = analyze_rule_indicators(text, sender_domain, url_domains)

    if domain_mismatch:
        indicators.append("寄件者與連結網域不一致")
        strong.append("寄件者與 URL 網域不一致")

    strong = list(dict.fromkeys(strong))
    has_short_url = any(domain_matches(domain, SHORT_URL_DOMAINS) for domain in url_domains)
    has_trusted_domain = bool(matched_official or matched_trusted)
    risk_score = round(phishing_probability * 100)
    postprocess_notes = []

    if strong:
        postprocess_notes.append(f"偵測到強危險特徵：{', '.join(strong)}，不套用可信網域降權。")
    if domain_mismatch:
        postprocess_notes.append("寄件者網域與連結網域不一致，不套用可信網域降權。")
    if has_short_url:
        postprocess_notes.append("信件含短網址，不套用可信網域降權。")

    can_trusted_downgrade = (
        not is_phishing
        and phishing_probability < 0.5
        and has_trusted_domain
        and not strong
        and not domain_mismatch
        and not has_short_url
    )
    official_informational_message = (
        bool(matched_official)
        and not url_domains
        and not strong
        and not domain_mismatch
        and not has_short_url
        and not any(k in text.lower() for k in ["登入", "下載", "附件", "密碼", "驗證碼", "信用卡", "付款", "繳費", "verify", "password", "download"])
    )

    if official_informational_message:
        risk_score = min(risk_score, 25)
        postprocess_notes.append("寄件者為解析後完全符合的官方/教育網域，且內容無連結、無強危險特徵、無敏感操作要求；判定為資訊型通知並降為低風險。")
    elif phishing_probability >= 0.7 or is_phishing:
        risk_score = max(risk_score, 70)
        postprocess_notes.append("模型判定為 phishing 或 phishing_probability >= 0.7，因此維持高風險且不套用可信網域降權。")
    elif 0.4 <= phishing_probability < 0.7:
        risk_score = max(risk_score, 40)
        if can_trusted_downgrade:
            risk_score = max(25, min(risk_score, 45 if matched_official else 55))
            postprocess_notes.append("模型機率為中等且命中解析後的可信官方網域、無強危險特徵、無網域不一致、無短網址，因此僅有限降權。")
        elif has_trusted_domain:
            postprocess_notes.append("雖命中可信網域，但因模型機率不低或存在其他風險條件，未降到低風險。")
        else:
            postprocess_notes.append("未命中可信網域且 phishing_probability 為中等，維持中風險。")
    else:
        if strong or domain_mismatch or has_short_url:
            risk_score = max(risk_score, 40)
            postprocess_notes.append("雖 phishing_probability 較低，但存在強危險特徵、網域不一致或短網址，至少維持中風險。")
        elif can_trusted_downgrade:
            risk_score = min(risk_score, 25)
            postprocess_notes.append("命中解析後的可信官方網域且無強危險特徵、無網域不一致、無短網址，因此降為低風險。")
        else:
            risk_score = min(risk_score, 39)
            if has_trusted_domain:
                postprocess_notes.append("命中可信網域，但未完全符合降權條件，僅依模型低機率維持低風險。")
            else:
                postprocess_notes.append("phishing_probability 較低且未偵測強危險特徵，維持低風險；未因未列名網域額外降權。")

    if risk_score >= 70:
        risk_level = "high"
        risk_level_zh = "高風險"
    elif risk_score >= 40:
        risk_level = "medium"
        risk_level_zh = "中風險"
    else:
        risk_level = "low"
        risk_level_zh = "低風險"

    confidence_score = round(max(phishing_probability, 1 - phishing_probability), 4)

    personal_data_risk = "內容可能要求輸入密碼、驗證碼、信用卡或身分證等敏感資料。" if "敏感資料要求" in indicators else "目前未明顯要求敏感個資，但仍建議查證。"
    payment_risk = "若提供信用卡或帳號資料，可能產生金錢或帳戶被盜用風險。" if any(k in text for k in ["付款", "信用卡", "繳費", "帳戶"]) else "目前未明顯出現付款風險。"

    safe_actions = [
        "不要直接點擊信件中的連結",
        "改從官方網站或官方 App 登入查證",
        "確認寄件者網域與官方客服資訊",
        "不要提供密碼、驗證碼、信用卡或身分證資料",
    ]

    explanation = f"此信件被判定為{risk_level_zh}。"
    if matched_official or matched_trusted:
        explanation += " 系統偵測到可信或常見服務網域，但這不是絕對安全保證，仍需配合內容與連結檢查。"
    if strong:
        explanation += " 因內容包含強危險特徵，所以未直接降權。"

    return {
        "is_phishing": is_phishing,
        "label": label,
        "risk_level": risk_level,
        "risk_level_zh": risk_level_zh,
        "risk_score": risk_score,
        "confidence_score": confidence_score,
        "phishing_probability": round(phishing_probability, 4),
        "indicators": list(dict.fromkeys(indicators)),
        "manipulation_methods": list(dict.fromkeys(methods)),
        "personal_data_risk": personal_data_risk,
        "payment_risk": payment_risk,
        "safe_actions": safe_actions,
        "explanation_for_general_users": explanation,
        "urls": extract_urls(text),
        "sender_domain": sender_domain,
        "url_domains": url_domains,
        "matched_official_domains": matched_official,
        "matched_trusted_domains": matched_trusted,
        "domain_mismatch": domain_mismatch,
        "postprocess_notes": postprocess_notes,
        "model_source": "TF-IDF + Logistic Regression phishing email model",
        "metrics": metrics,
        "disclaimer": "此結果僅供輔助判斷，重要操作請透過官方網站、官方 App 或客服管道查證。",
    }


load_model()


@app.get("/")
def health_check():
    return jsonify({
        "status": "ok",
        "model_loaded": classifier is not None and vectorizer is not None,
        "model_error": model_load_error,
        "error": model_load_error,
    })


@app.post("/api/analyze-email")
def analyze_email():
    if classifier is None or vectorizer is None:
        return jsonify({
            "error": "model_unavailable",
            "model_loaded": False,
            "model_error": model_load_error,
            "required_files": [
                "phishing_model/phishing_classifier.pkl",
                "phishing_model/vectorizer.pkl",
                "phishing_model/metrics.json",
            ],
        }), 503

    data = request.get_json(silent=True) or {}

    subject = data.get("subject", "")
    sender = data.get("sender", "")
    body = data.get("body", "")

    if not body and data.get("text"):
        body = data.get("text", "")

    result = build_response(subject, sender, body)
    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
