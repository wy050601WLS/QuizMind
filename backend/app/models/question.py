from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))
    created_at = Column(DateTime, default=datetime.now)
    
    questions = relationship("Question", back_populates="category")

class KnowledgePoint(Base):
    __tablename__ = "knowledge_points"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.now)
    
    category = relationship("Category")
    questions = relationship("Question", back_populates="knowledge_point")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    question_type = Column(Enum("single", "multiple", "judge", "blank", name="question_type"), nullable=False)
    difficulty = Column(Enum("easy", "medium", "hard", name="difficulty_level"), nullable=False)
    options = Column(Text)
    answer = Column(String(500), nullable=False)
    explanation = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"))
    knowledge_point_id = Column(Integer, ForeignKey("knowledge_points.id"))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    category = relationship("Category", back_populates="questions")
    knowledge_point = relationship("KnowledgePoint", back_populates="questions")
    wrong_questions = relationship("WrongQuestion", back_populates="question")

class WrongQuestion(Base):
    __tablename__ = "wrong_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    my_answer = Column(String(500))
    error_count = Column(Integer, default=1)
    last_error_time = Column(DateTime, default=datetime.now)
    is_marked = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    
    question = relationship("Question", back_populates="wrong_questions")

class PracticeRecord(Base):
    __tablename__ = "practice_records"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    my_answer = Column(String(500))
    is_correct = Column(Integer, nullable=False)
    practice_time = Column(DateTime, default=datetime.now)
    duration = Column(Integer)
    
    question = relationship("Question")