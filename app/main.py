from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from app.core.packaging import STATIC_DIR, templates
from app.auth.routes import router as auth_router
from app.dashboard.routes import router as dashboard_router
from app.projects.routes import router as projects_router
from app.editor.routes import router as editor_router
from app.ai.routes import router as ai_router
from app.diagnostics.routes import router as diagnostics_router
from app.pov.routes import router as pov_router
from app.storage.routes import router as storage_router
from app.reliability.routes import router as reliability_router
from app.auth.auth import get_user_from_session
import os
from sqlalchemy.exc import OperationalError
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI(title="Narrative Atelier: Kokoro Engine")

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Register routers
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(projects_router)
app.include_router(editor_router)
app.include_router(ai_router)
app.include_router(diagnostics_router)
app.include_router(pov_router)
app.include_router(storage_router)
app.include_router(reliability_router)

@app.exception_handler(OperationalError)
async def db_connection_exception_handler(request: Request, exc: OperationalError):
    # Emergency Recovery Mode
    projects_dir = Path("Projects")
    local_projects = []

    if projects_dir.exists():
        for p_dir in projects_dir.iterdir():
            if p_dir.is_dir():
                files = []
                # Look in Chapters and Drafts
                for sub in ["Chapters", "Drafts"]:
                    path = p_dir / sub
                    if path.exists():
                        for f in path.glob("*.md"):
                            files.append({"name": f"{sub}/{f.name}", "path": str(f)})
                local_projects.append({"name": p_dir.name, "files": files})

    return templates.TemplateResponse("reliability/recovery_mode.html", {
        "request": request,
        "local_projects": local_projects,
        "storage_root": str(projects_dir.absolute())
    }, status_code=503)

@app.get("/")
async def landing(request: Request, user=Depends(get_user_from_session)):
    return templates.TemplateResponse("landing.html", {"request": request, "user": user})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
