from fastapi import APIRouter, Depends, Body, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.auth import login_required
from app.models.models import Project, Chapter, Draft
from app.export.markdown_exporter import MarkdownExporter
from app.export.txt_exporter import TXTExporter
from app.export.docx_exporter import DOCXExporter
from app.export.package_builder import PackageBuilder
from app.importer.markdown_importer import MarkdownImporter
from app.importer.txt_importer import TXTImporter
from app.importer.docx_importer import DOCXImporter
from app.storage.storage_service import StorageService
from app.storage.backup_service import BackupService
from pathlib import Path
import shutil
import os

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
        active_draft = db.query(Draft).filter(Draft.chapter_id == ch.id, Draft.is_active == True).first()
        content = storage.get_content(active_draft.file_path) if active_draft else ""
        chapters_data.append({"title": ch.title, "content": content})

    # Prepare export path
    export_dir = Path("Exports")
    export_dir.mkdir(exist_ok=True)
    file_path = export_dir / f"manuscript_{project_id}.{format}"

    full_content = "\n\n".join([f"# {c['title']}\n\n{c['content']}" for c in chapters_data])

    if format == "md":
        MarkdownExporter.export(full_content, file_path)
    elif format == "txt":
        TXTExporter.export(full_content, file_path)
    elif format == "docx":
        DOCXExporter.export(project.title, user.username, chapters_data, file_path)

    return FileResponse(file_path, filename=f"{project.title}.{format}")

@router.get("/package/{project_id}")
async def export_package(project_id: int, user=Depends(login_required), db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project: raise HTTPException(404, "Project not found")

    storage = StorageService(project.title)
    chapters = db.query(Chapter).filter(Chapter.project_id == project_id).order_by(Chapter.chapter_order).all()

    chapters_data = []
    drafts_data = []
    for ch in chapters:
        active_draft = db.query(Draft).filter(Draft.chapter_id == ch.id, Draft.is_active == True).first()
        chapters_data.append({"title": ch.title, "content": storage.get_content(active_draft.file_path) if active_draft else ""})
        all_d = db.query(Draft).filter(Draft.chapter_id == ch.id).all()
        for d in all_d:
            drafts_data.append({"title": d.title, "content": storage.get_content(d.file_path) if d.file_path else ""})

    zip_path = PackageBuilder.build(project.title, user.username, chapters_data, drafts_data)
    return FileResponse(zip_path, filename=os.path.basename(zip_path))

@router.post("/import/{project_id}")
async def import_file(project_id: int, file: UploadFile = File(...), user=Depends(login_required), db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project: raise HTTPException(404, "Project not found")

    temp = Path(f"temp_{file.filename}")
    with temp.open("wb") as f: shutil.copyfileobj(file.file, f)

    try:
        ext = temp.suffix.lower()
        if ext == ".md": data = MarkdownImporter.handle(temp)
        elif ext == ".txt": data = TXTImporter.handle(temp)
        elif ext == ".docx": data = DOCXImporter.handle(temp)
        else: raise HTTPException(400, "Invalid format")

        storage = StorageService(project.title)
        new_ch = Chapter(project_id=project.id, title=data["title"], chapter_order=len(project.chapters))
        db.add(new_ch); db.flush()
        path = storage.save_chapter(new_ch.id, new_ch.title, data["content"])
        new_ch.file_path = path
        db.add(Draft(chapter_id=new_ch.id, title="Imported", file_path=path, is_active=True))
        db.commit()
        return {"status": "success"}
    finally:
        if temp.exists(): temp.unlink()

@router.post("/snapshot/{project_id}")
async def create_snapshot(project_id: int, user=Depends(login_required), db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project: raise HTTPException(404)
    path = BackupService.create_project_snapshot(project.title, Path(project.storage_path))
    return {"path": path}
