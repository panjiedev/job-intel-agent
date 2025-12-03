"""Job 数据访问层"""
from typing import List, Optional
from .database import Database
from .models import Job


class JobDAO:
    """Job 表的数据访问对象"""

    def __init__(self, db: Database):
        self.db = db

    def insert(self, job: Job) -> int:
        """插入一条职位记录，返回新记录的 id"""
        sql = """
            INSERT INTO job (job_name, salary_desc, post_description, work_address,
                             show_skills, experience_name, degree_name, position_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            job.job_name,
            job.salary_desc,
            job.post_description,
            job.work_address,
            job.show_skills,
            job.experience_name,
            job.degree_name,
            job.position_name,
        )
        return self.db.execute(sql, params)

    def get_by_id(self, job_id: int) -> Optional[Job]:
        """根据 id 查询职位"""
        sql = "SELECT * FROM job WHERE id = ?"
        row = self.db.query_one(sql, (job_id,))
        return Job.from_row(row)

    def get_all(self) -> List[Job]:
        """查询所有职位"""
        sql = "SELECT * FROM job"
        rows = self.db.query(sql)
        return [Job.from_row(row) for row in rows]

    def delete_by_id(self, job_id: int) -> None:
        """根据 id 删除职位"""
        sql = "DELETE FROM job WHERE id = ?"
        self.db.execute(sql, (job_id,))

