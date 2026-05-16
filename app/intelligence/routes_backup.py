from fastapi import APIRouter, Depends, Body, HTTPException
from app.auth.auth import login_required
from app.diagnostics.engine import DiagnosticsEngine

router = APIRouter(prefix="/diagnostics", tags=["diagnostics"])

@router.post("/analyze")
async def analyze_narrative(
    payload: dict = Body(...),
    user=Depends(login_required)
):
    text = payload.get("text")
    if not text:
        return {"observations": []}

    engine = DiagnosticsEngine()
    observations = await engine.run_analysis(text)
    return {"observations": observations}
