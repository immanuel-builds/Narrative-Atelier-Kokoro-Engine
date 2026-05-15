from fastapi import APIRouter, Depends, Body, HTTPException, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.auth import login_required
from app.models.models import Project, Chapter, Draft
from app.storage.export_service import ExportService
from app.storage.storage_service import StorageService
from pathlib import Path

router = APIRouter(prefix="/storage", tags=["storage"])

@router.get("/export/{project_id}")
async def export_project(
    project_id: int,
    format: str = "md",
    user=Depends(login_required),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    chapters = db.query(Chapter).filter(Chapter.project_id == project_id).order_by(Chapter.chapter_order).all()
    storage = StorageService(project.title)

    chapters_data = []
    for ch in chapters:
        # Get active draft content
        active_draft = db.query(Draft).filter(Draft.chapter_id == ch.id, Draft.is_active == True).first()
        content = ""
        if active_draft and active_draft.file_path:
            content = storage.get_content(active_draft.file_path)
        chapters_data.append({"title": ch.title, "content": content})

    try:
        file_path = ExportService.export_project(project.title, chapters_data, format)
    except Exception as e:
        # Fallback to .md if .docx fails
        if format != "md":
            file_path = ExportService.export_project(project.title, chapters_data, "md")
        else:
            raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

    if file_path and Path(file_path).exists():
        return FileResponse(
            path=file_path,
            filename=Path(file_path).name,
            media_type='application/octet-stream'
        )

    raise HTTPException(status_code=500, detail="Export failed")
