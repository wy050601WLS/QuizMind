from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.question import Question, Category, KnowledgePoint
from ..schemas.question import (
    QuestionCreate, QuestionUpdate, QuestionResponse,
    CategoryCreate, CategoryResponse,
    KnowledgePointCreate, KnowledgePointResponse,
    ApiResponse, PaginatedResponse
)

router = APIRouter(prefix="/api", tags=["questions"])

@router.get("/questions", response_model=PaginatedResponse)
def get_questions(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    subject: Optional[str] = None,
    question_type: Optional[str] = None,
    difficulty: Optional[str] = None,
    knowledge_point_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Question)
    
    if subject:
        query = query.join(Category).filter(Category.name == subject)
    if question_type:
        query = query.filter(Question.question_type == question_type)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    if knowledge_point_id:
        query = query.filter(Question.knowledge_point_id == knowledge_point_id)
    
    total = query.count()
    questions = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return PaginatedResponse(
        data={"questions": [q.__dict__ for q in questions]},
        total=total,
        page=page,
        page_size=page_size
    )

@router.get("/questions/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")
    return question

@router.post("/questions", response_model=QuestionResponse)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    db_question = Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.put("/questions/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int,
    question: QuestionUpdate,
    db: Session = Depends(get_db)
):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="题目不存在")
    
    update_data = question.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_question, key, value)
    
    db.commit()
    db.refresh(db_question)
    return db_question

@router.delete("/questions/{question_id}", response_model=ApiResponse)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="题目不存在")
    
    db.delete(db_question)
    db.commit()
    return ApiResponse(message="删除成功")

@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.post("/categories", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/knowledge-points", response_model=List[KnowledgePointResponse])
def get_knowledge_points(
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(KnowledgePoint)
    if category_id:
        query = query.filter(KnowledgePoint.category_id == category_id)
    return query.all()

@router.post("/knowledge-points", response_model=KnowledgePointResponse)
def create_knowledge_point(
    knowledge_point: KnowledgePointCreate,
    db: Session = Depends(get_db)
):
    db_kp = KnowledgePoint(**knowledge_point.dict())
    db.add(db_kp)
    db.commit()
    db.refresh(db_kp)
    return db_kp