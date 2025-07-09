# AI Domain Name Generator 🚀

This project fine-tunes a language model (Flan-T5) to generate domain name suggestions based on business descriptions. It includes data generation, training, evaluation with a simulated LLM-as-a-Judge, edge case analysis, and a deployed FastAPI app.

---

## 📁 Folder Structure

```
AI Engineer Project/
├── app/               # FastAPI backend with /generate endpoint
├── data/              # JSON dataset, evaluation CSVs
├── models/            # Tokenizer + model config (no weights)
├── notebooks/         # Jupyter notebooks for training and eval
├── report/            # Technical write-up
├── utils/             # Safety filter logic
```

---

## 🔮 Run the API

```bash
uvicorn app.main:app --reload
```

Then visit: [http://localhost:8000/docs](http://localhost:8000/docs) to test

---

## 🛡️ Safety Guardrails

Blocked inputs like:

```json
{ "business_description": "xxx nude adult site" }
```

Result in:

```json
{
  "status": "blocked",
  "message": "Request contains inappropriate content"
}
```

---

## 📆 Note on Model Weights

This repo does **not include model weights** (`model.safetensors`) to keep it lightweight.
You can regenerate the model using `notebooks/01_model_training.ipynb`.

---

## ✨ Features

* Fine-tuned Flan-T5 on synthetic business data
* Domain name generator API with Swagger UI
* LLM-as-a-Judge style scoring (relevance, creativity, professionalism)
* Edge case discovery and analysis
* Safety filtering for inappropriate content

---

## 📄 Report

See `report/technical_report.md` for the full write-up.

## 🧠 FAQ / Troubleshooting

- **Q:** Why do I get `blocked` in the response?
  **A:** The input likely contains restricted content. Check `utils/safety.py` for rules.

- **Q:** Why are there only 3 domain names returned?
  **A:** The model is configured to return `num_return_sequences=3`. You can change this in `main.py`.

- **Q:** I don’t see results in Swagger. What do I do?
  **A:** Restart the server and visit http://localhost:8000/docs again.
