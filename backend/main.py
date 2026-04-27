from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os

from llm import generate
from metrics import final_score
from database import cursor, conn

app = FastAPI()

# 🔥 STRICT CORS FIX (IMPORTANT)
origins = [
    "https://autorubricaii.vercel.app",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Input(BaseModel):
    prompt: str
    answer: str

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/evaluate")
def evaluate(data: Input):
    combined_prompt = f"""
    Evaluate the answer.

    Prompt: {data.prompt}
    Answer: {data.answer}

    Give rubric and feedback.
    """

    llm_output = generate(combined_prompt)
    score = final_score(data.prompt, data.answer)

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

# 🔥 REQUIRED FOR RENDER
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)