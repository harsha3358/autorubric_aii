# AutoRubric AI

AutoRubric AI reviews student answers and presents scores, strengths, weaknesses, and practical feedback in a clear dashboard.

## Why it matters

Manual grading takes time and can vary between reviewers. This project explores how AI and fixed scoring rules can support faster, more consistent evaluation while keeping the reasoning visible.

## What it does

- Scores clarity, depth, structure, and relevance
- Generates written feedback and a structured rubric
- Uses validation rules when the AI response is unavailable or malformed
- Stores past results for review

## Technology

FastAPI, Python, Hugging Face models, SQLite, JavaScript, Tailwind CSS, and Chart.js.

## Run locally

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 10000
```

Serve the `frontend` folder separately and configure `HF_TOKEN` to enable AI evaluation.
