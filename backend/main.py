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

    combined_prompt = f"""
    Generate a short rubric and feedback.

    Prompt: {prompt}
    Answer: {answer}

    Output:
    Rubric:
    Feedback:
    """

    result = await loop.run_in_executor(None, cached_generate, combined_prompt)

    return result

@app.get("/")
def home():
    return {"status": "AutoRubric backend running"}

#  MAIN ENDPOINT
@app.post("/evaluate")
async def evaluate(data: Input):

    output = await get_outputs(data.prompt, data.answer)

    score = final_score(data.prompt, data.answer)

    return {
        "score": score,
        "feedback": output,
        "rubric": "Generated within feedback"
    }