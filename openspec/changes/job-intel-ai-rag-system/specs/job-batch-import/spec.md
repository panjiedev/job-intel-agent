## ADDED Requirements

### Requirement: 动态 Excel 列名映射入库
对于不使用 RPA 自动化而是单独使用 Excel 文件导入的情况，允许用户自定义表头到数据库的字段映射。

#### Scenario: 映射字典校验和录入
- **WHEN** 提交前端的字段隐射关系如（'职位描述': 'post_description'）进行批量 `POST /api/jobs/import`
- **THEN** 后端使用 pydantic 模型进行动态匹配及格式校验
- **THEN** 合格数据开始进入入库程序

### Requirement: 同步生成职位数据 Embedding 
为了支持向量搜索，必须在 Job 的核心文本字段上提取 Embedding。

#### Scenario: 异步填充向量字段
- **WHEN** 每当有一条新职位将要写入关系型数据库
- **THEN** 系统调取 `DashScope Embeddings API` 生成该条目的维度特征（长度 1536 左右）
- **THEN** 特征数值写入对应职位记录的 Vector 类型的 `embedding` 字段
