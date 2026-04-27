from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import uuid
import asyncio
from functools import lru_cache

from llm import generate
from metrics import final_score
from database import cursor, conn

app = FastAPI()

# CORS (important for frontend)
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

# 🔥 CACHE LLM CALLS
@lru_cache(maxsize=100)
def cached_generate(prompt: str):
    return generate(prompt)

# 🔥 PARALLEL EXECUTION
async def get_outputs(prompt, answer):
    loop = asyncio.get_event_loop()

    rubric_task = loop.run_in_executor(
        None, cached_generate, f"Create a short rubric for: {prompt}"
    )

    feedback_task = loop.run_in_executor(
        None, cached_generate, f"Give concise feedback for: {answer}"
    )

    rubric, feedback = await asyncio.gather(rubric_task, feedback_task)

    return rubric, feedback

@app.get("/")
def home():
    return {"status": "AutoRubric backend running"}

# 🚀 MAIN ENDPOINT
@app.post("/evaluate")
async def evaluate(data: Input):

    # parallel LLM calls
    rubric, feedback = await get_outputs(data.prompt, data.answer)

    # scoring
    score = final_score(data.prompt, data.answer)

    # store result
    cursor.execute(
        "INSERT INTO results VALUES (?,?,?,?,?)",
        (str(uuid.uuid4()), data.prompt, data.answer, score, feedback)
    )
    conn.commit()

    return {
        "score": score,
        "feedback": feedback,
        "rubric": rubric
    }