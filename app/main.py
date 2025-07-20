from fastapi import FastAPI
from app.routers import auth, faces, protections

app = FastAPI(title="SeeCure Backend")
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(faces.router, prefix="/api/v1/faces")
app.include_router(protections.router, prefix="/api/v1/protections")

@app.get("/", tags=["health"])
def health_check():
    return {"status": "OK"}
