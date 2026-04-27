from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os

from metrics import evaluate_metrics, final_score
from database import cursor, conn

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schema
class Input(BaseModel):
    prompt: str
    answer: str

@app.get("/")
def home():
    return {"status": "running"}

# MAIN EVALUATION
@app.post("/evaluate")
def evaluate(data: Input):

    stats_metrics = evaluate_metrics(data.prompt, data.answer)
    
    from llm import generate_llm_metrics
    llm_data = generate_llm_metrics(data.prompt, data.answer)

    # Validation and Normalization Layer
    final_metrics = {}
    feedback = ""
    used_ai = False

    if llm_data and isinstance(llm_data, dict):
        for key in ["relevance", "clarity", "depth", "structure"]:
            val = llm_data.get(key)
            if isinstance(val, (int, float)) and 0 <= val <= 100:
                final_metrics[key] = float(val)
            else:
                final_metrics[key] = stats_metrics[key]
        feedback = str(llm_data.get("feedback", "")).strip()
        used_ai = True
    else:
        final_metrics = stats_metrics.copy()

    score = final_score(final_metrics)

    if not feedback:
        if score >= 80:
            feedback = "Excellent response with strong clarity, depth, and relevance."
        elif score >= 50:
            feedback = "Good answer with solid understanding, but could benefit from deeper explanation."
        else:
            feedback = "Weak response. Lacks clarity, depth, and alignment with the prompt."

    source_text = "AI-Evaluated" if used_ai else "Statistically Calculated"

    rubric = f"""
### Evaluation Rubric

| Criteria | Score | Evaluation Source |
| :--- | :--- | :--- |
| **Relevance** | {final_metrics['relevance']}% | {source_text} |
| **Clarity** | {final_metrics['clarity']}% | {source_text} |
| **Depth** | {final_metrics['depth']}% | {source_text} |
| **Structure** | {final_metrics['structure']}% | {source_text} |
"""

    reasoning = [
        f"Relevance Score: {final_metrics['relevance']}%",
        f"Clarity Score: {final_metrics['clarity']}%",
        f"Depth Score: {final_metrics['depth']}%",
        f"Structure Score: {final_metrics['structure']}%"
    ]

    record_id = str(uuid.uuid4())

    cursor.execute(
        "INSERT INTO results VALUES (?,?,?,?,?)",
        (record_id, data.prompt, data.answer, score, feedback)
    )
    conn.commit()

    return {
        "id": record_id,
        "score": score,
        "feedback": feedback,
        "rubric": rubric,
        "reasoning": reasoning
    }


# GET ALL RESULTS
@app.get("/results")
def get_results():
    cursor.execute("SELECT * FROM results")
    rows = cursor.fetchall()

    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "prompt": r[1],
            "answer": r[2],
            "score": r[3],
            "feedback": r[4]
        })

    return results


# GET SINGLE RESULT
@app.get("/results/{record_id}")
def get_single(record_id: str):
    cursor.execute("SELECT * FROM results WHERE id=?", (record_id,))
    r = cursor.fetchone()

    if not r:
        return {"error": "Not found"}

    return {
        "id": r[0],
        "prompt": r[1],
        "answer": r[2],
        "score": r[3],
        "feedback": r[4]
    }


# CLEAR DATABASE 
@app.delete("/clear")
def clear_db():
    cursor.execute("DELETE FROM results")
    conn.commit()
    return {"message": "All records deleted"}


# RENDER PORT FIX
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)