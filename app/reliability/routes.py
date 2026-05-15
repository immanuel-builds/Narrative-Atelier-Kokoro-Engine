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

    # Gather all file paths for this project's drafts
    draft_files = []
    chapters = db.query(Chapter).filter(Chapter.project_id == project_id).all()
    for ch in chapters:
        drafts = db.query(Draft).filter(Draft.chapter_id == ch.id).all()
        for d in drafts:
            if d.file_path:
                draft_files.append(d.file_path)

    result = IntegrityChecker.check_project_integrity(project.storage_path, draft_files)
    return result

@router.get("/recovery/view")
async def recovery_view(path: str):
    # Security: only allow reading from Projects/ directory
    p = Path(path)
    if "Projects" not in p.parts:
         raise HTTPException(status_code=403, detail="Access denied")

    if not p.exists():
         raise HTTPException(status_code=404, detail="File not found")

    content = p.read_text(encoding="utf-8")
    return HTMLResponse(content=f"<pre style='padding: 2rem; font-family: monospace; white-space: pre-wrap;'>{content}</pre>")
