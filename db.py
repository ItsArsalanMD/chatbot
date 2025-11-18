
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file (you can change this to MSSQL or PostgreSQL)
DATABASE_URL = "sqlite:///./chatbot.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class ChatData(Base):
    __tablename__ = "chat_data"
    id = Column(Integer, primary_key=True, index=True)
    problem = Column(Text)
    solution = Column(Text)

Base.metadata.create_all(bind=engine)