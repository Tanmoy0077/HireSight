from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.routes import analysis
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="HireSight API",
    description="AI-powered resume analysis system",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router, prefix="/api")

static_files_dir = os.path.join(
    os.path.dirname(__file__), "..", "..", "frontend", "dist"
)

app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(static_files_dir, "assets")),
    name="assets",
)


@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_files_dir, "index.html"))


@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    file_path = os.path.join(static_files_dir, full_path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(static_files_dir, "index.html"))


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
