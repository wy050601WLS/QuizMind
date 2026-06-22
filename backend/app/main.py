from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .database import engine, Base
from .routers import questions, practice, wrong_questions, ai
import logging
import traceback
import os

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

# CORS 配置，支持环境变量
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(questions.router)
app.include_router(practice.router)
app.include_router(wrong_questions.router)
app.include_router(ai.router)

@app.get("/")
async def root():
    return {"message": "AI智能刷题学习助手API服务"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "服务运行正常"}

# ValueError 异常处理器（放在 Exception 之前）
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    logger.warning(f"参数错误: {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "code": 400,
            "message": str(exc),
            "data": None
        }
    )

# 全局异常处理器
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"全局异常: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }
    )