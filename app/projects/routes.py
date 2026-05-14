from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.auth import login_required
from app.models.models import Project
from app.storage.markdown_handler import MarkdownHandler

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/create")
async def create_project(
    request: Request,
    title: str = Form(...),
    description: str = Form(None),
    user=Depends(login_required),
    db: Session = Depends(get_db)
):
    paths = MarkdownHandler.ensure_project_structure(title)
    new_project = Project(
        user_id=user.id,
        title=title,
        description=description,
        storage_path=str(paths["root"])
    )
    db.add(new_project)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@router.post("/{project_id}/edit")
async def edit_project(
    project_id: int,
    title: str = Form(...),
    description: str = Form(None),
    user=Depends(login_required),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if project:
        project.title = title
        project.description = description
        db.commit()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@router.get("/{project_id}/delete")
async def delete_project(
    project_id: int,
    user=Depends(login_required),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if project:
        db.delete(project)
        db.commit()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
