import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from job_intel_agent.db.database import get_db, engine, Base
from job_intel_agent.db.models import Job, Resume

# LangChain 相关
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

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
    model="qwen-plus",
    temperature=0.7,
    openai_api_key=DASH_SCOPE_API_KEY,
    openai_api_base=DASH_SCOPE_BASE_URL
)

# embeddings 模型: 使用 text-embedding-v3
embeddings = OpenAIEmbeddings(
    model="text-embedding-v3",
    openai_api_key=DASH_SCOPE_API_KEY,
    openai_api_base=DASH_SCOPE_BASE_URL
)

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """健康检查"""
    return {"status": "ok"}
from job_intel_agent.api.routers import api_router
app.include_router(api_router)
