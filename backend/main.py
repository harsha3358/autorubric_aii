from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os

from llm import generate
from metrics import final_score
from database import cursor, conn

app = FastAPI()

# ✅ CORS FIX (CRITICAL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class Input(BaseModel):
    prompt: str
    answer: str

# Health check
@app.get("/")
def home():
    return {"status": "AutoRubric backend running"}

# Main endpoint
@app.post("/evaluate")
def evaluate(data: Input):

    # 🔥 Single LLM call (optimized)
    combined_prompt = f"""
    Evaluate the following answer.

    Prompt:
    {data.prompt}

    Answer:
    {data.answer}

    Provide:
    1. Short rubric (3 points)
    2. Feedback (concise)
    """

    llm_output = generate(combined_prompt)

    # Scoring
    score = final_score(data.prompt, data.answer)

    # Store in DB
    cursor.execute(
        "INSERT INTO results VALUES (?,?,?,?,?)",
        (str(uuid.uuid4()), data.prompt, data.answer, score, llm_output)
    )
    conn.commit()

    return {
        "score": score,
        "feedback": llm_output,
        "rubric": "Included in feedback"
    }


# 🔥 RENDER PORT FIX
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)