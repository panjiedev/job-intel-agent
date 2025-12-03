"""JobDAO 测试用例"""
import os
import sys

# 添加项目根目录到 path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from job_intel_agent.db import Database, Job, JobDAO


def test_insert_and_query():
    """测试插入一条数据并查询"""
    # 使用临时数据库
    db = Database(db_path="data/test_job_intel.db")

    # 初始化表结构
    db.init_schema("docs/sql/job.sql")

    # 创建 DAO
    job_dao = JobDAO(db)

    # 构造测试数据
    job = Job(
        job_name="Python后端开发工程师",
        salary_desc="20-35K·15薪",
        post_description="负责后端服务开发，熟悉 Python、FastAPI、MySQL 等技术栈",
        work_address="北京市海淀区中关村",
        show_skills="Python,FastAPI,MySQL,Redis",
        experience_name="3-5年",
        degree_name="本科",
        position_name="后端开发",
    )

    # 插入数据
    new_id = job_dao.insert(job)
    print(f"✅ 插入成功，新记录 id = {new_id}")

    # 查询刚插入的数据
    result = job_dao.get_by_id(new_id)
    print(f"✅ 查询成功：")
    print(f"   - id: {result.id}")
    print(f"   - job_name: {result.job_name}")
    print(f"   - salary_desc: {result.salary_desc}")
    print(f"   - post_description: {result.post_description}")
    print(f"   - work_address: {result.work_address}")
    print(f"   - show_skills: {result.show_skills}")
    print(f"   - experience_name: {result.experience_name}")
    print(f"   - degree_name: {result.degree_name}")
    print(f"   - position_name: {result.position_name}")

    # 验证数据正确性
    assert result.id == new_id
    assert result.job_name == "Python后端开发工程师"
    assert result.salary_desc == "20-35K·15薪"
    print("\n✅ 所有断言通过，测试成功！")


if __name__ == "__main__":
    test_insert_and_query()

