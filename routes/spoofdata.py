from fastapi import APIRouter, Query
from helpers.tools.payload_builder import get_optimal_profile
from data.config import DEFAULT_SPOOF_PROFILE

router = APIRouter()

@router.get("/sd")
@router.get("/spoofdata")
async def spoofdata(strategy: str = Query("best")):
    if strategy == "best":
        data = get_optimal_profile(strategy)
    else:
        data = DEFAULT_SPOOF_PROFILE
        
    return {"status": "success", "strategy": strategy, "spoofdata": data}
