## Context

当前项目能够基于简单的 SQLite 数据库实现对职位信息的 CRUD 管理，并提出了向岗位智库以及智能体转变的目标。
然而，当前架构缺乏高级的大模型接入（如文本向量化、RAG 检索、简历解析整合）。在此次设计中，将基于原先的基础实现系统层面的重构：从单体 Python 脚本升级为前后端分离的现代化架构，并在本地通过 Docker 的形式提供 Postgres（携带 pgvector）服务，以支撑智能分析和求职准备的闭环。

## Goals / Non-Goals

**Goals:**
- 实现端到端的前后端分离架构，采用 Next.js 构建交互，FastAPI 承担逻辑引擎与 API 提供者。
- 设计支持文本向量检索的 PostgreSQL (pgvector) 存储，同时支持与原有的 SQLite 构建双模兼容的代码层。
- 基于 LangChain 结合 DashScope (Qwen 大模型 API) 编排 RAG 业务流（包含：简历向量检索、相似度判定、求职短板提取与规划规划）。
- 定义标准的 Prompt 组织方式，将业务大纲和模版放到外置 yaml 设计。

**Non-Goals:**
- 开发现成的高可用 SaaS 服务（侧重本地化 Docker 部署研究）。
- 自主研发强大的网页自动化爬取（目前核心以手工/外部爬取的 Excel 映射录入替代）。

## Decisions

1. **前端技术选型**：选用 Next.js 14 (App Router) 配合 Vercel AI SDK，作为当前最高效也是生态最全的 AI Native 框架，并引入 Tailwind CSS 进行极速响应式绘制。
2. **大模型部署形态**：为了降低本地计算压迫与兼顾性能，不使用本地 Ollama 驱动核心模型，转而在代码中对接阿里云服务 DashScope 下的 Qwen 系列大语言模型及其 Embedding 模型（接口遵循 OpenAI 标准）。
3. **数据库存储方案**：以 `pgvector/pgvector:17` Docker 容器为主力数据池，同时借助 SQLAlchemy 的强适应性，保留 SQLite + 本地 ChromaDB（降级方案） 作为无需容器时的实验环境备份。
4. **提示词托管 (Prompt-as-Code)**：建立 `prompts/` 单独存放 `.yaml` 模板文件。
5. **Excel 数据处理入库**：采用 pandas 配合 pydantic 验证快速清洗数据并映射数据库表结构，同时利用异步请求并发获取文本向量以提高入库效率。

## Risks / Trade-offs

- **学习曲线增加**：引入多个新技术栈（Next.js, LangChain, PostgreSQL）可能导致代码行数增加和初期开发门槛提升。
- **依赖网络**：依托阿里云大模型意味着系统在纯断网环境下无法进行推理与 Embedding 操作。需要有合理的降级或重定向配置能力。
