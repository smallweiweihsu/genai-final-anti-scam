import json
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
=======
import os
>>>>>>> theirs
=======
import os
>>>>>>> theirs
=======
import os
>>>>>>> theirs
=======
import os
>>>>>>> theirs
=======
import os
>>>>>>> theirs
=======
import os
>>>>>>> theirs
import re
from pathlib import Path
from urllib.parse import urlparse

import joblib
from flask import Flask, jsonify, request
from flask_cors import CORS

<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours

=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "phishing_model"
CLASSIFIER_PATH = MODEL_DIR / "phishing_classifier.pkl"
VECTORIZER_PATH = MODEL_DIR / "vectorizer.pkl"
METRICS_PATH = MODEL_DIR / "metrics.json"

<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
MODEL_SOURCE = "TF-IDF + Logistic Regression phishing email model"
DISCLAIMER = "此結果僅供輔助判斷，重要操作請透過官方網站、官方 App 或客服管道查證。"

app = Flask(__name__)
CORS(app)

model = None
vectorizer = None
metrics = None
model_error = None


RULES = {
    "急迫語氣": {
        "keywords": ["立即", "馬上", "立刻", "限時", "24小時", "24 小時", "逾期", "緊急", "urgent", "immediately"],
        "method": "製造急迫感",
    },
    "帳戶威脅": {
        "keywords": ["停用", "凍結", "鎖定", "異常登入", "停權", "blocked", "locked", "suspend"],
        "method": "威脅帳戶權益",
    },
    "個資要求": {
        "keywords": ["密碼", "驗證碼", "信用卡", "身分證", "帳號密碼", "password", "credit card", "verification code"],
        "method": "要求提供敏感資料",
    },
    "連結誘導": {
        "keywords": ["點擊", "點選", "登入連結", "重新登入", "完成驗證", "http://", "https://", "click here", "verify your account"],
        "method": "誘導點擊或重新登入",
    },
    "獎勵退款": {
        "keywords": ["中獎", "退款", "補助", "禮品", "現金回饋", "reward", "refund", "bonus", "prize"],
        "method": "以獎勵或退款吸引操作",
    },
}

STRICT_OFFICIAL_DOMAINS = {
    "gov.tw",
    "e.gov.tw",
    "nat.gov.tw",
    "mof.gov.tw",
    "nta.gov.tw",
    "npa.gov.tw",
    "moi.gov.tw",
    "motc.gov.tw",
    "mvdis.gov.tw",
    "nhi.gov.tw",
    "mol.gov.tw",
    "epa.gov.tw",
    "cwa.gov.tw",
    "cdc.gov.tw",
    "fda.gov.tw",
    "taiwan.gov.tw",
    "edu.tw",
    "ntu.edu.tw",
    "nthu.edu.tw",
    "nycu.edu.tw",
    "ncku.edu.tw",
    "ncu.edu.tw",
    "nsysu.edu.tw",
    "ntust.edu.tw",
    "ntnu.edu.tw",
    "ccu.edu.tw",
    "nchu.edu.tw",
    "tmu.edu.tw",
    "cgu.edu.tw",
    "mail.edu.tw",
    "thsrc.com.tw",
    "railway.gov.tw",
    "tra.gov.tw",
    "taiwanbus.tw",
    "taiwantrip.com.tw",
    "metro.taipei",
    "tmrt.com.tw",
    "tymetro.com.tw",
    "krtc.com.tw",
    "post.gov.tw",
    "chunghwapost.com.tw",
    "t-cat.com.tw",
    "hct.com.tw",
    "kerrytj.com",
    "blackcat.com.tw",
    "bot.com.tw",
    "landbank.com.tw",
    "firstbank.com.tw",
    "huananbank.com.tw",
    "esunbank.com",
    "cathaybk.com.tw",
    "ctbcbank.com",
    "taishinbank.com.tw",
    "fubon.com",
    "fubon.com.tw",
    "megabank.com.tw",
    "sinopac.com",
    "sinopac.com.tw",
    "yuantabank.com.tw",
    "scsb.com.tw",
    "tcb-bank.com.tw",
    "linebank.com.tw",
    "rakuten-bank.com.tw",
    "cht.com.tw",
    "emome.net",
    "fetnet.net",
    "taiwanmobile.com",
    "twmsolution.com",
    "gt4g.tw",
}

TRUSTED_SERVICE_DOMAINS = {
    "ibon.com.tw",
    "ticket.com.tw",
    "momo.com.tw",
    "pchome.com.tw",
    "shopee.tw",
    "books.com.tw",
    "ruten.com.tw",
    "yahoo.com",
    "google.com",
    "microsoft.com",
    "apple.com",
    "paypal.com",
=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
ALLOWED_ORIGINS = os.environ.get(
    "ALLOWED_ORIGINS",
    "http://localhost:5501,http://127.0.0.1:5501",
).split(",")

app = Flask(__name__)
CORS(app, origins=ALLOWED_ORIGINS)

classifier = None
vectorizer = None
metrics = None
model_load_error = None

TRUSTED_DOMAINS = {
    "apple.com",
    "google.com",
    "microsoft.com",
    "office.com",
    "outlook.com",
    "paypal.com",
    "amazon.com",
    "shopee.tw",
    "gov.tw",
    "edu.tw",
    "post.gov.tw",
    "cht.com.tw",
    "twca.com.tw",
}

OFFICIAL_DOMAIN_KEYWORDS = {
    "apple": ["apple.com"],
    "google": ["google.com"],
    "microsoft": ["microsoft.com", "office.com", "outlook.com"],
    "paypal": ["paypal.com"],
    "amazon": ["amazon.com"],
    "shopee": ["shopee.tw"],
    "中華郵政": ["post.gov.tw"],
    "郵局": ["post.gov.tw"],
    "政府": ["gov.tw"],
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
}

SHORT_URL_DOMAINS = {
    "bit.ly",
    "tinyurl.com",
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
    "reurl.cc",
    "lihi.cc",
    "ppt.cc",
    "goo.gl",
    "t.co",
}

SENSITIVE_DATA_KEYWORDS = [
    "密碼",
    "驗證碼",
    "信用卡",
    "身分證",
    "帳號密碼",
    "password",
    "credit card",
    "verification code",
]

PAYMENT_HINT_KEYWORDS = ["付款", "繳費", "帳單", "票款", "扣款", "payment", "invoice", "bill"]
TIME_LIMIT_HINT_KEYWORDS = ["期限", "截止", "限時", "逾期", "24小時", "24 小時", "deadline", "expire"]


def load_artifacts():
    global model, vectorizer, metrics, model_error

    missing = []
    if not CLASSIFIER_PATH.exists():
        missing.append(str(CLASSIFIER_PATH.relative_to(BASE_DIR)))
    if not VECTORIZER_PATH.exists():
        missing.append(str(VECTORIZER_PATH.relative_to(BASE_DIR)))

    if missing:
        model_error = "Missing model artifact(s): " + ", ".join(missing)
        return

    try:
        model = joblib.load(CLASSIFIER_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
        if METRICS_PATH.exists():
            with METRICS_PATH.open("r", encoding="utf-8") as file:
                metrics = json.load(file)
        model_error = None
    except Exception as exc:
        model = None
        vectorizer = None
        metrics = None
        model_error = f"Failed to load model artifacts: {exc}"


def normalize_label(value):
    return str(value).strip().lower()


def is_phishing_label(value):
    normalized = normalize_label(value)
    return normalized in {"1", "phishing", "scam", "suspicious", "malicious"}


def phishing_class_index(classes):
    if classes is None:
        return None

    normalized_classes = [normalize_label(item) for item in classes]
    for target in ("phishing", "scam", "suspicious", "malicious", "1"):
        if target in normalized_classes:
            return normalized_classes.index(target)
    return None


def build_email_text(subject, sender, body):
    return f"主旨：{subject}\n寄件者：{sender}\n內容：{body}".strip()


def extract_domain(value):
    if not value:
        return ""

    candidate = str(value).strip().lower()
    if "@" in candidate and not candidate.startswith(("http://", "https://")):
        candidate = candidate.rsplit("@", 1)[1]

    if not candidate.startswith(("http://", "https://")):
        candidate = "https://" + candidate

    parsed = urlparse(candidate)
    domain = parsed.hostname or ""
    return domain.strip(".").lower()


def extract_urls(text):
    return re.findall(r"https?://[^\s<>'\")]+", text, flags=re.IGNORECASE)


def domain_matches(domain, allowed_domains):
    normalized_domain = extract_domain(domain)
    if not normalized_domain:
        return False
    return any(
        normalized_domain == allowed_domain or normalized_domain.endswith("." + allowed_domain)
        for allowed_domain in allowed_domains
    )


def get_sender_domain(sender):
    return extract_domain(sender)


def get_url_domains(text):
    return list(dict.fromkeys(
        domain
        for domain in (extract_domain(url) for url in extract_urls(text))
        if domain
    ))


def matched_domains(domains, allowed_domains):
    return sorted({
        domain
        for domain in domains
        if domain_matches(domain, allowed_domains)
    })


def has_strong_risk_indicators(text, urls):
    lowered = text.lower()
    strong_indicators = []

    if any(keyword.lower() in lowered for keyword in SENSITIVE_DATA_KEYWORDS):
        strong_indicators.append("敏感資料要求")

    if any(domain_matches(extract_domain(url), SHORT_URL_DOMAINS) for url in urls):
        strong_indicators.append("可疑短網址")

    return strong_indicators


def has_domain_mismatch(sender_domain, url_domains):
    if not sender_domain or not url_domains:
        return False

    allowed = {sender_domain}
    parent_matches = [
        url_domain
        for url_domain in url_domains
        if domain_matches(url_domain, allowed) or domain_matches(sender_domain, {url_domain})
    ]
    return len(parent_matches) == 0


def analyze_rules(text):
    lowered = text.lower()
    indicators = []
    methods = []

    for indicator, config in RULES.items():
        if any(keyword.lower() in lowered for keyword in config["keywords"]):
            indicators.append(indicator)
            methods.append(config["method"])

    return indicators, list(dict.fromkeys(methods))


def risk_level_from_score(score):
    if score >= 70:
        return "high", "高風險"
    if score >= 40:
        return "medium", "中風險"
    return "low", "低風險"


def describe_personal_data_risk(indicators):
    if "個資要求" in indicators:
        return "內容可能要求輸入密碼、驗證碼、信用卡或身分證等敏感資料。"
    if "連結誘導" in indicators:
        return "內容可能透過連結引導到假登入頁，進一步取得帳號或個資。"
    return "目前未偵測到明確的個資索取語句，但仍建議確認寄件者與網址。"


def describe_payment_risk(indicators):
    if "獎勵退款" in indicators:
        return "內容提到退款、補助或獎勵，可能誘導後續付款、提供金融資料或收取手續費。"
    if "個資要求" in indicators:
        return "若提供信用卡或帳號資料，可能產生盜刷或帳戶被盜用風險。"
    return "目前未直接偵測到付款要求。"


def build_safe_actions(indicators, is_phishing):
    actions = ["不要直接點擊信件中的連結", "改從官方網站或官方 App 登入查證", "確認寄件者網域與官方客服資訊"]
    if "個資要求" in indicators:
        actions.append("不要提供密碼、驗證碼、信用卡或身分證資料")
    if "帳戶威脅" in indicators:
        actions.append("不要因帳戶停用或凍結威脅而急著操作")
    if is_phishing:
        actions.append("可將信件回報給公司資安窗口或郵件服務供應商")
    return list(dict.fromkeys(actions))


def build_explanation(indicators, risk_level_zh):
    if indicators:
        joined = "、".join(indicators)
        return f"這封信被判定為{risk_level_zh}，主要因為內容出現「{joined}」等特徵。請先離開信件，改用官方管道查證。"
    return f"這封信目前被判定為{risk_level_zh}。即使沒有明顯話術，仍建議確認寄件者、網址與信件脈絡。"


def add_unique(items, item):
    if item and item not in items:
        items.append(item)


def add_domain_context_indicators(result, text, matched_official, matched_trusted):
    lowered = text.lower()
    if matched_official:
        add_unique(result["indicators"], "官方網域")
    if matched_trusted:
        add_unique(result["indicators"], "可信候選網域")
    if any(keyword.lower() in lowered for keyword in PAYMENT_HINT_KEYWORDS):
        add_unique(result["indicators"], "付款資訊")
    if any(keyword.lower() in lowered for keyword in TIME_LIMIT_HINT_KEYWORDS):
        add_unique(result["indicators"], "時間限制")


def apply_risk_postprocessing(result, subject, sender, body):
    text = build_email_text(subject, sender, body)
    urls = extract_urls(text)
    sender_domain = get_sender_domain(sender)
    url_domains = get_url_domains(text)
    all_domains = list(dict.fromkeys([domain for domain in [sender_domain, *url_domains] if domain]))
    matched_official = matched_domains(all_domains, STRICT_OFFICIAL_DOMAINS)
    matched_trusted = matched_domains(all_domains, TRUSTED_SERVICE_DOMAINS)
    strong_risk_indicators = has_strong_risk_indicators(text, urls)
    domain_mismatch = has_domain_mismatch(sender_domain, url_domains)
    postprocess_notes = []

    result["sender_domain"] = sender_domain
    result["url_domains"] = url_domains
    result["matched_official_domains"] = matched_official
    result["matched_trusted_domains"] = matched_trusted
    result["domain_mismatch"] = domain_mismatch
    result["postprocess_notes"] = postprocess_notes

    add_domain_context_indicators(result, text, matched_official, matched_trusted)

    for indicator in strong_risk_indicators:
        add_unique(result["indicators"], indicator)
    if domain_mismatch:
        add_unique(result["indicators"], "寄件者與連結網域不一致")
        postprocess_notes.append("寄件者網域與信件中的連結網域不一致，因此不套用可信網域降權。")

    if strong_risk_indicators:
        postprocess_notes.append("偵測到強危險特徵：" + "、".join(strong_risk_indicators) + "，因此不套用可信網域降權。")

    if result["label"] == "phishing":
        if matched_official or matched_trusted:
            result["explanation_for_general_users"] += " 信中出現看似官方或常見服務的網域，但模型仍判斷風險偏高，建議確認寄件者與實際連結是否一致。"
            postprocess_notes.append("模型已判定 phishing，可信網域只作為說明提示，不降低風險。")
        return result

    can_lower_risk = not strong_risk_indicators and not domain_mismatch
    if matched_official and can_lower_risk:
        result["risk_score"] = min(result["risk_score"], 35)
        result["risk_level"] = "low"
        result["risk_level_zh"] = "低風險"
        result["explanation_for_general_users"] = (
            "此信件較接近正常官方或公共服務通知。雖然包含連結、付款期限或系統通知，"
            "但寄件者或連結網域與可信官方服務相符，因此最終風險降低。仍建議從官方 App 或官方網站確認。"
        )
        postprocess_notes.append("命中嚴格可信官方網域，且模型判定 legitimate、未偵測強危險特徵，risk_score 上限調整為 35。")
    elif matched_trusted and can_lower_risk:
        result["risk_score"] = min(result["risk_score"], 45)
        result["risk_level"], result["risk_level_zh"] = risk_level_from_score(result["risk_score"])
        result["explanation_for_general_users"] = (
            "此信件較接近常見服務通知，但商業平台也常被仿冒，仍建議不要直接點擊信件中的連結，"
            "改從官方 App 或官方網站查詢。"
        )
        postprocess_notes.append("命中可信候選服務網域，且模型判定 legitimate、未偵測強危險特徵，risk_score 上限調整為 45。")
    elif matched_official or matched_trusted:
        postprocess_notes.append("命中可信網域，但因強危險特徵或網域不一致，未進行風險降權。")
    else:
        postprocess_notes.append("未命中可信網域提示，沿用模型風險分數。")

    result["is_phishing"] = result["label"] == "phishing"
    return result


def predict_phishing_probability(email_text):
    if model is None or vectorizer is None:
        raise RuntimeError(model_error or "Model artifacts are not loaded.")

    features = vectorizer.transform([email_text])
    predicted_label = model.predict(features)[0]
    predicted_is_phishing = is_phishing_label(predicted_label)

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(features)[0]
        index = phishing_class_index(getattr(model, "classes_", None))
        if index is not None and index < len(probabilities):
            return float(probabilities[index]), predicted_is_phishing

        predicted_index = phishing_class_index([predicted_label])
        if predicted_index is not None:
            return float(max(probabilities)), predicted_is_phishing
        return float(1 - max(probabilities)), predicted_is_phishing

    return (0.9 if predicted_is_phishing else 0.1), predicted_is_phishing


def build_response(subject, sender, body, phishing_probability, predicted_is_phishing):
    email_text = build_email_text(subject, sender, body)
    indicators, manipulation_methods = analyze_rules(email_text)
    risk_score = int(round(phishing_probability * 100))
    risk_level, risk_level_zh = risk_level_from_score(risk_score)
    is_phishing = bool(predicted_is_phishing)

    result = {
        "is_phishing": is_phishing,
        "label": "phishing" if is_phishing else "legitimate",
        "risk_level": risk_level,
        "risk_level_zh": risk_level_zh,
        "risk_score": risk_score,
        "confidence_score": round(max(phishing_probability, 1 - phishing_probability), 4),
        "phishing_probability": round(phishing_probability, 4),
        "indicators": indicators,
        "manipulation_methods": manipulation_methods,
        "personal_data_risk": describe_personal_data_risk(indicators),
        "payment_risk": describe_payment_risk(indicators),
        "safe_actions": build_safe_actions(indicators, is_phishing),
        "explanation_for_general_users": build_explanation(indicators, risk_level_zh),
        "urls": extract_urls(email_text),
        "model_source": MODEL_SOURCE,
        "disclaimer": DISCLAIMER,
    }
    return apply_risk_postprocessing(result, subject, sender, body)
=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
    "t.co",
    "goo.gl",
    "reurl.cc",
    "is.gd",
    "ow.ly",
    "buff.ly",
    "cutt.ly",
    "shorturl.at",
}

URL_PATTERN = re.compile(r"https?://[^\s<>'\")]+", re.IGNORECASE)
EMAIL_PATTERN = re.compile(r"[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})", re.IGNORECASE)


def load_model_artifacts():
    """Load model files once at startup and keep a readable error if unavailable."""
    global classifier, vectorizer, metrics, model_load_error

    missing_files = [
        str(path.relative_to(BASE_DIR))
        for path in (CLASSIFIER_PATH, VECTORIZER_PATH, METRICS_PATH)
        if not path.exists()
    ]
    if missing_files:
        model_load_error = "Missing model artifact(s): " + ", ".join(missing_files)
        return

    try:
        classifier = joblib.load(CLASSIFIER_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
        with METRICS_PATH.open("r", encoding="utf-8") as metrics_file:
            metrics = json.load(metrics_file)
        model_load_error = None
    except Exception as exc:  # Model artifacts can be corrupted or incompatible.
        classifier = None
        vectorizer = None
        metrics = None
        model_load_error = f"Failed to load model artifact(s): {exc}"


def normalize_domain(domain):
    domain = (domain or "").strip().lower().rstrip(".")
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def is_domain_or_subdomain(domain, expected_domain):
    domain = normalize_domain(domain)
    expected_domain = normalize_domain(expected_domain)
    return domain == expected_domain or domain.endswith(f".{expected_domain}")


def extract_urls(text):
    return URL_PATTERN.findall(text or "")


def extract_domains_from_urls(urls):
    domains = []
    for url in urls:
        parsed = urlparse(url)
        if parsed.netloc:
            domains.append(normalize_domain(parsed.netloc.split("@").pop().split(":")[0]))
    return domains


def extract_sender_domain(sender):
    match = EMAIL_PATTERN.search(sender or "")
    if match:
        return normalize_domain(match.group(1))
    parsed = urlparse(sender or "")
    if parsed.netloc:
        return normalize_domain(parsed.netloc)
    return ""


<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
def has_trusted_domain(sender_domain, link_domains):
    domains = [sender_domain, *link_domains]
    return any(
        is_domain_or_subdomain(domain, trusted_domain)
        for domain in domains
        for trusted_domain in TRUSTED_DOMAINS
    )
=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
def get_matched_trusted_domains(sender_domain, link_domains):
    domains = [domain for domain in [sender_domain, *link_domains] if domain]
    matched = {
        trusted_domain
        for domain in domains
        for trusted_domain in TRUSTED_DOMAINS
        if is_domain_or_subdomain(domain, trusted_domain)
    }
    return sorted(matched)


def has_trusted_domain(sender_domain, link_domains):
    return bool(get_matched_trusted_domains(sender_domain, link_domains))
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs


def find_official_domain_matches(text, sender_domain, link_domains):
    text_lower = (text or "").lower()
    matched_brands = []
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
=======
    matched_official_domains = set()
>>>>>>> theirs
=======
    matched_official_domains = set()
>>>>>>> theirs
=======
    matched_official_domains = set()
>>>>>>> theirs
    mismatches = []

    for keyword, official_domains in OFFICIAL_DOMAIN_KEYWORDS.items():
        if keyword.lower() not in text_lower:
            continue
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
        matched_brands.append(keyword)
        observed_domains = [domain for domain in [sender_domain, *link_domains] if domain]
        if not observed_domains:
            continue
        if not any(
            is_domain_or_subdomain(domain, official_domain)
            for domain in observed_domains
            for official_domain in official_domains
        ):
=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs

        matched_brands.append(keyword)
        observed_domains = [domain for domain in [sender_domain, *link_domains] if domain]
        observed_official_domains = {
            official_domain
            for domain in observed_domains
            for official_domain in official_domains
            if is_domain_or_subdomain(domain, official_domain)
        }
        matched_official_domains.update(observed_official_domains)

        if observed_domains and not observed_official_domains:
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
            mismatches.append(
                {
                    "brand": keyword,
                    "expected_domains": official_domains,
                    "observed_domains": observed_domains,
                }
            )

<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
    return matched_brands, mismatches
=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
    return matched_brands, sorted(matched_official_domains), mismatches


def get_risk_level_zh(risk_score):
    if risk_score >= 70:
        return "高風險"
    if risk_score >= 40:
        return "中風險"
    return "低風險"


def build_user_facing_fields(combined_text, phishing_probability, risk_score, postprocessed):
    text_lower = (combined_text or "").lower()
    indicators = []
    manipulation_methods = []
    safe_actions = [
        "不要直接點擊信件中的連結或短網址。",
        "改由官方網站、官方 App 或客服電話查證。",
        "不要在可疑頁面輸入密碼、驗證碼或信用卡資料。",
    ]

    if postprocessed["short_urls"]:
        indicators.append("偵測到短網址，可能隱藏真實目的地。")
    if postprocessed["domain_mismatch"]:
        indicators.append("信件提到官方品牌，但寄件者或連結網域不一致。")
    if postprocessed["matched_trusted_domains"]:
        indicators.append("偵測到常見可信或官方網域。")
    if any(keyword in text_lower for keyword in ["urgent", "immediately", "立即", "24 小時", "停用", "鎖定"]):
        manipulation_methods.append("製造急迫感，要求使用者立刻行動。")
    if any(keyword in text_lower for keyword in ["verify", "login", "password", "驗證", "登入", "密碼", "帳戶"]):
        indicators.append("內容要求帳戶登入或驗證。")
    if any(keyword in text_lower for keyword in ["payment", "credit card", "付款", "信用卡", "退款", "銀行"]):
        indicators.append("內容涉及付款、退款或金融資料。")

    if not indicators:
        indicators.append("未偵測到明顯高風險特徵，但仍建議透過官方管道確認重要通知。")
    if not manipulation_methods:
        manipulation_methods.append("未偵測到明顯情緒操弄話術。")

    personal_data_risk = any(
        keyword in text_lower
        for keyword in ["password", "verification code", "otp", "密碼", "驗證碼", "身分證", "個資", "帳戶"]
    )
    payment_risk = any(
        keyword in text_lower
        for keyword in ["payment", "credit card", "bank", "付款", "信用卡", "銀行", "匯款", "退款"]
    )

    risk_level_zh = get_risk_level_zh(risk_score)
    explanation_for_general_users = (
        f"系統判定此信件為{risk_level_zh}。模型原始釣魚機率約為 "
        f"{round(phishing_probability * 100)}%，並依短網址、官方網域一致性與可信網域等訊號"
        "調整成使用者可讀的最終風險分數。"
    )

    return {
        "risk_level_zh": risk_level_zh,
        "confidence_score": max(phishing_probability, 1 - phishing_probability),
        "indicators": indicators,
        "manipulation_methods": manipulation_methods,
        "personal_data_risk": personal_data_risk,
        "payment_risk": payment_risk,
        "safe_actions": safe_actions,
        "explanation_for_general_users": explanation_for_general_users,
    }
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs


def postprocess_risk(phishing_probability, subject, sender, body):
    combined_text = "\n".join([subject or "", sender or "", body or ""])
    urls = extract_urls(combined_text)
    link_domains = extract_domains_from_urls(urls)
    sender_domain = extract_sender_domain(sender)
    short_url_domains = [domain for domain in link_domains if domain in SHORT_URL_DOMAINS]
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
    official_brand_mentions, domain_mismatches = find_official_domain_matches(
=======
    official_brand_mentions, matched_official_domains, domain_mismatches = find_official_domain_matches(
>>>>>>> theirs
=======
    official_brand_mentions, matched_official_domains, domain_mismatches = find_official_domain_matches(
>>>>>>> theirs
=======
    official_brand_mentions, matched_official_domains, domain_mismatches = find_official_domain_matches(
>>>>>>> theirs
        combined_text,
        sender_domain,
        link_domains,
    )
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
    trusted_domain_detected = has_trusted_domain(sender_domain, link_domains)
=======
    matched_trusted_domains = get_matched_trusted_domains(sender_domain, link_domains)
    trusted_domain_detected = bool(matched_trusted_domains)
>>>>>>> theirs
=======
    matched_trusted_domains = get_matched_trusted_domains(sender_domain, link_domains)
    trusted_domain_detected = bool(matched_trusted_domains)
>>>>>>> theirs
=======
    matched_trusted_domains = get_matched_trusted_domains(sender_domain, link_domains)
    trusted_domain_detected = bool(matched_trusted_domains)
>>>>>>> theirs

    risk_score = int(round(phishing_probability * 100))
    postprocess_notes = []

    if short_url_domains:
        risk_score += 12
        postprocess_notes.append("偵測到短網址，最終風險分數已提高。")

    if domain_mismatches:
        risk_score += 18
        postprocess_notes.append("信件提到官方品牌，但寄件者或連結網域與常見官方網域不一致。")

    if trusted_domain_detected and not short_url_domains and not domain_mismatches:
        risk_score -= 15
        postprocess_notes.append("偵測到常見可信或官方網域，最終風險分數已保守下修。")

    if official_brand_mentions and not domain_mismatches:
        postprocess_notes.append("信件內容提到官方品牌，未發現明顯官方網域不一致。")

    risk_score = max(0, min(100, risk_score))

    return {
        "risk_score": risk_score,
        "official_domains": sorted(TRUSTED_DOMAINS),
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
=======
        "trusted_domains": sorted(TRUSTED_DOMAINS),
        "matched_official_domains": matched_official_domains,
        "matched_trusted_domains": matched_trusted_domains,
>>>>>>> theirs
=======
        "trusted_domains": sorted(TRUSTED_DOMAINS),
        "matched_official_domains": matched_official_domains,
        "matched_trusted_domains": matched_trusted_domains,
>>>>>>> theirs
=======
        "trusted_domains": sorted(TRUSTED_DOMAINS),
        "matched_official_domains": matched_official_domains,
        "matched_trusted_domains": matched_trusted_domains,
>>>>>>> theirs
        "trusted_domain_detected": trusted_domain_detected,
        "short_urls": short_url_domains,
        "domain_mismatch": bool(domain_mismatches),
        "domain_mismatch_details": domain_mismatches,
        "postprocess_notes": postprocess_notes,
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
=======
        "sender_domain": sender_domain,
        "url_domains": link_domains,
>>>>>>> theirs
=======
        "sender_domain": sender_domain,
        "url_domains": link_domains,
>>>>>>> theirs
=======
        "sender_domain": sender_domain,
        "url_domains": link_domains,
>>>>>>> theirs
        "observed_domains": {
            "sender_domain": sender_domain,
            "link_domains": link_domains,
        },
    }


def get_request_text(payload):
    subject = payload.get("subject", "") if isinstance(payload, dict) else ""
    sender = payload.get("sender", "") if isinstance(payload, dict) else ""
    body = ""
    if isinstance(payload, dict):
        body = (
            payload.get("body")
            or payload.get("content")
            or payload.get("text")
            or payload.get("email_text")
            or ""
        )
    return subject, sender, body
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs


@app.get("/")
def health_check():
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
    return jsonify({
        "status": "ok",
        "model_loaded": model is not None and vectorizer is not None,
        "error": model_error,
    })
=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
    return jsonify(
        {
            "service": "genai-anti-scam-api",
            "status": "ok" if model_load_error is None else "model_unavailable",
            "model_loaded": model_load_error is None,
            "model_error": model_load_error,
            "allowed_origins": ALLOWED_ORIGINS,
            "endpoints": ["GET /", "POST /api/analyze-email"],
            "metrics": metrics,
        }
    )
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs


@app.post("/api/analyze-email")
def analyze_email():
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
    if model is None or vectorizer is None:
        return jsonify({
            "error": model_error or "Model artifacts are not loaded.",
            "model_loaded": False,
            "required_files": [
                "backend/phishing_model/phishing_classifier.pkl",
                "backend/phishing_model/vectorizer.pkl",
                "backend/phishing_model/metrics.json",
            ],
        }), 503

    payload = request.get_json(silent=True) or {}
    subject = str(payload.get("subject", "") or "")
    sender = str(payload.get("sender", "") or "")
    body = str(payload.get("body", "") or "")
    text = str(payload.get("text", "") or "")

    if text and not body:
        body = text

    email_text = build_email_text(subject, sender, body)
    if not email_text:
        return jsonify({"error": "Please provide subject, sender, body, or text."}), 400

    try:
        phishing_probability, predicted_is_phishing = predict_phishing_probability(email_text)
        return jsonify(build_response(subject, sender, body, phishing_probability, predicted_is_phishing))
    except Exception as exc:
        return jsonify({
            "error": f"Failed to analyze email: {exc}",
            "model_loaded": False,
        }), 500


load_artifacts()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
    if model_load_error is not None or classifier is None or vectorizer is None:
        return (
            jsonify(
                {
                    "error": "model_unavailable",
                    "message": model_load_error or "Model is not loaded.",
                    "required_files": [
                        "backend/phishing_model/phishing_classifier.pkl",
                        "backend/phishing_model/vectorizer.pkl",
                        "backend/phishing_model/metrics.json",
                    ],
                }
            ),
            503,
        )

    payload = request.get_json(silent=True) or {}
    subject, sender, body = get_request_text(payload)
    combined_text = "\n".join(part for part in [subject, sender, body] if part).strip()

    if not combined_text:
        return (
            jsonify(
                {
                    "error": "invalid_request",
                    "message": "Please provide email text in one of: text, body, content, or email_text.",
                }
            ),
            400,
        )

    features = vectorizer.transform([combined_text])
    probabilities = classifier.predict_proba(features)[0]
    phishing_probability = float(probabilities[1])
    prediction = int(classifier.predict(features)[0])
    postprocessed = postprocess_risk(phishing_probability, subject, sender, body)
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
    user_facing_fields = build_user_facing_fields(
        combined_text,
        phishing_probability,
        postprocessed["risk_score"],
        postprocessed,
    )
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs

    return jsonify(
        {
            "is_phishing": bool(prediction),
            "label": "phishing" if prediction else "normal",
            "phishing_probability": phishing_probability,
            "risk_score": postprocessed["risk_score"],
            "model": "TF-IDF + Logistic Regression",
            "metrics": metrics,
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
=======
            **user_facing_fields,
>>>>>>> theirs
=======
            **user_facing_fields,
>>>>>>> theirs
=======
            **user_facing_fields,
>>>>>>> theirs
            **postprocessed,
        }
    )


load_model_artifacts()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
