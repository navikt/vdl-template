from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/is-alive", include_in_schema=False)
async def liveness_status():
    """
    Liveness check
    """
    return JSONResponse(status_code=status.HTTP_200_OK, content={})


@router.get("/is-ready", include_in_schema=False)
async def readiness_status():
    """
    Readiness check
    """
    return JSONResponse(status_code=status.HTTP_200_OK, content={})
