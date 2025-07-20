# app/main.py

from fastapi import FastAPI
import app.routers.auth as auth
import app.routers.faces as faces
import app.routers.protections as protections

app = FastAPI(title="SeeCure Backend")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(faces.router, prefix="/api/v1/faces", tags=["faces"])
app.include_router(protections.router, prefix="/api/v1/protections", tags=["protections"])

@app.get("/", tags=["health"])
def health_check():
    return {"status": "OK"}
