<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
# Phishing Model Artifacts

這個資料夾本機需要放：
=======
# Phishing model artifacts

The Flask API expects these files in this directory at deploy time:
>>>>>>> theirs
=======
# Phishing model artifacts

The Flask API expects these files in this directory at deploy time:
>>>>>>> theirs
=======
# Phishing model artifacts

The Flask API expects these files in this directory at deploy time:
>>>>>>> theirs
=======
# Phishing model artifacts

The Flask API expects these files in this directory at deploy time:
>>>>>>> theirs
=======
# Phishing model artifacts

The Flask API expects these files in this directory at deploy time:
>>>>>>> theirs
=======
# Phishing model artifacts

The Flask API expects these files in this directory at deploy time:
>>>>>>> theirs

- `phishing_classifier.pkl`
- `vectorizer.pkl`
- `metrics.json`

<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
`.pkl` 模型檔不建議 push 到 public GitHub。請只在本機或受控環境保存模型檔。
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
These artifacts are used by the TF-IDF + Logistic Regression email classifier.

For the final project demo, strategy A is acceptable if the files are small and do not contain API keys, private data, or personally identifiable information: commit the two `.pkl` files and `metrics.json` so Render or Railway can deploy directly from GitHub.

> 此模型檔僅供期末展示，不含 API key 或個資；正式部署不建議將模型權重放 public repo。

If you do not commit the `.pkl` files, upload or mount them through the deployment platform before starting the API. Otherwise `/api/analyze-email` will return `503 model_unavailable` instead of crashing.
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
