<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
# Flask Backend

這個 backend 用於本機即時釣魚郵件模型推理。GitHub Pages 只能提供靜態網站，不能直接執行 Python，也不能載入 `.pkl` 模型檔進行推理。

## 本機模型檔

請手動將模型檔放到以下位置：

- `backend/phishing_model/phishing_classifier.pkl`
- `backend/phishing_model/vectorizer.pkl`
- `backend/phishing_model/metrics.json`

不要把 `.pkl` 模型檔 push 到 public GitHub。

## 啟動 backend

```bash
cd backend
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
# Flask backend deployment guide

This backend exposes a public HTTP API for the GitHub Pages frontend. It keeps the final project architecture as:

- **Frontend:** GitHub Pages (`web/`)
- **Backend:** Render or Railway public Flask service (`backend/`)
- **Model:** existing B plan, **TF-IDF + Logistic Regression**

The backend does not use Hugging Face, Gradio public URLs, or image recognition.

## API endpoints

- `GET /` — health check and model status
- `POST /api/analyze-email` — analyzes an email with the local model artifacts

Example request:

```bash
curl -X POST http://127.0.0.1:5000/api/analyze-email \
  -H "Content-Type: application/json" \
  -d '{"subject":"帳戶即將停用","sender":"security@example-login.com","text":"請立即點擊 https://bit.ly/demo 驗證帳戶"}'
```

The response keeps two separate risk values:

- `phishing_probability`: the raw model probability.
- `risk_score`: the final user-facing score after post-processing.

The post-processing preserves official/trusted domain checks, short URL detection, domain mismatch notes, and `postprocess_notes`.

## Local run

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
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
pip install -r requirements.txt
python app.py
```

<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
啟動後打開：

```text
http://127.0.0.1:5000
```

## 開啟本機測試頁

另開一個終端機，在 repo 根目錄執行：

```bash
python -m http.server 5501 -d web
```

接著打開：

```text
http://localhost:5501/live-api-demo.html
```
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
The service listens on `0.0.0.0` and uses `PORT` when provided by a deployment platform. Locally, it defaults to port `5000`.

## Required model files

Put these files in `backend/phishing_model/` before running or deploying:

```text
backend/phishing_model/phishing_classifier.pkl
backend/phishing_model/vectorizer.pkl
backend/phishing_model/metrics.json
```

If the files are missing, the app will not crash. Instead, `POST /api/analyze-email` returns `503 model_unavailable` with the missing file list.

## CORS and GitHub Pages

The backend reads allowed origins from `ALLOWED_ORIGINS`:

```python
ALLOWED_ORIGINS = os.environ.get(
    "ALLOWED_ORIGINS",
    "http://localhost:5501,http://127.0.0.1:5501"
).split(",")
```

For deployment, set this environment variable to include local testing and GitHub Pages:

```text
ALLOWED_ORIGINS=https://smallweiweihsu.github.io,https://smallweiweihsu.github.io/genai-final-anti-scam,http://localhost:5501,http://127.0.0.1:5501
```

If the final GitHub Pages URL changes, add the exact URL here.

## Render deployment steps

`render.yaml` is stored at the **repository root** because Render Blueprints normally discover it from the root of the GitHub repo. The service still uses `rootDir: backend` so Render builds and starts the Flask backend from this folder.

1. Confirm `backend/app.py` runs locally.
2. Confirm `backend/requirements.txt` exists.
3. Confirm `backend/phishing_model/` contains the model files.
4. Commit and push to GitHub.
5. Go to Render and create a Web Service.
6. Connect this GitHub repo.
7. Set **Root Directory** to `backend` if configuring manually.
8. Set build command:
   ```bash
   pip install -r requirements.txt
   ```
9. Set start command:
   ```bash
   gunicorn app:app
   ```
10. Set environment variable:
   ```text
   ALLOWED_ORIGINS=https://smallweiweihsu.github.io,https://smallweiweihsu.github.io/genai-final-anti-scam,http://localhost:5501,http://127.0.0.1:5501
   ```
11. Deploy and copy the public Render URL.
12. Open `web/live-api-demo.html` on GitHub Pages and set the API URL to the Render URL.
13. Test the email analysis function.

## Railway notes

Railway can also run this backend. Use `backend` as the service root, install dependencies from `requirements.txt`, and start with:

```bash
gunicorn app:app
```

Railway also provides `PORT`, which `app.py` reads automatically.

## Model deployment strategy

### Strategy A — commit `.pkl` files for the final demo

Recommended for this final project if the files are small and do not contain sensitive data.

Pros:

- Simplest workflow.
- Render / Railway can deploy directly from GitHub.
- Lowest risk of getting blocked before the final presentation.

Cons:

- A public repo will expose the model files.
- Not recommended for production.

> 此模型檔僅供期末展示，不含 API key 或個資；正式部署不建議將模型權重放 public repo。

### Strategy B — keep `.pkl` files outside GitHub

Examples: Google Drive download during build, GitHub Release artifact, private repo, or deployment platform private storage.

Pros:

- Better security.

Cons:

- More moving parts.
- Higher chance of deployment failure before the final presentation.

## Current `.gitignore` warning

The repository currently ignores `*.pkl`. If you choose Strategy A, you must explicitly allow these two files before committing them:

```gitignore
*.pkl
!backend/phishing_model/phishing_classifier.pkl
!backend/phishing_model/vectorizer.pkl
```

Do not commit API keys, `.env`, private data, raw phishing URLs, or sensitive screenshots.
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
