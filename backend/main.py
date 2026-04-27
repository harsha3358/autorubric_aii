from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os

from metrics import evaluate_metrics, final_score
from database import cursor, conn

app = FastAPI()

# ✅ CORS
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

# 🔥 MAIN EVALUATION
@app.post("/evaluate")
def evaluate(data: Input):

    metrics = evaluate_metrics(data.prompt, data.answer)
    score = final_score(metrics)

    rubric = f"""
Evaluation Rubric

1. Relevance ({metrics['relevance']}%)
2. Depth ({metrics['depth']}%)
3. Structure ({metrics['structure']}%)
4. Clarity ({metrics['clarity']}%)
"""

    if score > 85:
        feedback = "Excellent response with strong clarity, depth, and relevance."
    elif score > 70:
        feedback = "Good answer with solid understanding, but could benefit from deeper explanation."
    elif score > 50:
        feedback = "Average response with partial understanding. Needs more structure and detail."
    else:
        feedback = "Weak response. Lacks clarity, depth, and alignment with the prompt."

    reasoning = [
        f"Relevance Score: {metrics['relevance']}%",
        f"Depth Score: {metrics['depth']}%",
        f"Structure Score: {metrics['structure']}%",
        f"Clarity Score: {metrics['clarity']}%"
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


# 📊 GET ALL RESULTS
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


# 🔍 GET SINGLE RESULT
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


# 🧹 CLEAR DATABASE (for demo reset)
@app.delete("/clear")
def clear_db():
    cursor.execute("DELETE FROM results")
    conn.commit()
    return {"message": "All records deleted"}


# 🔥 RENDER PORT FIX
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)