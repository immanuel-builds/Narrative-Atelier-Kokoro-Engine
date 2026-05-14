from fastapi import APIRouter, Request, Depends, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.auth import login_required
from app.models.models import Project, Chapter

router = APIRouter(prefix="/editor", tags=["editor"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/{project_id}", response_class=HTMLResponse)
async def workspace(
    project_id: int,
    request: Request,
    chapter_id: int = None,
    user=Depends(login_required),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    chapters = db.query(Chapter).filter(Chapter.project_id == project_id).order_by(Chapter.chapter_order).all()

    active_chapter = None
    if chapter_id:
        active_chapter = db.query(Chapter).filter(Chapter.id == chapter_id, Chapter.project_id == project_id).first()
    elif chapters:
        active_chapter = chapters[0]

    return templates.TemplateResponse("editor/workspace.html", {
        "request": request,
        "user": user,
        "project": project,
        "chapters": chapters,
        "active_chapter": active_chapter
    })

@router.post("/{project_id}/chapters/create")
async def create_chapter(
    project_id: int,
    title: str = Form(...),
    user=Depends(login_required),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get last order
    last_chapter = db.query(Chapter).filter(Chapter.project_id == project_id).order_by(Chapter.chapter_order.desc()).first()
    next_order = (last_chapter.chapter_order + 1) if last_chapter else 0

    new_chapter = Chapter(
        project_id=project_id,
        title=title,
        content="",
        chapter_order=next_order
    )
    db.add(new_chapter)
    db.commit()

    return RedirectResponse(url=f"/editor/{project_id}?chapter_id={new_chapter.id}", status_code=status.HTTP_302_FOUND)

@router.post("/{project_id}/chapters/{chapter_id}/save")
async def save_chapter(
    project_id: int,
    chapter_id: int,
    title: str = Form(...),
    content: str = Form(""),
    user=Depends(login_required),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    chapter = db.query(Chapter).filter(Chapter.id == chapter_id, Chapter.project_id == project_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    chapter.title = title
    chapter.content = content
    db.commit()

    return RedirectResponse(url=f"/editor/{project_id}?chapter_id={chapter_id}", status_code=status.HTTP_302_FOUND)

@router.get("/{project_id}/chapters/{chapter_id}/delete")
async def delete_chapter(
    project_id: int,
    chapter_id: int,
    user=Depends(login_required),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    chapter = db.query(Chapter).filter(Chapter.id == chapter_id, Chapter.project_id == project_id).first()
    if chapter:
        db.delete(chapter)
        db.commit()

    return RedirectResponse(url=f"/editor/{project_id}", status_code=status.HTTP_302_FOUND)
