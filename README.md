# AI智能刷题学习助手

## 项目简介
面向学生群体的AI智能刷题学习工具，围绕"出题-刷题-纠错-巩固"的学习闭环，结合大模型AI能力实现灵活出题、智能解析、个性化学习建议。

## 技术栈
- **前端**：Vue 3 + Vite + Element Plus + ECharts
- **后端**：Python FastAPI
- **数据库**：SQLite
- **AI能力**：豆包大模型API / 通义千问API
- **容器化**：Docker + Docker Compose

## 项目结构

```
QuizMind/
├── frontend/          # 前端项目
│   ├── src/
│   │   ├── api/       # API接口
│   │   ├── components/# 组件
│   │   ├── router/    # 路由
│   │   ├── stores/    # 状态管理
│   │   ├── utils/     # 工具类
│   │   └── views/     # 页面
│   ├── Dockerfile
│   └── package.json
├── backend/           # 后端项目
│   ├── app/
│   │   ├── models/    # 数据模型
│   │   ├── routers/   # 路由
│   │   ├── schemas/   # 数据模式
│   │   ├── services/  # 服务
│   │   └── utils/     # 工具类
│   ├── init_db.py     # 数据库初始化
│   ├── run.py         # 启动脚本
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml # Docker编排配置
├── 任务文档.md
├── 项目.md
├── 项目历程文档.md
└── 数据库设计文档.md
```

## 快速开始

### 方式一：本地开发

#### 1. 启动后端

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（可选）
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动后端服务
python run.py
```

后端服务将在 http://localhost:8000 启动

#### 2. 启动前端

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 http://localhost:3000 启动

#### 3. 访问应用

打开浏览器访问 http://localhost:3000

### 方式二：Docker部署

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看运行状态
docker-compose ps

# 停止服务
docker-compose down
```

访问 http://localhost:3000 即可使用

## 功能模块

### 已完成功能
- ✅ 前端项目骨架搭建
- ✅ 后端项目骨架搭建
- ✅ 数据库设计与初始化
- ✅ 前端基础页面框架
- ✅ 前后端联调验证
- ✅ 题库管理功能（CRUD、筛选、分页）
- ✅ 刷题练习功能（多种题型、进度跟踪）
- ✅ 错题本功能（错题管理、标记、查看解析）
- ✅ 学习统计功能（数据可视化、趋势图）
- ✅ AI智能出题功能
- ✅ 错题AI解析功能
- ✅ 薄弱点总结功能
- ✅ AI模拟组卷功能
- ✅ Docker容器化部署

### 待开发功能
- 🔄 多用户支持
- 🔄 更多AI模型支持

## API接口

### 健康检查
- `GET /api/health` - 检查服务状态

### 题目管理
- `GET /api/questions` - 获取题目列表
- `GET /api/questions/{id}` - 获取题目详情
- `POST /api/questions` - 创建题目
- `PUT /api/questions/{id}` - 更新题目
- `DELETE /api/questions/{id}` - 删除题目

### 分类管理
- `GET /api/categories` - 获取分类列表
- `POST /api/categories` - 创建分类

### 知识点管理
- `GET /api/knowledge-points` - 获取知识点列表
- `POST /api/knowledge-points` - 创建知识点

### 练习记录
- `POST /api/practice/submit` - 提交答案
- `GET /api/practice/records` - 获取练习记录
- `GET /api/practice/statistics` - 获取练习统计
- `GET /api/practice/daily-stats` - 获取每日统计

### 错题管理
- `GET /api/wrong-questions` - 获取错题列表
- `PUT /api/wrong-questions/{id}/mark` - 标记错题
- `DELETE /api/wrong-questions/{id}` - 删除错题
- `POST /api/wrong-questions/batch-delete` - 批量删除错题
- `GET /api/wrong-questions/statistics` - 获取错题统计

### AI功能
- `GET /api/ai/health` - 检查AI服务状态
- `POST /api/ai/generate-question` - AI生成题目
- `POST /api/ai/analyze-wrong-question` - AI分析错题
- `POST /api/ai/generate-suggestions` - AI生成学习建议
- `POST /api/ai/generate-exam` - AI生成模拟试卷

## 环境变量配置

### 后端环境变量
创建 `backend/.env` 文件：

```env
# 数据库配置
DATABASE_URL=sqlite:///./ai_study.db

# AI服务配置
AI_PROVIDER=mock  # 可选: mock, doubao, qwen

# 豆包大模型配置
DOUBAO_API_KEY=your_api_key
DOUBAO_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
DOUBAO_MODEL=doubao-pro-32k

# 通义千问配置
QWEN_API_KEY=your_api_key
QWEN_BASE_URL=https://dashscope.aliyuncs.com/api/v1
QWEN_MODEL=qwen-turbo
```

### 前端环境变量
创建 `frontend/.env.development` 文件：

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## 开发规范

### 代码规范
- 前端：遵循Vue 3官方风格指南
- 后端：遵循PEP 8 Python代码规范
- 注释：核心类、函数、接口配备完整注释

### 提交规范
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 重构
- test: 测试相关
- chore: 构建/工具相关

## 常见问题

### 1. 后端启动失败
- 检查Python版本（推荐3.8+）
- 检查依赖是否安装完整
- 检查端口8000是否被占用

### 2. 前端启动失败
- 检查Node.js版本（推荐16+）
- 检查依赖是否安装完整
- 检查端口3000是否被占用

### 3. 前后端无法通信
- 确保后端服务已启动
- 检查CORS配置
- 检查API地址配置

### 4. Docker部署问题
- 确保Docker已安装
- 检查端口是否被占用
- 查看日志：`docker-compose logs`

## 更新日志

### 2026-06-22
- 完成项目初始化
- 搭建前后端骨架
- 实现基础页面框架
- 完成数据库设计
- 实现核心业务功能
- 集成AI能力
- 添加Docker容器化部署

---
*项目文档 - 2026年6月22日*