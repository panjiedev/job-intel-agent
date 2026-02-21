import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from job_intel_agent.db.database import Base, get_db
from job_intel_agent.db.models import Job, Resume

# 我们使用 testcontainers 来创建一个临时的 postgres, 或者直接使用本地的 job_intel_pgvector 进行测试。
# 既然已经有本地的了，直接用那个即可。

DB_URL = os.environ.get("TEST_DATABASE_URL", "postgresql://root:123456@localhost:5432/job_intel")

engine = create_engine(DB_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_session():
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # 清除数据
        Base.metadata.drop_all(bind=engine)

def test_database_connection_and_crud(db_session):
    # 测试插入 JOB
    job = Job(
        job_name="测试职位",
        post_description="这是一个测试职位描述",
        salary_desc="10k-20k"
    )
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)
    
    assert job.id is not None
    assert job.job_name == "测试职位"
    
    # 测试获取 JOB
    fetched_job = db_session.query(Job).filter(Job.id == job.id).first()
    assert fetched_job is not None
    assert fetched_job.job_name == "测试职位"

    # 测试删除
    db_session.delete(fetched_job)
    db_session.commit()
    
    deleted_job = db_session.query(Job).filter(Job.id == job.id).first()
    assert deleted_job is None
