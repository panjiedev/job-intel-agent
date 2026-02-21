import os
import logging

# 配置全局日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("job-intel")

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from job_intel_agent.db.database import get_db, engine, Base
from job_intel_agent.db.models import Job, Resume

# LangChain 相关
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from openai import OpenAI

app = FastAPI(title="Job Intel AI RAG System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
Base.metadata.create_all(bind=engine)

# 初始化大模型 (兼容 OpenAI 格式接入 DashScope)
DASH_SCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "sk-6cd14981baf84b7eb40bd94ee22eac3a")
DASH_SCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

llm = ChatOpenAI(
    model="qwen3.5-plus",
    temperature=0.7,
    openai_api_key=DASH_SCOPE_API_KEY,
    openai_api_base=DASH_SCOPE_BASE_URL
)

# Embeddings: 直接使用 openai 原生客户端调用 DashScope
# langchain_openai.OpenAIEmbeddings 会发送 DashScope 不支持的额外参数导致 400
_openai_client = OpenAI(api_key=DASH_SCOPE_API_KEY, base_url=DASH_SCOPE_BASE_URL)

class DashScopeEmbeddings:
    """自定义 Embedding 封装，绕开 langchain_openai 的兼容性问题"""
    def __init__(self, model: str = "text-embedding-v4"):
        self.model = model

    def embed_query(self, text: str) -> list[float]:
        resp = _openai_client.embeddings.create(model=self.model, input=text)
        return resp.data[0].embedding

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # DashScope text-embedding-v4 每批最多 10 条
        all_embeddings = []
        for i in range(0, len(texts), 10):
            batch = texts[i:i+10]
            resp = _openai_client.embeddings.create(model=self.model, input=batch)
            all_embeddings.extend([d.embedding for d in resp.data])
        return all_embeddings

embeddings = DashScopeEmbeddings(model="text-embedding-v4")

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """健康检查"""
    return {"status": "ok"}
from job_intel_agent.api.routers import api_router
app.include_router(api_router)

