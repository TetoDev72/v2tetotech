from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/h")
@router.get("/headers")
async def get_headers(request: Request):
    return {
        "client_ip": request.client.host,
        "headers": dict(request.headers)
    }
