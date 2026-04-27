from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os

from metrics import evaluate_metrics, final_score
from database import cursor, conn

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input schema
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

    # 🔥 PROFESSIONAL RUBRIC
    rubric = f"""
Evaluation Rubric

1. Relevance ({metrics['relevance']}%)
   Measures alignment with the given prompt.

2. Depth ({metrics['depth']}%)
   Evaluates completeness and level of detail.

3. Structure ({metrics['structure']}%)
   Assesses logical organization and flow.

4. Clarity ({metrics['clarity']}%)
   Measures readability and articulation.
"""

    # 🔥 PROFESSIONAL FEEDBACK
    if score > 85:
        feedback = "Excellent response with strong clarity, depth, and relevance."
    elif score > 70:
        feedback = "Good answer with solid understanding, but could benefit from deeper explanation."
    elif score > 50:
        feedback = "Average response with partial understanding. Needs more structure and detail."
    else:
        feedback = "Weak response. Lacks clarity, depth, and alignment with the prompt."

    # 🔥 REASONING
    reasoning = [
        f"Relevance Score: {metrics['relevance']}%",
        f"Depth Score: {metrics['depth']}%",
        f"Structure Score: {metrics['structure']}%",
        f"Clarity Score: {metrics['clarity']}%"
    ]

    # Save to DB
    cursor.execute(
        "INSERT INTO results VALUES (?,?,?,?,?)",
        (str(uuid.uuid4()), data.prompt, data.answer, score, feedback)
    )
    conn.commit()

    return {
        "score": score,
        "feedback": feedback,
        "rubric": rubric,
        "reasoning": reasoning
    }


# 🔥 RENDER PORT FIX
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)