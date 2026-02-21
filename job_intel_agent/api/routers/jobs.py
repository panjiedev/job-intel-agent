"""
路由器：职位相关的 API

- 导入 Excel
- 批量存入并生成 Embeddings
"""
import io
import pandas as pd
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from job_intel_agent.db.database import get_db
from job_intel_agent.db.models import Job

import json

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

@router.post("/import")
async def import_jobs_from_excel(
    file: UploadFile = File(...),
    mapping_str: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    上传 Excel 文件并通过字典映射插入到数据库中，异步调用获取 Embedding
    - file: 只支持 .xlsx
    - mapping_str: JSON 格式的字符串，如：{"A列头部名": "job_name", "B列头部名": "post_description"}
    """
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files are supported")
        
    try:
        mapping = json.loads(mapping_str)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid mapping format: {str(e)}")

    contents = await file.read()
    try:
        df = pd.read_excel(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read excel: {str(e)}")

    inserted_count = 0
    
    from main import embeddings, logger
    
    logger.info(f"开始处理 Excel 职位导入. 文件名: {file.filename}, 匹配列: {list(mapping.keys())}")
    
    for _, row in df.iterrows():
        job_data = {}
        for excel_col, db_col in mapping.items():
            if excel_col in df.columns:
                val = row[excel_col]
                # pandas 的 nan 处理
                job_data[db_col] = None if pd.isna(val) else str(val)
                
        if not job_data.get("job_name"):
            continue # 跳过没有职位名称的记录
            
        new_job = Job(**job_data)
        
        # 如果包含描述，则同步获取 embedding (实际生产中可以采用后台任务 background_tasks)
        desc = new_job.post_description
        if desc and isinstance(desc, str) and desc.strip():
            try:
                 emb_vector = embeddings.embed_query(desc.strip())
                 new_job.embedding = emb_vector
            except Exception as e:
                 print(f"Warning: Failed to generate embedding for {new_job.job_name}: {e}")
                 
        db.add(new_job)
        inserted_count += 1
        
    db.commit()
    logger.info(f"Excel 导入完成. 共成功入库 {inserted_count} 条数据 (Postgres/PGVector)")
    
    return {"status": "success", "inserted": inserted_count}
