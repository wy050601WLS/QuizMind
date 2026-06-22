import httpx
import json
import os
import logging
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class AIServiceBase(ABC):
    """AI服务基类"""
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """生成AI响应"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """健康检查"""
        pass

class DoubaoService(AIServiceBase):
    """豆包大模型服务"""
    
    def __init__(self):
        self.api_key = os.getenv("DOUBAO_API_KEY", "")
        self.base_url = os.getenv("DOUBAO_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
        self.model = os.getenv("DOUBAO_MODEL", "doubao-pro-32k")
        self.timeout = 30
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """调用豆包API生成响应"""
        if not self.api_key:
            raise ValueError("豆包API密钥未配置")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "你是一个专业的教育助手，擅长出题、解析和学习指导。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 2000)
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data
                )
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
            except httpx.TimeoutException:
                logger.error("豆包API调用超时")
                raise
            except Exception as e:
                logger.error(f"豆包API调用失败: {e}")
                raise
    
    async def health_check(self) -> bool:
        """检查豆包服务状态"""
        try:
            await self.generate("你好", max_tokens=10)
            return True
        except Exception:
            return False

class QwenService(AIServiceBase):
    """通义千问服务"""
    
    def __init__(self):
        self.api_key = os.getenv("QWEN_API_KEY", "")
        self.base_url = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/api/v1")
        self.model = os.getenv("QWEN_MODEL", "qwen-turbo")
        self.timeout = 30
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """调用通义千问API生成响应"""
        if not self.api_key:
            raise ValueError("通义千问API密钥未配置")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "input": {
                "messages": [
                    {"role": "system", "content": "你是一个专业的教育助手，擅长出题、解析和学习指导。"},
                    {"role": "user", "content": prompt}
                ]
            },
            "parameters": {
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 2000)
            }
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/services/aigc/text-generation/generation",
                    headers=headers,
                    json=data
                )
                response.raise_for_status()
                result = response.json()
                return result["output"]["choices"][0]["message"]["content"]
            except httpx.TimeoutException:
                logger.error("通义千问API调用超时")
                raise
            except Exception as e:
                logger.error(f"通义千问API调用失败: {e}")
                raise
    
    async def health_check(self) -> bool:
        """检查通义千问服务状态"""
        try:
            await self.generate("你好", max_tokens=10)
            return True
        except Exception:
            return False

class MockAIService(AIServiceBase):
    """模拟AI服务（用于测试和降级）"""
    
    def __init__(self):
        self.responses = {
            "出题": "这是一道AI生成的题目：",
            "解析": "这道题的解析如下：",
            "建议": "根据你的学习情况，建议如下："
        }
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """返回模拟响应"""
        for key, value in self.responses.items():
            if key in prompt:
                return f"{value}\n\n[模拟AI响应] 当前使用的是模拟AI服务，请配置真实的AI API密钥以获取真实响应。"
        return "[模拟AI响应] 当前使用的是模拟AI服务，请配置真实的AI API密钥以获取真实响应。"
    
    async def health_check(self) -> bool:
        """模拟服务始终健康"""
        return True

class AIServiceFactory:
    """AI服务工厂"""
    
    _services = {}
    _default_service = None
    
    @classmethod
    def register_service(cls, name: str, service: AIServiceBase):
        """注册AI服务"""
        cls._services[name] = service
    
    @classmethod
    def get_service(cls, name: Optional[str] = None) -> AIServiceBase:
        """获取AI服务"""
        if name is None:
            name = cls._default_service or "mock"
        return cls._services.get(name, cls._services.get("mock"))
    
    @classmethod
    def set_default(cls, name: str):
        """设置默认服务"""
        cls._default_service = name
    
    @classmethod
    async def health_check_all(cls) -> Dict[str, bool]:
        """检查所有服务状态"""
        results = {}
        for name, service in cls._services.items():
            try:
                results[name] = await service.health_check()
            except Exception:
                results[name] = False
        return results

class AIService:
    """AI服务统一接口"""
    
    def __init__(self):
        self.factory = AIServiceFactory
        self._initialize_services()
    
    def _initialize_services(self):
        """初始化AI服务"""
        # 注册模拟服务
        self.factory.register_service("mock", MockAIService())
        
        # 注册豆包服务
        doubao_service = DoubaoService()
        self.factory.register_service("doubao", doubao_service)
        
        # 注册通义千问服务
        qwen_service = QwenService()
        self.factory.register_service("qwen", qwen_service)
        
        # 设置默认服务
        default_provider = os.getenv("AI_PROVIDER", "mock")
        self.factory.set_default(default_provider)
    
    async def generate_question(self, subject: str, knowledge_point: str, 
                              question_type: str, difficulty: str, 
                              count: int = 1) -> Dict[str, Any]:
        """生成题目"""
        prompt = f"""请生成{count}道{subject}科目{knowledge_point}知识点的{question_type}题目，难度为{difficulty}。

要求：
1. 题目内容清晰准确
2. 选项合理（如果是选择题）
3. 提供正确答案
4. 提供详细解析

请以JSON格式返回，格式如下：
{{
    "questions": [
        {{
            "content": "题目内容",
            "options": ["选项A", "选项B", "选项C", "选项D"],
            "answer": "正确答案",
            "explanation": "解析"
        }}
    ]
}}"""
        
        service = self.factory.get_service()
        response = await service.generate(prompt)
        
        try:
            # 尝试解析JSON响应
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            # 如果不是有效JSON，返回原始响应
            return {"raw_response": response}
    
    async def analyze_wrong_question(self, question: str, user_answer: str, 
                                   correct_answer: str) -> Dict[str, Any]:
        """分析错题"""
        prompt = f"""学生做错了以下题目：

题目：{question}
学生答案：{user_answer}
正确答案：{correct_answer}

请分析：
1. 错误原因
2. 知识点拆解
3. 易错点提醒
4. 学习建议

请以JSON格式返回，格式如下：
{{
    "error_reason": "错误原因",
    "knowledge_points": ["知识点1", "知识点2"],
    "mistake_tips": "易错点提醒",
    "suggestions": ["建议1", "建议2"]
}}"""
        
        service = self.factory.get_service()
        response = await service.generate(prompt)
        
        try:
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            return {"raw_response": response}
    
    async def generate_learning_suggestions(self, wrong_questions: list, 
                                         knowledge_points: list) -> Dict[str, Any]:
        """生成学习建议"""
        prompt = f"""根据学生的学习数据生成个性化学习建议：

错题数量：{len(wrong_questions)}道
涉及知识点：{', '.join(knowledge_points[:5])}

请分析学生的学习薄弱点，并提供：
1. 知识点掌握度排名
2. 个性化学习建议
3. 巩固方向

请以JSON格式返回，格式如下：
{{
    "mastery_ranking": [
        {{"point": "知识点", "mastery": 60, "suggestion": "建议"}}
    ],
    "learning_suggestions": ["建议1", "建议2"],
    "consolidation_directions": ["方向1", "方向2"]
}}"""
        
        service = self.factory.get_service()
        response = await service.generate(prompt)
        
        try:
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            return {"raw_response": response}
    
    async def generate_exam_paper(self, subject: str, scope: str,
                                 question_types: Dict[str, float],
                                 difficulty_distribution: Dict[str, float],
                                 total_score: int) -> Dict[str, Any]:
        """生成模拟试卷"""
        prompt = f"""请生成一份{subject}科目的模拟试卷：

考试范围：{scope}
题型分布：{json.dumps(question_types, ensure_ascii=False)}
难度分布：{json.dumps(difficulty_distribution, ensure_ascii=False)}
总分：{total_score}分

请生成完整的试卷，包括：
1. 各题型的题目
2. 分值分配
3. 参考答案
4. 评分标准

请以JSON格式返回，格式如下：
{{
    "title": "试卷标题",
    "total_score": {total_score},
    "questions": [
        {{
            "type": "题型",
            "content": "题目内容",
            "options": ["选项"],
            "answer": "答案",
            "score": 10,
            "explanation": "解析"
        }}
    ],
    "scoring_criteria": "评分标准"
}}"""
        
        service = self.factory.get_service()
        response = await service.generate(prompt)
        
        try:
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            return {"raw_response": response}
    
    async def health_check(self) -> Dict[str, bool]:
        """检查所有AI服务状态"""
        return await self.factory.health_check_all()

# 全局AI服务实例
ai_service = AIService()