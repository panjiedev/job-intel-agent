import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 环境变量配置 DATABASE_URL
# SQLite 测试: sqlite:///./data/test_job_intel.db
# PostgreSQL: postgresql://root:123456@localhost:5432/job_intel
DB_URL = os.environ.get("DATABASE_URL", "sqlite:///./data/job_intel.db")

# 如果包含 sqlite，则加上 check_same_thread
connect_args = {}
if DB_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(DB_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
