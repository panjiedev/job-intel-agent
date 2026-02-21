from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .database import Base

try:
    from pgvector.sqlalchemy import Vector
    HAS_PGVECTOR = True
except ImportError:
    HAS_PGVECTOR = False

class Job(Base):
    __tablename__ = "job"
    id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String(255), nullable=False)
    salary_desc = Column(String(255))
    post_description = Column(Text)
    work_address = Column(String(255))
    show_skills = Column(String(255))
    experience_name = Column(String(100))
    degree_name = Column(String(100))
    position_name = Column(String(255))
    
    # 增加 pgvector 支持
    if HAS_PGVECTOR:
        embedding = Column(Vector(1536))

class Resume(Base):
    __tablename__ = "resume"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255))
    raw_content = Column(Text)
    core_skills = Column(Text)
    expected_position = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    
    if HAS_PGVECTOR:
        embedding = Column(Vector(1536))
