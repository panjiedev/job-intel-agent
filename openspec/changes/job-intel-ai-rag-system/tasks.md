## 1. 环境与数据库层建设

- [x] 1.1 编写 `docs/sql/01_init_pgvector.sql` 和 `02_create_job_tables.sql`，定义 Job 和 Resume 表及 `embedding vector(1536)` 字段。
- [x] 1.2 编写项目根目录下的 `docker-compose.yml`，编排 `pgvector` 服务和网络。
- [x] 1.3 改造 `job_intel_agent/db/database.py`，引入 SQLAlchemy 连接池，支持读取环境变量在 SQLite 和 Postgres 间透明切换。
- [x] 1.4 编写针对 DB 连接和基础 CRUD 的 Pytest 单元测试。

## 2. 后端核心机制引入 (FastAPI & LangChain)

- [x] 2.1 引入 FastAPI 框架并重构现有的单测脚本，搭建起 `app.py` 或 `main.py` 入口点。
- [x] 2.2 定义统一样板提示词管理仓库，建立 `prompts/job_keyword_extraction.yaml` 等基础配置占位符。
- [x] 2.3 集成 LangChain 并对接阿里云 DashScope `/v1/chat/completions` (Qwen) 和 `/v1/embeddings` 接口层。

## 3. 面向业务链的 RAG 开发

- [ ] 3.1 开发 `/api/jobs/import` 接口：接收前端传来的 Excel 字典隐射并做 pydantic 校验和落库，同时调用 Embedding API 存储文本词距。
- [ ] 3.2 开发 `/api/resume/upload` 接口：接收 Markdown 或 TXT 提取全文转存为用户 Profile 并向量化。
- [ ] 3.3 开发职位匹配端点：使用用户简历的 Embedding 在 `pgvector` 中通过余弦相似度算出 Top 5 职位。
- [ ] 3.4 串联匹配分析 Prompt，流式（Streaming）返回匹配劣势及规划。
- [ ] 3.5 编写涵盖 Excel 读取、相似度比对、以及利用 pytest-mock 切断 LangChain 的本地断言与测试。

## 4. 前端应用重构 (Next.js)

- [ ] 4.1 在项目根目录使用 `npx create-next-app` 生成一个新的 web 工程（含 Tailwind/Typescript）。
- [ ] 4.2 引入 `ai` (Vercel AI SDK) 及 `lucide-react`。开发基础的 Layout 和路由体系。
- [ ] 4.3 实现职位批量导入的数据表格 Mapping UI。
- [ ] 4.4 实现简历上传页以及“结果看板”。呈现从后端返回的流式 Markdown 格式分析报告。
- [ ] 4.5 与本地 Docker 启动的后端接口联调。
