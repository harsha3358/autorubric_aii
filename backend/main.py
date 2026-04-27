from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import uuid

from llm import generate
from metrics import final_score
from database import cursor, conn

# 🔥 INIT APP
app = FastAPI()

# 🔥 CORS FIX (CRITICAL FOR VERCEL FRONTEND)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (safe for demo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 INPUT SCHEMA
class Input(BaseModel):
    prompt: str
    answer: str

# 🔹 HEALTH CHECK
@app.get("/")
def home():
    return {"status": "AutoRubric backend running"}

# 🔹 MAIN EVALUATION ENDPOINT
@app.post("/evaluate")
def evaluate(data: Input):

    # 🔥 SINGLE LLM CALL (FAST)
    combined_prompt = f"""
    Evaluate the following answer.

    Prompt:
    {data.prompt}

    Answer:
    {data.answer}

    Provide:
    1. Short rubric (3-4 points)
    2. Feedback (concise)
    """

    llm_output = generate(combined_prompt)

    # 🔹 SCORING (LIGHTWEIGHT)
    score = final_score(data.prompt, data.answer)

    # 🔹 STORE RESULT
    cursor.execute(
        "INSERT INTO results VALUES (?,?,?,?,?)",
        (str(uuid.uuid4()), data.prompt, data.answer, score, llm_output)
    )
    conn.commit()

    # 🔹 RESPONSE
    return {
        "score": score,
        "feedback": llm_output,
        "rubric": "Included in feedback"
    }