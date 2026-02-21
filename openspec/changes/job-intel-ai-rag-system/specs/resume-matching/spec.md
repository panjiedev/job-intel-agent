## ADDED Requirements

### Requirement: 简历文本抽取与特征封装
支持接收用户上传的 .txt 或 .md 简历文件，依靠大模型或结构化抽取方式，将核心工作经验和技能特征转化为结构化文本及对应的 Embeddings。

#### Scenario: 用户上传合法简历文件
- **WHEN** 用户通过 Next.js 前端界面上传一份 2MB 以内的 `.txt` 简历
- **THEN** 后端 API `POST /api/resume/upload` 解析该文件内容
- **THEN** 后端通过大语言模型提取关键意图（期望岗位、已有技能等）
- **THEN** 提取结果转换为 Embedding，作为用户画像的向量特征

### Requirement: 职位智能推荐与 RAG
使用简历生成的向量查询 PostgreSQL 数据库，匹配相识度最高的 5 份职位，并生成对应的求职策略。

#### Scenario: 用户请求智能投递建议
- **WHEN** 简历解析完成，并发起一次职位匹配度分析请求
- **THEN** 系统调起 `pgvector` 的余弦相似度查询 `<=>`（或欧氏距离）计算最贴近的 N=5 份工作
- **THEN** 系统将这 5 份JD与候选人的简历拼接组成 Prompt，流式返回匹配短板与优势分析报告
