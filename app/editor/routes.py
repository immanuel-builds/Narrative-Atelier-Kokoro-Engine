from fastapi import APIRouter, Request, Depends, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.auth import login_required
from app.models.models import Project, Chapter, Draft
from app.storage.storage_service import StorageService

router = APIRouter(prefix="/editor", tags=["editor"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/{project_id}", response_class=HTMLResponse)
async def workspace(
    project_id: int,
    request: Request,
    chapter_id: int = None,
    draft_id: int = None,
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

    active_draft = None
    drafts = []
    content = ""

    if active_chapter:
        storage = StorageService(project.title)

        # Ensure at least one draft exists
        existing_drafts = db.query(Draft).filter(Draft.chapter_id == active_chapter.id).all()
        if not existing_drafts:
            active_draft = Draft(
                chapter_id=active_chapter.id,
                title="Initial Draft",
                draft_type="rough",
                is_active=True
            )
            db.add(active_draft)
            db.commit()

            # Create file
            file_path = storage.save_draft(active_chapter.id, active_draft.id, active_draft.title, "")
            active_draft.file_path = file_path
            db.commit()

            existing_drafts = [active_draft]

        drafts = existing_drafts

        if draft_id:
            active_draft = db.query(Draft).filter(Draft.id == draft_id, Draft.chapter_id == active_chapter.id).first()
        else:
            active_draft = db.query(Draft).filter(Draft.chapter_id == active_chapter.id, Draft.is_active == True).first()
            if not active_draft:
                active_draft = drafts[0]

        if active_draft and active_draft.file_path:
            if Path(active_draft.file_path).exists():
                content = storage.get_content(active_draft.file_path)
            else:
                content = "[RECOVERY] Local file missing. Please check the Backups folder or relink your project."

    return templates.TemplateResponse("editor/workspace.html", {
        "request": request,
        "user": user,
        "project": project,
        "chapters": chapters,
        "active_chapter": active_chapter,
        "drafts": sorted(drafts, key=lambda d: d.created_at, reverse=True),
        "active_draft": active_draft,
        "content": content
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
        chapter_order=next_order
    )
    db.add(new_chapter)
    db.commit()

    # Initialize storage and first draft
    storage = StorageService(project.title)
    new_draft = Draft(
        chapter_id=new_chapter.id,
        title=title,
        draft_type="rough",
        is_active=True
    )
    db.add(new_draft)
    db.commit()

    file_path = storage.save_draft(new_chapter.id, new_draft.id, title, "")
    new_draft.file_path = file_path
    db.commit()

    return RedirectResponse(url=f"/editor/{project_id}?chapter_id={new_chapter.id}", status_code=status.HTTP_302_FOUND)

@router.post("/{project_id}/chapters/{chapter_id}/save")
async def save_chapter(
    project_id: int,
    chapter_id: int,
    title: str = Form(...),
    content: str = Form(""),
    draft_id: int = Form(None),
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

    if draft_id:
        draft = db.query(Draft).filter(Draft.id == draft_id, Draft.chapter_id == chapter_id).first()
        if draft:
            draft.title = title
            # Save to file
            storage = StorageService(project.title)
            file_path = storage.save_draft(chapter_id, draft_id, title, content)
            draft.file_path = file_path

    db.commit()
    return RedirectResponse(url=f"/editor/{project_id}?chapter_id={chapter_id}&draft_id={draft_id}", status_code=status.HTTP_302_FOUND)

@router.post("/{project_id}/chapters/{chapter_id}/autosave")
async def autosave_chapter(
    project_id: int,
    chapter_id: int,
    title: str = Form(...),
    content: str = Form(""),
    draft_id: int = Form(None),
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
    if draft_id:
        draft = db.query(Draft).filter(Draft.id == draft_id, Draft.chapter_id == chapter_id).first()
        if draft:
            draft.title = title
            # Save to file
            storage = StorageService(project.title)
            file_path = storage.save_draft(chapter_id, draft_id, title, content)
            draft.file_path = file_path

    db.commit()
    return {"status": "success", "message": "Autosaved"}

@router.post("/{project_id}/chapters/{chapter_id}/drafts/create")
async def create_draft(
    project_id: int,
    chapter_id: int,
    title: str = Form(...),
    draft_type: str = Form("rough"),
    duplicate_from: int = Form(None),
    user=Depends(login_required),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    content = ""
    storage = StorageService(project.title)

    if duplicate_from:
        source_draft = db.query(Draft).filter(Draft.id == duplicate_from, Draft.chapter_id == chapter_id).first()
        if source_draft and source_draft.file_path:
            content = storage.get_content(source_draft.file_path)

    # Set others to inactive
    db.query(Draft).filter(Draft.chapter_id == chapter_id).update({"is_active": False})

    new_draft = Draft(
        chapter_id=chapter_id,
        title=title,
        draft_type=draft_type,
        is_active=True
    )
    db.add(new_draft)
    db.commit()

    file_path = storage.save_draft(chapter_id, new_draft.id, title, content)
    new_draft.file_path = file_path
    db.commit()

    return RedirectResponse(url=f"/editor/{project_id}?chapter_id={chapter_id}&draft_id={new_draft.id}", status_code=status.HTTP_302_FOUND)

@router.get("/{project_id}/chapters/{chapter_id}/drafts/{draft_id}/activate")
async def activate_draft(
    project_id: int,
    chapter_id: int,
    draft_id: int,
    user=Depends(login_required),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.query(Draft).filter(Draft.chapter_id == chapter_id).update({"is_active": False})
    draft = db.query(Draft).filter(Draft.id == draft_id, Draft.chapter_id == chapter_id).first()
    if draft:
        draft.is_active = True
        db.commit()

    return RedirectResponse(url=f"/editor/{project_id}?chapter_id={chapter_id}&draft_id={draft_id}", status_code=status.HTTP_302_FOUND)

@router.get("/{project_id}/chapters/{chapter_id}/drafts/{draft_id}/archive")
async def archive_draft(
    project_id: int,
    chapter_id: int,
    draft_id: int,
    user=Depends(login_required),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    draft = db.query(Draft).filter(Draft.id == draft_id, Draft.chapter_id == chapter_id).first()
    if draft:
        draft.draft_type = "archived"
        if draft.is_active:
            draft.is_active = 0
            # Try to find another draft to activate
            other = db.query(Draft).filter(Draft.chapter_id == chapter_id, Draft.id != draft_id, Draft.draft_type != "archived").first()
            if other:
                other.is_active = 1
        db.commit()
    return RedirectResponse(url=f"/editor/{project_id}?chapter_id={chapter_id}", status_code=status.HTTP_302_FOUND)

@router.get("/{project_id}/chapters/{chapter_id}/drafts/{draft_id}/restore")
async def restore_draft(
    project_id: int,
    chapter_id: int,
    draft_id: int,
    user=Depends(login_required),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    draft = db.query(Draft).filter(Draft.id == draft_id, Draft.chapter_id == chapter_id).first()
    if draft:
        draft.draft_type = "revised"
        db.commit()
    return RedirectResponse(url=f"/editor/{project_id}?chapter_id={chapter_id}&draft_id={draft_id}", status_code=status.HTTP_302_FOUND)

@router.get("/{project_id}/chapters/{chapter_id}/drafts/{draft_id}/delete")
async def delete_draft(
    project_id: int,
    chapter_id: int,
    draft_id: int,
    user=Depends(login_required),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    draft = db.query(Draft).filter(Draft.id == draft_id, Draft.chapter_id == chapter_id).first()
    if draft:
        # Don't delete if it's the last draft
        count = db.query(Draft).filter(Draft.chapter_id == chapter_id).count()
        if count > 1:
            is_active = draft.is_active
            db.delete(draft)
            if is_active:
                other = db.query(Draft).filter(Draft.chapter_id == chapter_id).first()
                if other:
                    other.is_active = 1
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
