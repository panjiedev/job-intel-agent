"""SQLite 数据库连接管理"""
import sqlite3
from pathlib import Path


class Database:
    """SQLite 数据库管理类"""

    def __init__(self, db_path: str = "data/job_intel.db"):
        self.db_path = db_path
        self._ensure_dir()

    def _ensure_dir(self):
        """确保数据库目录存在"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 支持按列名访问
        return conn

    def init_schema(self, schema_path: str = "docs/sql/job.sql"):
        """根据 SQL 文件初始化表结构"""
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        conn = self.get_connection()
        try:
            conn.executescript(schema_sql)
            conn.commit()
        finally:
            conn.close()

    def execute(self, sql: str, params: tuple = ()):
        """执行单条 SQL（INSERT/UPDATE/DELETE）"""
        conn = self.get_connection()
        try:
            cursor = conn.execute(sql, params)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def query(self, sql: str, params: tuple = ()):
        """查询并返回所有结果"""
        conn = self.get_connection()
        try:
            cursor = conn.execute(sql, params)
            return cursor.fetchall()
        finally:
            conn.close()

    def query_one(self, sql: str, params: tuple = ()):
        """查询并返回单条结果"""
        conn = self.get_connection()
        try:
            cursor = conn.execute(sql, params)
            return cursor.fetchone()
        finally:
            conn.close()

