from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.auth.routes import router as auth_router
from app.dashboard.routes import router as dashboard_router
from app.projects.routes import router as projects_router
from app.editor.routes import router as editor_router
from app.auth.auth import get_user_from_session
import os

app = FastAPI(title="Narrative Atelier: Kokoro Engine")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# Register routers
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(projects_router)
app.include_router(editor_router)

@app.get("/")
async def landing(request: Request, user=Depends(get_user_from_session)):
    return templates.TemplateResponse("landing.html", {"request": request, "user": user})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
