## ADDED Requirements

### Requirement: 基于关键词的市场技能特征汇聚
当用户想要针对例如 "Python 后端开发" 方向分析时，能够通过关键词搜索目标岗位群落，交由大语言模型提炼公共关键词（如 FastAPI, MySQL, Redis 等的百分比占比或并集提取）。

#### Scenario: 用户搜索一个行业词并触发分析
- **WHEN** 用户使用关键词或复合筛选（例如经验: 3-5年，标签: 前端）向后端请求
- **THEN** 后端从 SQLite 或 Postgres 中提取此批职位的 `post_description` / `show_skills`
- **THEN** 将批量文本浓缩（提示词映射），并调用 Qwen 产出“归属于该方向的最核心 Top N 技能项”

### Requirement: 逆向匹配用户的求职方向
利用提取出的公共市场技能项与用户本身存储入库的简历进行“能力相减减法”。由于使用了 RAG 和 LLM 可以实现较为宽泛的等价概念替代判断（而不仅仅是字面匹配）。

#### Scenario: 自动生成补齐计划
- **WHEN** 市场分析完成
- **THEN** `GET /api/market/analysis/plan` 被调用，并同时注入简历信息
- **THEN** LLM 生成一份阶段计划表：如第一周补充何种框架，第二周精进哪些能力，并以结构化 Markdown（甚至 JSON）传回前端绘制雷达图或时间线
