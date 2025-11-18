
from fastapi import FastAPI, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from sqlalchemy import or_
from db import SessionLocal, ChatData
import re

app = FastAPI(title="Simple Chatbot API")

@app.get("/chatbot/")
def chatbot(query: str = Query(..., description="Ask your question")):
    db: Session = SessionLocal()
    try:
        # Tokenize query, remove common stopwords, and require all tokens to appear
        tokens = [t for t in re.findall(r"\w+", query.lower()) if t not in {"the", "a", "to", "how", "what", "is", "of", "in", "and", "for"}]

        if tokens:
            filters = [func.lower(ChatData.problem).like(f"%{t}%") for t in tokens]
            result = db.query(ChatData).filter(or_(*filters)).first()
        else:
            # fallback to full-query substring match
            result = db.query(ChatData).filter(func.lower(ChatData.problem).like(f"%{query.lower()}%")).first()

        if not result:
            return {"query": query, "solution": "Sorry, I don’t have an answer for that."}

        return {"query": query, "solution": result.solution}
    finally:
        db.close()
