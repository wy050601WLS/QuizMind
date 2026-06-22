from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from ..database import get_db
from ..services.ai_service import ai_service
from ..models.question import Question, WrongQuestion, KnowledgePoint

router = APIRouter(prefix="/api/ai", tags=["ai"])

class QuestionGenerateRequest(BaseModel):
    subject: str
    knowledge_point: str
    question_type: str = "single"
    difficulty: str = "medium"
    count: int = 1

class WrongQuestionAnalyzeRequest(BaseModel):
    question_id: int
    user_answer: str

class ExamPaperRequest(BaseModel):
    subject: str
    scope: str
    question_types: Dict[str, float] = {"single": 0.6, "multiple": 0.2, "judge": 0.2}
    difficulty_distribution: Dict[str, float] = {"easy": 0.3, "medium": 0.5, "hard": 0.2}
    total_score: int = 100

@router.get("/health")
async def health_check():
    """检查AI服务状态"""
    try:
        results = await ai_service.health_check()
        return {
            "code": 200,
            "message": "success",
            "data": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"健康检查失败: {str(e)}")

@router.post("/generate-question")
async def generate_question(request: QuestionGenerateRequest):
    """AI生成题目"""
    try:
        result = await ai_service.generate_question(
            subject=request.subject,
            knowledge_point=request.knowledge_point,
            question_type=request.question_type,
            difficulty=request.difficulty,
            count=request.count
        )
        return {
            "code": 200,
            "message": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成题目失败: {str(e)}")

@router.post("/analyze-wrong-question")
async def analyze_wrong_question(
    request: WrongQuestionAnalyzeRequest,
    db: Session = Depends(get_db)
):
    """AI分析错题"""
    try:
        # 获取题目信息
        question = db.query(Question).filter(Question.id == request.question_id).first()
        if not question:
            raise HTTPException(status_code=404, detail="题目不存在")
        
        result = await ai_service.analyze_wrong_question(
            question=question.content,
            user_answer=request.user_answer,
            correct_answer=question.answer
        )
        return {
            "code": 200,
            "message": "success",
            "data": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析错题失败: {str(e)}")

@router.post("/generate-suggestions")
async def generate_suggestions(db: Session = Depends(get_db)):
    """AI生成学习建议"""
    try:
        # 获取错题数据
        wrong_questions = db.query(WrongQuestion).limit(50).all()
        
        # 获取涉及的知识点
        knowledge_points = []
        for wq in wrong_questions:
            if wq.question and wq.question.knowledge_point:
                knowledge_points.append(wq.question.knowledge_point.name)
        
        knowledge_points = list(set(knowledge_points))
        
        result = await ai_service.generate_learning_suggestions(
            wrong_questions=[{"id": wq.id} for wq in wrong_questions],
            knowledge_points=knowledge_points
        )
        return {
            "code": 200,
            "message": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成学习建议失败: {str(e)}")

@router.post("/generate-exam")
async def generate_exam(request: ExamPaperRequest):
    """AI生成模拟试卷"""
    try:
        result = await ai_service.generate_exam_paper(
            subject=request.subject,
            scope=request.scope,
            question_types=request.question_types,
            difficulty_distribution=request.difficulty_distribution,
            total_score=request.total_score
        )
        return {
            "code": 200,
            "message": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成试卷失败: {str(e)}")