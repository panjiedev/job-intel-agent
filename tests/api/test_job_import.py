import pytest
from fastapi.testclient import TestClient
from main import app
from job_intel_agent.db.database import Base, engine, get_db
from sqlalchemy.orm import sessionmaker
import pandas as pd
import io
import json

# 创建测试数据库
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    # 不能随便 drop_all 如果用的是真实的本地 docker pg
    # 真实项目中应该用一个隔离的 schema 或专门测试命名的 db
    # 为了这个测试我们保留数据

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

def test_job_import():
    # 创建内存 Excel
    df = pd.DataFrame([{"标题": "Golang工程师", "描述": "需要熟练掌握Go", "地点": "北京"}])
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        df.to_excel(writer, index=False)
    buffer.seek(0)
    
    mapping = {
        "标题": "job_name",
        "描述": "post_description",
        "地点": "work_address"
    }

    response = client.post(
        "/api/jobs/import",
        data={"mapping_str": json.dumps(mapping)},
        files={"file": ("test.xlsx", buffer.read(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    )

    assert response.status_code == 200
    assert response.json()["inserted"] == 1
