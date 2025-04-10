from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routes import upload, generate, health

app = FastAPI(title="Product Metadata Generator")

# Allow frontend to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(health.router)
app.include_router(upload.router)
app.include_router(generate.router)

# Serve static files (e.g., uploaded images, generated JSONs)
app.mount("/static", StaticFiles(directory="static"), name="static")
