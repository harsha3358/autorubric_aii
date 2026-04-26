from fastapi import FastAPI
from pydantic import BaseModel
import uuid

from fastapi.middleware.cors import CORSMiddleware

from llm import generate
from metrics import final_score
from database import cursor, conn

app = FastAPI()

# CORS (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Input(BaseModel):
    prompt: str
    answer: str

@app.post("/evaluate")
def evaluate(data: Input):

    # Generate rubric
    rubric = generate(f"Create a simple rubric for: {data.prompt}")

    # Generate feedback
    feedback = generate(f"""
Evaluate this answer based on the rubric.

Rubric: {rubric}
Answer: {data.answer}

Give short feedback.
""")

    # NEW SCORING SYSTEM
    score = final_score(data.prompt, data.answer)

    # Save to DB
    cursor.execute("INSERT INTO results VALUES (?,?,?,?,?)",
                   (str(uuid.uuid4()), data.prompt, data.answer, score, feedback))
    conn.commit()

    return {
        "score": score,
        "feedback": feedback,
        "rubric": rubric
    }