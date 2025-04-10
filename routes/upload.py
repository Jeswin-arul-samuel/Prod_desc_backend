import os
import uuid
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from utils.image_utils import load_image, extract_image_from_video
from utils.category_detector import detect_category

router = APIRouter()

# Directory where the files will be uploaded and served from
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount StaticFiles for the /static path to serve the uploaded files
# This should already be handled in your main app code like:
# app.mount("/static", StaticFiles(directory="static"), name="static")

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save file with a unique name
        filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Write the uploaded file to the static/uploads directory
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Get the content type (image/video)
        content_type = file.content_type or ""

        # Process the file depending on its content type
        if content_type.startswith("image"):
            image = load_image(file_path)
            image_path = f"uploads/{filename}"  # URL path to access the image
        elif content_type.startswith("video"):
            image = extract_image_from_video(file_path)
            # Save the extracted frame to disk
            frame_filename = f"{uuid.uuid4().hex}_frame.jpg"
            image_path = f"uploads/{frame_filename}"  # URL path to access the frame
            image.save(os.path.join(UPLOAD_DIR, frame_filename))
        else:
            return JSONResponse(
                status_code=400,
                content={"error": f"Unsupported file type: {content_type}"}
            )

        # Detect category using your category detection model
        category = detect_category(image)

        # Return the relative path to the frontend (to access the file via URL)
        return {
            "image_path": image_path,  # Path relative to the static folder
            "category": category
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Upload failed: {str(e)}"}
        )
