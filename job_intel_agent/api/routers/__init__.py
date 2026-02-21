from fastapi import APIRouter
from job_intel_agent.api.routers import jobs, resume

api_router = APIRouter()
api_router.include_router(jobs.router)
api_router.include_router(resume.router)
