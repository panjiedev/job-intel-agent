## Why

项目需要从基础的职位抓取进阶为智能化的“个人求职与职场规划引擎”。
通过引入大语言模型（LLM）和检索增强生成（RAG）能力，系统能够理解简历、匹配职位、分析市场共性，并为用户提供针对性的学习与面试准备建议。

## What Changes

1. **引入 AI 基础设施**：集成 LangChain，提供基于 Qwen 的大模型推理服务和基于 PostgreSQL (pgvector) 的文本向量检索能力。
2. **职位数据的动态投递与向量化**：支持通过 Excel 映射上传职位，并自动生成职位描述的 Embedding 存入数据库。
3. **简历解析与匹配度引擎**：支持上传简历文件文本，借助 RAG 引擎对比简历向量与职位库向量，提取核心能力 Gap。
4. **市场共性与反向规划**：分析批量指定职位的共性技能树，并根据用户简历薄弱点，依托大模型自动生成 1~3 个月的提升规划。
5. **重构项目架构**：采用前后端分离架构，前端引入 Next.js 14 与 Vercel AI SDK 构建 AI Native 交互；后端依托 FastAPI 与 SQLAlchemy 提供支撑。

## Capabilities

### New Capabilities
- `resume-matching`: 简历上传、解析、与职位库基于 pgvector 的 RAG 匹配及优劣势分析。
- `job-batch-import`: 由第三方来源抓取的职位 Excel 的动态映射与批量入库，同步生成 Embedding。
- `market-analysis`: 针对检索后批量职位的共性分析和技能点归纳，辅以反转简历视角的补充学习建议。

### Modified Capabilities
- `job-persistence`: 改造现有的基于 sqlite 的存储层向 PostgreSQL 迁移，引入 ORM 和 Vector 类型字段管理。

## Impact
- **代码结构**：新增 `prompts` 目录专门管理大模型提示词（YAML 格式）。
- **环境依赖**：引入 `docker-compose`，集成本地 `pgvector/pgvector:17` 及后续前端/后端的隔离部署。大模型推理接入云端阿里云百炼 (DashScope) `/v1/chat/completions` 和 `/v1/embeddings`。
- **核心框架**：引入 Next.js 到前端工程体系，彻底改造项目展示层面。后端采用 FastAPI 替换纯命令行单点脚本流向。
