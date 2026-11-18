# ExplainBot

ExplainBot is an AI-powered technical concept explainer that simplifies technical terms for different levels of understanding.

Users can enter a technical term, select an audience level, and receive a short explanation with an everyday analogy.

## Features

- Explains technical concepts at three levels: ELI5, Teenager, and Engineer.
- Uses Google Gemini to generate explanations.
- Uses prompt templates to control explanation style and structure.
- Validates generated responses for sentence count and analogy presence.
- Stores explanation history in PostgreSQL.
- Provides a simple web interface built with HTML, CSS, and JavaScript.
- Includes automated API tests and golden evaluation cases.

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| AI Model | Google Gemini API |
| Database | PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| Testing | Pytest |
| Version Control | Git, GitHub |

## Project Structure

```text
explainbot/
├── app/
│   ├── main.py
│   ├── llm.py
│   ├── database.py
│   └── prompt_builder.py
├── prompts/
│   └── explain_v1.txt
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── tests/
│   ├── golden_cases.json
│   ├── run_golden_eval.py
│   ├── test_main.py
│   └── test_validation.py
├── requirements.txt
└── .gitignore
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/RudranshMadaan/explainbot.git
cd explainbot
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_supported_gemini_model
DATABASE_URL=postgresql://username:password@localhost:5432/explainbot
```

Use your own credentials. Never commit `.env` to GitHub.

### 5. Set up PostgreSQL

Create a database named `explainbot` and run:

```sql
CREATE TABLE explain_history (
    id SERIAL PRIMARY KEY,
    term VARCHAR(120) NOT NULL,
    audience VARCHAR(20) NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6. Start the application

```powershell
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 in your browser.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Serve the web interface |
| GET | `/health` | Check application health |
| POST | `/api/explain` | Generate an explanation |
| GET | `/api/history` | Retrieve recent explanations |

## Run Tests

```powershell
python -m pytest -v
```

Run the golden evaluation separately:

```powershell
python tests/run_golden_eval.py
```

The golden evaluation uses the configured Gemini API and may consume API quota.

## Current Status

The application has a working FastAPI backend, PostgreSQL history storage, browser interface, response validation, and automated tests.

Deployment is not yet configured.

## Author

**Rudransh Madaan**

GitHub: https://github.com/RudranshMadaan
