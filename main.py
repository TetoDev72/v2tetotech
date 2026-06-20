from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from data.config import DEBUG, FLAVOR, PROJECT_NAME, API_VERSION

from routes import (
    sync, auto, fetch, advsync, batch, 
    decrypt, headers, deeplink, charity, 
    svinfo, payloadgen, spoofdata, api
)

docs_url = "/docs"
redoc_url = "/redoc"

app = FastAPI(
    title=PROJECT_NAME,
    version=API_VERSION,
    docs_url=docs_url,
    redoc_url=redoc_url,
    debug=DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router)
app.include_router(sync.router)
app.include_router(auto.router)
app.include_router(fetch.router)
app.include_router(advsync.router)
app.include_router(batch.router)
app.include_router(decrypt.router)
app.include_router(headers.router)
app.include_router(deeplink.router)
app.include_router(charity.router)
app.include_router(svinfo.router)
app.include_router(payloadgen.router)
app.include_router(spoofdata.router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if FLAVOR == "release":
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
    return JSONResponse(status_code=500, content={"detail": str(exc)})

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {PROJECT_NAME}",
        "version": API_VERSION,
        "status": "online",
        "docs": "/docs"
    }

if __name__ == "__main__":
    log_level = "info" if FLAVOR == "release" else "debug"

    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=DEBUG,
        log_level=log_level
    )
