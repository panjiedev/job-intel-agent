-- 创建职位信息表
CREATE TABLE IF NOT EXISTS job (
    id SERIAL PRIMARY KEY,
    job_name VARCHAR(255) NOT NULL,
    salary_desc VARCHAR(255),
    post_description TEXT,
    work_address VARCHAR(255),
    show_skills VARCHAR(255),
    experience_name VARCHAR(100),
    degree_name VARCHAR(100),
    position_name VARCHAR(255),
    embedding vector(1536) -- 词向量特征 (兼容 text-embedding-v3/qwen)
);

-- 创建简历信息表
CREATE TABLE IF NOT EXISTS resume (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(255),
    raw_content TEXT,
    core_skills TEXT,
    expected_position VARCHAR(255),
    embedding vector(1536), -- 简历的特征表达
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
