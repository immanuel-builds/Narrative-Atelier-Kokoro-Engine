from fastapi import APIRouter, Depends, Body, HTTPException
from app.auth.auth import login_required
from app.ai.enhancement_service import EnhancementService
from app.ai.coaching_service import CoachingService

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/enhance")
async def enhance_text(
    payload: dict = Body(...),
    user=Depends(login_required)
):
    text = payload.get("text")
    enhancement_type = payload.get("type", "refine")
    mode = payload.get("mode", "balanced")

    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    service = EnhancementService()
    result = await service.enhance(text, enhancement_type, mode)
    return {"result": result}

@router.post("/critique")
async def critique_scene(
    payload: dict = Body(...),
    user=Depends(login_required)
):
    text = payload.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    service = CoachingService()
    result = await service.get_critique(text)
    return {"result": result}

@router.post("/explain")
async def explain_technique(
    payload: dict = Body(...),
    user=Depends(login_required)
):
    technique = payload.get("technique")
    if not technique:
        raise HTTPException(status_code=400, detail="Technique is required")

    service = CoachingService()
    result = await service.explain_technique(technique)
    return {"result": result}
