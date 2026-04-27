# AutoRubric AI

**Intelligent Answer Evaluation System**

AutoRubric AI is a full-stack AI-powered system that evaluates user responses using a multi-metric scoring engine, generates structured rubrics, and provides explainable feedback.

---

## Live Deployment

Frontend (Vercel):  
https://autorubricaii.vercel.app/

Backend (Render):  
https://autorubric-aii.onrender.com/

API Documentation:  
https://autorubric-aii.onrender.com/docs

Database Access (via API):  
https://autorubric-aii.onrender.com/results

---

## Overview

AutoRubric AI analyzes a given prompt and answer, then produces:

- Structured evaluation rubric  
- Multi-dimensional score  
- Professional feedback  
- Transparent reasoning  

The system combines deterministic scoring logic with optional AI-assisted evaluation to ensure reliability and scalability.

---

## Features

- Multi-metric evaluation (Relevance, Depth, Structure, Clarity)  
- Explainable scoring with reasoning breakdown  
- Automatic rubric generation  
- Real-time evaluation API  
- Persistent result storage  
- Fully deployed cloud architecture  

---

## Architecture

Frontend (Vercel)  
→ FastAPI Backend (Render)  
→ Evaluation Engine (Python)  
→ SQLite Database  

---

## Tech Stack

### Frontend
- HTML5  
- Tailwind CSS  
- JavaScript (Vanilla)  
- Chart.js  

### Backend
- Python  
- FastAPI  
- Uvicorn  
- Pydantic  

### Evaluation Engine
- Custom rule-based scoring system  
- Multi-metric analysis  

### Database
- SQLite  

### Deployment
- Vercel (Frontend)  
- Render (Backend)  
- GitHub (Version Control)  

---

## Evaluation Metrics

The system evaluates answers across four key dimensions:

- **Relevance** – Alignment with the prompt  
- **Depth** – Level of detail and completeness  
- **Structure** – Logical flow and organization  
- **Clarity** – Readability and articulation  

### Final Score Formula

Score =  
0.35 × Relevance +  
0.30 × Depth +  
0.20 × Structure +  
0.15 × Clarity  

---

## API Endpoints

### POST /evaluate  
Evaluate a prompt-answer pair  

# AutoRubric-AI

## Clone the repository:

```bash
git clone https://github.com/harsha3358/AutoRubric-AI.git
cd AutoRubric-AI/backend
```

## Install dependencies:

```bash
pip install -r requirements.txt
```

## Run backend:

```bash
python main.py
```

## Open the frontend from the frontend folder.

## Deployment

### Backend (Render)

*   **Root Directory:** `backend`
*   **Build Command:** `pip install -r requirements.txt`
*   **Start Command:** `python main.py`
*   **Environment Variable:**
    *   `HF_TOKEN` (optional, if using LLM)

### Frontend (Vercel)

*   Deploy frontend folder
*   Update API URL in `app.js`

## Design Principles

*   Explainability over black-box models
*   Lightweight and deployable architecture
*   Deterministic + AI hybrid system
*   Production-ready design

## Limitations

*   Uses heuristic scoring instead of full semantic embeddings
*   SQLite is not persistent on free hosting
*   Free-tier hosting introduces cold-start latency

## Future Improvements

*   LLM-based evaluator (AI judge)
*   Semantic similarity via embeddings API
*   Analytics dashboard
*   PostgreSQL or cloud database integration
*   User authentication and history tracking
