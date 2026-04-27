# AutoRubric AI

AutoRubric AI is an automated, AI-driven evaluation tool designed to provide intuitive, visual, and human-friendly feedback on student assignments. By leveraging a Large Language Model (LLM), it moves beyond simple scoring to offer deep insights, structured rubrics, and explainable reasoning for every evaluation.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Future Enhancements](#future-enhancements)

## Overview

Most AI evaluation tools overwhelm users with raw, unstructured text. AutoRubric AI is built with a focus on clarity and usability. It processes student answers against assignment prompts and returns a comprehensive evaluation dashboard that includes:

1.  **Overall Score**: A quick, visual representation of the student's performance.
2.  **Performance Metrics**: A radar chart breaking down the score into Clarity, Depth, and Relevance.
3.  **Constructive Feedback**: A meaningful, human-readable explanation of the score.
4.  **Detailed Rubric**: A transparent, tabular evaluation matrix detailing exactly how the score was calculated.

## Architecture

The project follows a decoupled client-server architecture:

-   **Frontend**: A modern, responsive, two-column web interface built with pure HTML, JavaScript, Tailwind CSS, Chart.js (for visualizations), and Marked.js (for parsing markdown rubrics).
-   **Backend**: A REST API built with Python and FastAPI. It receives evaluation requests, processes them using a local or cloud-based LLM, stores the results in a SQLite database, and returns structured JSON responses.

## Prerequisites

Before starting, ensure you have the following installed on your system:

-   Python 3.8 or higher
-   pip (Python package installer)
-   Git

## Installation and Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/autorubric-aii.git
    cd autorubric-aii
    ```

2.  **Set Up the Backend Environment**
    Navigate to the backend directory and create a virtual environment:
    ```bash
    cd backend
    python -m venv venv
    ```

3.  **Activate the Virtual Environment**
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4.  **Install Dependencies**
    Install the required Python packages from the requirements file:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure Environment Variables (Optional)**
    If your LLM setup requires specific API keys or endpoints, create a `.env` file in the `backend` directory based on your specific LLM integration.

## Running the Application

### 1. Start the Backend Server
Ensure your virtual environment is active and you are in the `backend` directory. Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 10000
```
The backend API will now be available at `http://localhost:10000`.

### 2. Start the Frontend
The frontend consists of static HTML and JavaScript files. You can serve them using any basic HTTP server. For example, open a new terminal, navigate to the `frontend` directory, and run:

```bash
cd frontend
python -m http.server 8000
```
Alternatively, you can simply open the `frontend/index.html` file directly in your web browser.

## Usage

1.  Open the frontend application in your web browser (e.g., `http://localhost:8000`).
2.  In the left pane, enter the **Assignment Prompt** (the question or task assigned to the student).
3.  Enter the **Student's Answer** in the provided text area.
4.  Click the **Generate Evaluation** button.
5.  Wait for the processing to complete. The right pane will populate with the score, charts, feedback, and the detailed rubric.

## Project Structure

```text
autorubric_aii/
├── backend/
│   ├── database.py       # SQLite database configuration and setup
│   ├── llm.py            # Integration logic for the Large Language Model
│   ├── main.py           # FastAPI application and routing endpoints
│   ├── metrics.py        # Scoring logic and metric calculations
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── app.js            # Frontend application logic and API calls
│   └── index.html        # Main user interface layout
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
```

## Future Enhancements

-   **Cloud LLM Integration**: Expand support beyond local LLMs to include managed services like OpenAI or Anthropic for improved speed and accuracy.
-   **Authentication**: Implement user accounts to save and track evaluation history across different sessions.
-   **Export Functionality**: Allow educators to export the generated rubrics and feedback as PDF or CSV files.
-   **Adaptive Feedback**: Tailor the tone and complexity of the feedback based on the student's grade level.
