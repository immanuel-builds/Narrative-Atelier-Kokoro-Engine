from fastapi import APIRouter, Depends, Body, HTTPException
from app.auth.auth import login_required
from app.reliability.recovery_service import RecoveryService
from app.reliability.integrity_checker import IntegrityChecker
from app.models.models import Project
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/reliability", tags=["reliability"])

@router.post("/snapshot")
async def create_snapshot(
    payload: dict = Body(...),
    user=Depends(login_required),
    db: Session = Depends(get_db)
):
    project_id = payload.get("project_id")
    chapter_id = payload.get("chapter_id")
    content = payload.get("content")

    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    path = RecoveryService.create_snapshot(project.title, chapter_id, content)
    return {"status": "success", "backup_path": path}

@router.get("/check/{project_id}")
async def check_integrity(
    project_id: int,
    user=Depends(login_required),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = IntegrityChecker.check_project_integrity(project.storage_path)
    return result
