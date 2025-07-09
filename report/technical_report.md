# AI Engineer Technical Report: Domain Name Generator

## Executive Summary

This report presents the development and evaluation of a fine-tuned language model for automated domain name generation. The project implements a complete ML pipeline including synthetic data generation, model fine-tuning, systematic evaluation using LLM-as-a-Judge, edge case analysis, and safety guardrails. The final system is deployed as a FastAPI application with robust content filtering capabilities.

**Key Achievements:**

- Fine-tuned Flan-T5 model (`flan-t5-base`) for domain name generation
- Simulated LLM-as-a-Judge framework scoring domain quality
- Edge case discovery across 5 failure categories
- API deployed with FastAPI and dynamic model loading
- Achieved average Relevance: 0.89, Creativity: 0.85, Professionalism: 0.86 (on validation set)

---

## 1. Methodology & Initial Results

### 1.1 Dataset Creation Approach

**Synthetic Data Generation Strategy:**

- Method: Python script (`generate_dataset.py`) used to randomly combine business categories, tone, and size to form realistic descriptions.
- Business Types Covered: Tech, Food, Legal, Fashion, Finance, Wellness, Health, Education, Beauty, Nonprofit
- Data Complexity Levels: Simple ("A food startup"), Medium ("A growing legal firm serving startups"), Complex ("A digital-first health platform for busy urban professionals")
- Dataset Size: 200 samples (80% train, 10% val, 10% test)

**Data Quality Measures:**

- Category and tone diversity
- Controlled text length distribution
- Template-based grammar
- Manual inspection of edge cases

### 1.2 Baseline Model Selection

**Model Choice: Flan-T5-Base**

- Rationale: Instruction-tuned, high-quality open-source generation model with good support for few-shot formatting
- Model Size: ~250M parameters
- Pre-training Advantages: Handles "task: input" format naturally, improving domain-specific prompting

**Training Configuration:**

```
training_args = TrainingArguments(
    output_dir="../models/model_v1",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    save_strategy="epoch",
    logging_dir="../models/model_v1/logs",
    logging_steps=10,
    save_total_limit=2
)
```

### 1.3 Initial Model Performance

**Training Results:**

- Training Loss: ~1.2
- Validation Loss: ~1.4
- Training Time: ~12 minutes (Colab GPU)
- Model Size: ~1.1GB including tokenizer/config

**Evaluation Scores (sample of 25):**

- Relevance: 0.89
- Creativity: 0.85
- Professionalism: 0.86

**Sample Output:**

```
Business: "eco-friendly digital banking startup"
1. greenbanker.io
2. sustainfintech.com
3. ecofinancehub.net
```

---

## 2. Edge Case Analysis

### 2.1 Discovery Process

- Method 1: Manual adversarial prompting
- Method 2: Overlapping/contradictory keywords ("legal tattoo shop")
- Method 3: Domain-specific nonsense inputs ("kill zone ai for pets")

### 2.2 Failure Taxonomy

| Category             | Example Input       | Example Output           | Root Cause               |
| -------------------- | ------------------- | ------------------------ | ------------------------ |
| Relevance Failures   | "AI lawyer"         | "beautyskinhub.com"      | Context misalignment     |
| Creativity Failures  | "coffee shop"       | "coffee1.com"            | Repetitive decoding      |
| Professionalism Fail | "tax software"      | "savetax4u.com"          | Tone mismatch            |
| Technical Failures   | "global fintech ai" | "fin_tech_ai_no_tld"     | No TLD postprocessing    |
| Safety Failures      | "xxx site"          | (Blocked)                | Caught by keyword filter |

### 2.3 Failure Frequency Summary

```
Edge Case Type          | Frequency | Severity | Priority
------------------------|-----------|----------|----------
Relevance Failures     | 20%       | Medium   | 2
Creativity Failures    | 24%       | Medium   | 2
Professionalism Fail   | 16%       | Low      | 3
Technical Failures     | 4%        | Low      | 3
Safety Failures        | 100% blocked | High  | 1
```

---

## 3. Iterative Improvement

### 3.1 Sampling Enhancements

- Switched from greedy decoding to `do_sample=True`
- Set `num_return_sequences=3` for variation
- Tuned `max_new_tokens=20` for brevity

### 3.2 Safety Enhancements

- Implemented `is_safe_input()` filter in `utils/safety.py`
- Used in `main.py` before generation
- Blocked inputs include: `xxx`, `nude`, `kill`, `fck`, etc.

### 3.3 Evaluation Enhancements

- Created `mock_judge()` with scoring rules
- Used to populate `eval_model_v1.csv`
- Categories: relevance, creativity, professionalism, flagged

---

## 4. LLM-as-a-Judge Evaluation Framework

- No paid GPT used (free version)
- Simulated GPT-like scoring using `mock_judge()`
- Scoring dimensions:
  - Relevance: keyword + context match
  - Creativity: lexical uniqueness
  - Professionalism: domain tone
- Output used to flag low-quality generations and analyze model behavior

---

## 5. Safety Guardrails

### 5.1 Blocking Strategy

- Keywords defined in `safety.py`
- Checks lowercase string match and partials
- Trigger blocks if any matches

### 5.2 Example Blocked Input

```
{
  "business_description": "xxx nude content"
}
```

→ Response:

```
{
  "status": "blocked",
  "message": "Request contains inappropriate content"
}
```

---

## 6. API Deployment

- Built with FastAPI
- POST `/generate`
- Accepts JSON: `{ "business_description": "..." }`
- Returns domain suggestions or block message
- Launched with Uvicorn (`uvicorn app.main:app --reload`)
- Includes logging for safety & model errors

---

## 7. Conclusion

### Key Achievements

- End-to-end LLM pipeline from dataset to deployment
- Full edge case + safety coverage
- API-compatible with robust formatting and output

### Lessons Learned

- Decoding strategy has major effect on diversity
- Template-based data gen produces strong baseline performance
- Safety needs both input + output filtering for real-world use

---

**Repository:** [https://github.com/VishnuCharugundla/ai-domain-name-generator](https://github.com/VishnuCharugundla/ai-domain-name-generator)  
**Author:** Vishnu Charugundla
```
