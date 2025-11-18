
from fastapi import FastAPI, Query
from sqlalchemy.orm import Session
from db import SessionLocal, ChatData

app = FastAPI(title="Simple Chatbot API")

@app.get("/chatbot/")
def chatbot(query: str = Query(..., description="Ask your question")):
    db: Session = SessionLocal()

    # Find matching problem (case-insensitive)
    result = db.query(ChatData).filter(ChatData.problem.ilike(f"%{query}%")).first()

    if not result:
        return {"query": query, "solution": "Sorry, I don’t have an answer for that."}

    return {"query": query, "solution": result.solution}
