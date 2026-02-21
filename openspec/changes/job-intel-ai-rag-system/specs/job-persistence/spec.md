## CHANGED Requirements

### Requirement: Database 从只读 SQLite 切换为双模兼容模型，优先采用 Postgres (pgvector)
原系统完全基于单一的 SQLite `database.py`。
为了更好的生态，这里修改了存储层（Database 和 DAO）。引入 SQLAlchemy 作为 ORM 替代原生 SQL `execute`。

#### Scenario: DAO 初始化兼容不同存储引擎
- **WHEN** 环境变量配置 `DATABASE_URL=sqlite:///./test.db` 或 `DATABASE_URL=postgresql://user:pass@localhost:5432/job_intel`
- **THEN** Backend 系统通过依赖注入创建 DB Session
- **THEN** 若是 SQLite 模式，利用本地简易模型进行 CRUD，向量降级忽略或转接 Chroma；若是 PG 模式，自动启用 `vector` 数据类型的字段执行
- **THEN** 原有的 `JobDAO.insert` 需要重写采用 Pydantic+SQLAlchemy 持久化对象而非原生拼接 SQL 语句
