from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from job_intel_agent.db.database import get_db
from job_intel_agent.db.models import Resume, Job
from langchain_core.messages import SystemMessage, HumanMessage

import yaml

router = APIRouter(prefix="/api/resume", tags=["Resume Tracking"])

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """提取上传简历的纯文本并将其落库作为 RAG 的向量特征支撑"""
    if not (file.filename.endswith(".md") or file.filename.endswith(".txt")):
        raise HTTPException(status_code=400, detail="Only .txt or .md files")
        
    content = await file.read()
    text = content.decode("utf-8")
    
    from main import embeddings, llm, logger
    from job_intel_agent.utils.prompt_manager import prompt_manager
    
    # 使用模板管理器加载 Prompt
    prompt_tpl = prompt_manager.load_template("resume_extraction")
    final_prompt = prompt_tpl.format(resume_text=text)
    
    logger.info(f"发送简历解析请求到 LLM. Prompt 长度: {len(final_prompt)}")
    logger.debug(f"完整 Prompt 内容: {final_prompt}")

    try:
        response = llm.invoke(final_prompt)
        core_info = response.content
        logger.info(f"LLM 解析成功. 返回字符数: {len(core_info)}")
    except Exception as e:
        logger.error(f"LLM 解析失败: {str(e)}")
        core_info = "LLM提取失败"
        
    # 计算简历全文 Embeddings
    vector = embeddings.embed_query(text)
    
    new_resume = Resume(
        user_name=file.filename.split(".")[0],
        raw_content=text,
        core_skills=core_info,
        embedding=vector
    )
    db.add(new_resume)
    db.commit()
    return {"status": "success", "resume_id": new_resume.id, "extracted": core_info}

@router.get("/match/{resume_id}")
async def match_top_jobs(resume_id: int, top_k: int = 5, db: Session = Depends(get_db)):
    """简历上传后，依据简历 Embedding 和 PGVector '<=>' 余弦相似度召回职位"""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
         raise HTTPException(status_code=404, detail="Resume not found")
         
    # 使用 `<=>` 也就是 Cosine distance -> ASC 越接近 0 越像
    results = db.query(Job).order_by(Job.embedding.cosine_distance(resume.embedding)).limit(top_k).all()
    
    return [
       {"id": j.id, "job_name": j.job_name, "skills": j.show_skills}
       for j in results
    ]
