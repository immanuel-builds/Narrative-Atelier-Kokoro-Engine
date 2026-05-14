from fastapi import APIRouter, Depends, Body, HTTPException
from app.auth.auth import login_required
from app.pov.detection import POVDetection
from app.pov.transformation import POVTransformation
from app.pov.intimacy import IntimacyAnalyzer
from app.pov.reliability import ReliabilityAnalyzer

router = APIRouter(prefix="/pov", tags=["pov"])

@router.post("/analyze")
async def analyze_pov(
    payload: dict = Body(...),
    user=Depends(login_required)
):
    text = payload.get("text")
    if not text:
        return {"error": "No text provided"}

    detection = POVDetection.detect(text)
    intimacy = IntimacyAnalyzer.analyze(text)
    reliability = ReliabilityAnalyzer.analyze(text)

    return {
        "detection": detection,
        "intimacy": intimacy,
        "reliability": reliability
    }

@router.post("/transform")
async def transform_pov(
    payload: dict = Body(...),
    user=Depends(login_required)
):
    text = payload.get("text")
    target_pov = payload.get("target_pov")

    if not text or not target_pov:
        raise HTTPException(status_code=400, detail="Text and target_pov required")

    transformer = POVTransformation()
    transformed_text = await transformer.transform(text, target_pov)

    return {"transformed_text": transformed_text}
