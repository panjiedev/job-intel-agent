"""数据模型定义"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Job:
    """职位信息模型"""
    id: Optional[int] = None
    job_name: str = ""
    salary_desc: Optional[str] = None
    post_description: Optional[str] = None
    work_address: Optional[str] = None
    show_skills: Optional[str] = None
    experience_name: Optional[str] = None
    degree_name: Optional[str] = None
    position_name: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "Job":
        """从数据库行转换为 Job 对象"""
        if row is None:
            return None
        return cls(
            id=row["id"],
            job_name=row["job_name"],
            salary_desc=row["salary_desc"],
            post_description=row["post_description"],
            work_address=row["work_address"],
            show_skills=row["show_skills"],
            experience_name=row["experience_name"],
            degree_name=row["degree_name"],
            position_name=row["position_name"],
        )

