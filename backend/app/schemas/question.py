from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class KnowledgePointBase(BaseModel):
    name: str
    category_id: int
    description: Optional[str] = None

class KnowledgePointCreate(KnowledgePointBase):
    pass

class KnowledgePointResponse(KnowledgePointBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    content: str
    question_type: str
    difficulty: str
    options: Optional[str] = None
    answer: str
    explanation: Optional[str] = None
    category_id: int
    knowledge_point_id: int

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    content: Optional[str] = None
    question_type: Optional[str] = None
    difficulty: Optional[str] = None
    options: Optional[str] = None
    answer: Optional[str] = None
    explanation: Optional[str] = None
    category_id: Optional[int] = None
    knowledge_point_id: Optional[int] = None

class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None
    knowledge_point: Optional[KnowledgePointResponse] = None
    
    class Config:
        from_attributes = True

class WrongQuestionBase(BaseModel):
    question_id: int
    my_answer: Optional[str] = None

class WrongQuestionCreate(WrongQuestionBase):
    pass

class WrongQuestionResponse(WrongQuestionBase):
    id: int
    error_count: int
    last_error_time: datetime
    is_marked: int
    created_at: datetime
    question: Optional[QuestionResponse] = None
    
    class Config:
        from_attributes = True

class PracticeRecordBase(BaseModel):
    question_id: int
    my_answer: Optional[str] = None
    is_correct: int
    duration: Optional[int] = None

class PracticeRecordCreate(PracticeRecordBase):
    pass

class PracticeRecordResponse(PracticeRecordBase):
    id: int
    practice_time: datetime
    question: Optional[QuestionResponse] = None
    
    class Config:
        from_attributes = True

class ApiResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[dict] = None

class PaginatedResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[dict] = None
    total: int = 0
    page: int = 1
    page_size: int = 10