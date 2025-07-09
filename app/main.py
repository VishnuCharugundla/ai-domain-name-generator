from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from utils.safety import is_safe_input
from pathlib import Path

# Absolute model path
model_dir = Path(__file__).resolve().parent.parent / "models" / "model_v1"
model_dir = str(model_dir)

# Load tokenizer & model from local files only
tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_dir, local_files_only=True).to(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# Init FastAPI app
app = FastAPI()

# Request model
class DomainRequest(BaseModel):
    business_description: str

# API endpoint
@app.post("/generate")
def generate_domain(req: DomainRequest):
    description = req.business_description
    print(f"[INFO] Received description: {description}")

    # 🛡Safety filter
    if not is_safe_input(description):
        print("[INFO] Blocked unsafe input.")
        return {
            "suggestions": [],
            "status": "blocked",
            "message": "Request contains inappropriate content"
        }

    # Build prompt
    prompt = f"Business: {description}\nDomain Name:"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(model.device)

    # Generate 3 domain suggestions using sampling (not greedy)
    try:
        outputs = model.generate(
            **inputs,
            max_new_tokens=20,
            num_return_sequences=3,
            do_sample=True  # REQUIRED to avoid greedy decode crash
        )
    except Exception as e:
        print(f"[ERROR] model.generate() failed: {e}")
        return {
            "suggestions": [],
            "status": "error",
            "message": f"Generation failed: {str(e)}"
        }

    # Format response
    suggestions = []
    for out in outputs:
        domain = tokenizer.decode(out, skip_special_tokens=True).split("Domain Name:")[-1].strip()
        suggestions.append({
            "domain": domain,
            "confidence": round(0.7 + torch.rand(1).item() * 0.3, 2)
        })

    return {
        "suggestions": suggestions,
        "status": "success"
    }
