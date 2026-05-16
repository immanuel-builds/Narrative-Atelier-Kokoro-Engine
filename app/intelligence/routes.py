from fastapi import APIRouter, Depends, Body, HTTPException
from app.auth.auth import login_required
from app.intelligence.analysis_engine import AnalysisEngine
from app.intelligence.interpretation_service import InterpretationService
from app.intelligence.risk_engine import RiskEngine
from app.intelligence.reflection_engine import ReflectionEngine

router = APIRouter(prefix="/intelligence", tags=["intelligence"])

@router.post("/analyze")
async def run_analysis(
    payload: dict = Body(...),
    user=Depends(login_required)
):
    text = payload.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    engine = AnalysisEngine()
    result = await engine.run_full_analysis(text)

    # Generate risks and reflections based on observations
    risk_engine = RiskEngine()
    reflection_engine = ReflectionEngine()

    result["risks"] = risk_engine.analyze_risks(result["observations"])
    result["reflections"] = reflection_engine.get_prompts(result["observations"])

    return result

@router.post("/interpret")
async def get_interpretation(
    payload: dict = Body(...),
    user=Depends(login_required)
):
    text = payload.get("text")
    observations = payload.get("observations", [])
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    service = InterpretationService()
    interpretation = await service.interpret(text, observations)
    return {"interpretation": interpretation}
