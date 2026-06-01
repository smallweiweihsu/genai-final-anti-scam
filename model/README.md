# Model

此資料夾用來放模型相關說明、輸出範例與評估摘要。

第一版不放大型模型檔案，也不放 `.pt`、`.bin`、`.safetensors`、`.gguf` 等權重檔。

## 建議放置內容

- `predict_example.py`：未來可放簡化推論範例。
- `model_result_examples.json`：模型輸出範例。
- `evaluation_summary.md`：Experiment A / B / C 比較與誤判分析。

## 第一版對接策略

前端先讀取 `web/mockData.js`。B 的 API 完成後，只要輸出符合 `docs/api_schema.md`，前端即可替換資料來源。
