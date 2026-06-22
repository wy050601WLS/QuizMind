from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.question import WrongQuestion, Question
from ..schemas.question import WrongQuestionResponse, ApiResponse

router = APIRouter(prefix="/api", tags=["wrong-questions"])

@router.get("/wrong-questions")
def get_wrong_questions(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    subject: Optional[str] = None,
    knowledge_point_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(WrongQuestion)
    
    if subject:
        query = query.join(Question).join(Question.category).filter(
            Question.category.has(name=subject)
        )
    if knowledge_point_id:
        query = query.filter(Question.knowledge_point_id == knowledge_point_id)
    
    total = query.count()
    wrong_questions = query.order_by(WrongQuestion.last_error_time.desc()).offset(
        (page - 1) * page_size
    ).limit(page_size).all()
    
    return {
        "code": 200,
        "message": "success",
        "data": {"wrong_questions": [wq.__dict__ for wq in wrong_questions]},
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.get("/wrong-questions/{wrong_question_id}")
def get_wrong_question(wrong_question_id: int, db: Session = Depends(get_db)):
    wrong_question = db.query(WrongQuestion).filter(
        WrongQuestion.id == wrong_question_id
    ).first()
    if not wrong_question:
        raise HTTPException(status_code=404, detail="错题记录不存在")
    return {"code": 200, "message": "success", "data": wrong_question.__dict__}

@router.put("/wrong-questions/{wrong_question_id}/mark")
def mark_wrong_question(wrong_question_id: int, db: Session = Depends(get_db)):
    wrong_question = db.query(WrongQuestion).filter(
        WrongQuestion.id == wrong_question_id
    ).first()
    if not wrong_question:
        raise HTTPException(status_code=404, detail="错题记录不存在")
    
    wrong_question.is_marked = 1 if not wrong_question.is_marked else 0
    db.commit()
    return ApiResponse(message="标记成功")

@router.delete("/wrong-questions/{wrong_question_id}")
def delete_wrong_question(wrong_question_id: int, db: Session = Depends(get_db)):
    wrong_question = db.query(WrongQuestion).filter(
        WrongQuestion.id == wrong_question_id
    ).first()
    if not wrong_question:
        raise HTTPException(status_code=404, detail="错题记录不存在")
    
    db.delete(wrong_question)
    db.commit()
    return ApiResponse(message="删除成功")

@router.post("/wrong-questions/batch-delete")
def batch_delete_wrong_questions(ids: List[int], db: Session = Depends(get_db)):
    wrong_questions = db.query(WrongQuestion).filter(WrongQuestion.id.in_(ids)).all()
    for wq in wrong_questions:
        db.delete(wq)
    db.commit()
    return ApiResponse(message=f"成功删除{len(wrong_questions)}条记录")

@router.get("/wrong-questions/statistics")
def get_wrong_question_statistics(db: Session = Depends(get_db)):
    total_wrong = db.query(WrongQuestion).count()
    marked_wrong = db.query(WrongQuestion).filter(WrongQuestion.is_marked == 1).count()
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "total_wrong": total_wrong,
            "marked_wrong": marked_wrong
        }
    }