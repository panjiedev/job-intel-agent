"""JobDAO 测试用例"""
import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from job_intel_agent.db.database import Base
from job_intel_agent.db.job_dao import JobDAO

DB_URL = os.environ.get("TEST_DATABASE_URL", "postgresql://root:123456@localhost:5432/job_intel")

engine = create_engine(DB_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_insert_and_query(db_session):
    job_dao = JobDAO(db_session)

    job_data = {
        "job_name": "Python后端开发工程师",
        "salary_desc": "20-35K·15薪",
        "post_description": "负责后端服务开发，熟悉 Python、FastAPI、MySQL 等技术栈",
        "work_address": "北京市海淀区中关村",
        "show_skills": "Python,FastAPI,MySQL,Redis",
        "experience_name": "3-5年",
        "degree_name": "本科",
        "position_name": "后端开发",
    }

    new_id = job_dao.insert(job_data)
    print(f"✅ 插入成功，新记录 id = {new_id}")

    result = job_dao.get_by_id(new_id)

    assert result.id == new_id
    assert result.job_name == "Python后端开发工程师"
    assert result.salary_desc == "20-35K·15薪"

    job_dao.delete_by_id(new_id)
    assert job_dao.get_by_id(new_id) is None
