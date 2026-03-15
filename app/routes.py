from fastapi import APIRouter, HTTPException
from app.schemas import AnalysisRequest, AnalysisResponse
from app.orchestrator import MarketAnalysisOrchestrator

router = APIRouter()
orchestrator = MarketAnalysisOrchestrator()


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    responses={
        400: {"description": "Invalid product or region input"},
        500: {"description": "Internal server error"},
    },
)
def analyze_product(request: AnalysisRequest) -> AnalysisResponse:
    try:
        return orchestrator.run(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal server error") from exc
