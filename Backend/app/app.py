import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import chatbot, mood_tracker, auth
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Allow your frontend domain allow your frontend domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Get the absolute path to the 'frontend' directory
frontend_path = "/home/sst_24_2/Desktop/Project_nikhil/AI_virtual_therapist/frontend"

# Serve static files (e.g., HTML, CSS, JS)
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Include router for each module
app.include_router(chatbot.router)
app.include_router(mood_tracker.router)
app.include_router(auth.router)


@app.get("/")
def read_index():
    index_path = os.path.join(frontend_path, "index.html")  # Adjust the path to your HTML file
    return FileResponse(index_path)

@app.get("/generated_audio/{filename}")
async def get_audio(filename: str):
    file_path = os.path.join("generated_audio", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "File not found"}
    
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")