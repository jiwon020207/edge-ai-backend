# app/main.py

from fastapi import FastAPI
import app.routers.auth as auth
import app.routers.faces as faces
import app.routers.protections as protections
import app.routers.events as events
import app.routers.jobs   as jobs
import app.routers.models as models_api
import app.routers.inference as inference

app = FastAPI(title="SeeCure Backend")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(faces.router, prefix="/api/v1/faces", tags=["faces"])
app.include_router(protections.router, prefix="/api/v1/protections", tags=["protections"])
app.include_router(events.router)
app.include_router(jobs.router)
app.include_router(models_api.router)
app.include_router(inference.router)

@app.get("/", tags=["health"])
def health_check():
    return {"status": "OK"}
