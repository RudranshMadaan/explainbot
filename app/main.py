
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.llm import generate_explanation
from app.prompt_builder import build_prompt
from app.database import save_explanation, get_recent_explanations
app = FastAPI(
    title="ExplainBot API",
    description="Explain technical concepts at different difficulty levels",
    version="1.0.0"
)
BASE_DIR = Path(__file__).resolve().parent.parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

# Request structure
class ExplainRequest(BaseModel):
    term: str = Field(min_length=1, max_length=120)
    audience: Literal["eli5", "teenager", "engineer"]


# Response structure
class ExplainResponse(BaseModel):
    term: str
    answer: str


# Main explanation endpoint

@app.post("/api/explain", response_model=ExplainResponse)
def explain(body: ExplainRequest):

    term = body.term.strip()

    if not term:
        raise HTTPException(
            status_code=422,
            detail="Term cannot be empty"
        )

    try:
        prompt = build_prompt(term, body.audience)
        answer = generate_explanation(prompt)

        save_explanation(term, body.audience, answer)

        return ExplainResponse(
            term=term,
            answer=answer
        )

    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))

@app.get("/api/history")
def history():
    try:
        return get_recent_explanations()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve explanation history"
        )


# Health check
@app.get("/health")
def health():
    return {"ok": True}


# Home route
@app.get("/")
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")
