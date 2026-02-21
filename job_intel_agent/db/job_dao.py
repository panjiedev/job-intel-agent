"""Job 数据访问层"""
from typing import List, Optional
from sqlalchemy.orm import Session
from .models import Job


class JobDAO:
    """Job 表的数据访问对象"""

    def __init__(self, db: Session):
        self.db = db

    def insert(self, job_data: dict) -> int:
        """插入一条职位记录，返回新记录的 id"""
        job = Job(**job_data)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job.id

    def get_by_id(self, job_id: int) -> Optional[Job]:
        """根据 id 查询职位"""
        return self.db.query(Job).filter(Job.id == job_id).first()

    def get_all(self) -> List[Job]:
        """查询所有职位"""
        return self.db.query(Job).all()

    def delete_by_id(self, job_id: int) -> None:
        """根据 id 删除职位"""
        job = self.get_by_id(job_id)
        if job:
            self.db.delete(job)
            self.db.commit()
