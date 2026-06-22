from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import questions, practice, wrong_questions
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI智能刷题学习助手",
    description="面向学生群体的AI智能刷题学习工具",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(questions.router)
app.include_router(practice.router)
app.include_router(wrong_questions.router)

@app.get("/")
async def root():
    return {"message": "AI智能刷题学习助手API服务"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "服务运行正常"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"全局异常: {exc}")
    return {
        "code": 500,
        "message": "服务器内部错误",
        "data": None
    }