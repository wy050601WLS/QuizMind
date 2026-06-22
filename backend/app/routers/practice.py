from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from ..database import get_db
from ..models.question import PracticeRecord, Question, WrongQuestion
from ..schemas.question import PracticeRecordCreate, PracticeRecordResponse, ApiResponse

router = APIRouter(prefix="/api", tags=["practice"])

@router.post("/practice/submit", response_model=ApiResponse)
def submit_answer(record: PracticeRecordCreate, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == record.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")
    
    is_correct = 1 if record.my_answer == question.answer else 0
    
    db_record = PracticeRecord(
        question_id=record.question_id,
        my_answer=record.my_answer,
        is_correct=is_correct,
        duration=record.duration
    )
    db.add(db_record)
    
    if not is_correct:
        existing_wrong = db.query(WrongQuestion).filter(
            WrongQuestion.question_id == record.question_id
        ).first()
        
        if existing_wrong:
            existing_wrong.error_count += 1
            existing_wrong.last_error_time = datetime.now()
            existing_wrong.my_answer = record.my_answer
        else:
            db_wrong = WrongQuestion(
                question_id=record.question_id,
                my_answer=record.my_answer,
                error_count=1
            )
            db.add(db_wrong)
    
    db.commit()
    return ApiResponse(message="提交成功", data={"is_correct": is_correct})

@router.get("/practice/records")
def get_practice_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    days: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(PracticeRecord)
    
    if days:
        start_date = datetime.now() - timedelta(days=days)
        query = query.filter(PracticeRecord.practice_time >= start_date)
    
    total = query.count()
    records = query.order_by(PracticeRecord.practice_time.desc()).offset(
        (page - 1) * page_size
    ).limit(page_size).all()
    
    return {
        "code": 200,
        "message": "success",
        "data": {"records": [{k: v for k, v in r.__dict__.items() if not k.startswith('_')} for r in records]},
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.get("/practice/statistics")
def get_practice_statistics(days: Optional[int] = 7, db: Session = Depends(get_db)):
    start_date = datetime.now() - timedelta(days=days)
    
    total_records = db.query(PracticeRecord).filter(
        PracticeRecord.practice_time >= start_date
    ).count()
    
    correct_records = db.query(PracticeRecord).filter(
        PracticeRecord.practice_time >= start_date,
        PracticeRecord.is_correct == 1
    ).count()
    
    correct_rate = (correct_records / total_records * 100) if total_records > 0 else 0
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "total_questions": total_records,
            "correct_count": correct_records,
            "correct_rate": round(correct_rate, 2)
        }
    }

@router.get("/practice/daily-stats")
def get_daily_stats(days: int = 7, db: Session = Depends(get_db)):
    from sqlalchemy import func, cast, Date
    
    start_date = datetime.now() - timedelta(days=days)
    
    daily_stats = db.query(
        cast(PracticeRecord.practice_time, Date).label("date"),
        func.count(PracticeRecord.id).label("count"),
        func.sum(PracticeRecord.is_correct).label("correct_count")
    ).filter(
        PracticeRecord.practice_time >= start_date
    ).group_by(
        cast(PracticeRecord.practice_time, Date)
    ).all()
    
    result = []
    for stat in daily_stats:
        result.append({
            "date": str(stat.date),
            "count": stat.count,
            "correct_count": stat.correct_count or 0,
            "correct_rate": round((stat.correct_count or 0) / stat.count * 100, 2) if stat.count > 0 else 0
        })
    
    return {
        "code": 200,
        "message": "success",
        "data": {"daily_stats": result}
    }