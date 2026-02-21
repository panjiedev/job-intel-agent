# 🎯 Job Intel RAG System (岗位情报智能体)

本项目旨在实现一个基于 **LLM (大语言模型)** 和 **RAG (检索增强生成)** 的岗位分析与求职规划智能体引擎。它不仅能结构化地存储经过抓取的职位信息，更能分析个人简历并依据最新的市场供需提供量身定制的技能补齐建议。

---

## 🏗️ 系统架构设计

当前系统从单体数据收集脚本完全升格为**现代化、前后端分离**的 AI-Native 形态：

*   **人工智能引擎**
    *   大语言模型 (LLM)：集成阿里云 DashScope (百炼平台) 提供的 **Qwen 系列**模型作为核心推理引擎，具备深度的中国职场经验理解能力。
    *   文本向量化 (Embeddings)：集成 `text-embedding-v3`，将冗长的 JD (Job Description) 和简历降维成具有数学相似度的特征空间。
    *   工作流编排：使用核心库 **LangChain 1.0+** 实现 Prompt 的流水线处理。
*   **后端服务 (Backend)**
    *   使用 **FastAPI** 搭建异步无阻塞的 API 服务。
    *   使用 **SQLAlchemy** 进行透明度极高的数据对象映射（ORM）。
    *   动态注入 **Prompt 引擎**，将复杂的提示语（Prompt-as-Code）隔离放置于 `prompts/` 目录中解耦。
*   **数据库引擎 (Persistence layer)**
    *   采用本地容器化的 **PostgreSQL 17** 作为主力。
    *   加载开源的 **`pgvector`** 插件，原生支持并高速缓存 `1536` 维度的稠密向量检索 (Vector Similarity Search)。
*   **交互前端 (Frontend)**
    *   使用基于 React 生态的 **Next.js 14** 搭建应用。
    *   接入 **Vercel AI SDK** 打造纯粹的 RAG 打字机即时响应（Streaming）效果。
    *   UI 使用 TailwindCSS 与 Lucide 图标快速响应设计。

---

## ✨ 核心功能流

1.  **📊 岗位信息自动化采集入库 (已交付)**
    *   支持用户（或者各类外部爬虫）上传采集到的 `.xlsx` Excel 数据表格。
    *   提供可视化映射规则：即便每张表格式不一，也可在前端映射成数据库中标准的 `job_name` 和 `post_description`，系统会自动拉取接口计算 Embedding 存入。
2.  **📝 简历剖析与意图抽取 (已交付)**
    *   上传个人的 Markdown/TXT 格式简历。
    *   系统大模型会直接摘取你的「最高优硬壳技能」和「求职意向打标」。
3.  **⚖️ 职场对标与 RAG 精准补强 (已交付)**
    *   系统使用你的简历特征，立刻前往 `pgvector` 中采用余弦相似度（Cosine Distance）计算出排名前五 (Top 5) 且为你量身定做的岗位。
    *   (未来演进): 指出你的能力短板，反推你未来一到三个月应该补齐的技能清单。

---

## ⚡ 快速启动指南

### 1. 启动基础设施 (PostgreSQL + pgvector)

请确保你的本地安装了 Docker，在项目根目录快速拉起带有向量检索功能的数据库缓存服务：
```bash
docker-compose up -d
```
> 此时本地将绑定 5432 端口并自带一个名为 `job_intel` 的初始数据库。用户名 `root`，密码 `123456`。初始化 SQL 脚本保存在 `docs/sql` 目录。

### 2. 启动 FastAPI 本地算法服务 (Backend)

系统对 Python 依赖较多，推荐通过 `venv` 执行（项目已配置好环境）：
```bash
# 激活环境
source venv/bin/activate

# 设定环境变量 (阿里云百炼 API KEY 必须配置才可触发向量分析)
export DASHSCOPE_API_KEY="sk-你的真实APIKey"
export PYTHONPATH=.

# 启动服务
uvicorn main:app --reload --port 8000
```
> API 服务运行在 `http://localhost:8000`

### 3. 连接 Next.js AI 工作台 (Frontend)

开启一个全新的终端界面，并进入 `web` 目录进行启动：
```bash
cd web

# 初次部署请安装依赖包 (npm install)
npm run dev
```
> AI 控制台默认运行在 `http://localhost:3000`

---

## 📁 核心目录指南

```text
job-intel-agent/
├── docker-compose.yml       # 核心服务环境编排 (PGVector)
├── docs/
│   └── sql/                 # 初始化表结构的 SQL 源头
├── openspec/                # 基于 OpenSpec 的任务设计工作流与阶段规划
├── prompts/                 # 统一在此处配置 yaml 格式的大模型提示词 
├── job_intel_agent/         # -> 后端逻辑中心
│   ├── api/                 # FastAPI 业务路由层 (/api/jobs, /api/resume) 
│   └── db/                  # SQLAchemy 连接映射
├── tests/                   # 包含基于 PyTest + TestClient 的全栈用例覆盖
└── web/                     # -> 表现层 Next.js 工程 (UI / Layouts)
```

## 🛠 未来规划 (Roadmap)
参见 `/docs/TASKS.md` 与 OpenSpec 的实施进度。未来将在市场公共特征反抽（共性分析图谱）中继续发力。
