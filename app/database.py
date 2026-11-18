
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from .env")


def get_connection():
    return psycopg.connect(DATABASE_URL)


def save_explanation(term: str, audience: str, answer: str):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO explain_history (term, audience, answer)
            VALUES (%s, %s, %s)
            """,
            (term, audience, answer)
        )


def get_recent_explanations(limit: int = 10):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, term, audience, answer, created_at
            FROM explain_history
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (limit,)
        ).fetchall()

    return [
        {
            "id": row[0],
            "term": row[1],
            "audience": row[2],
            "answer": row[3],
            "created_at": row[4]
        }
        for row in rows
    ]
