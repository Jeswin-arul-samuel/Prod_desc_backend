import os
import uuid
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from utils.image_utils import load_image, extract_image_from_video
from utils.category_detector import detect_category

router = APIRouter()

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save file
        filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Check content_type safely
        content_type = file.content_type or ""

        if content_type.startswith("image"):
            image = load_image(file_path)
            image_path = file_path  # use original image
        elif content_type.startswith("video"):
            image = extract_image_from_video(file_path)
            # Save the extracted frame to disk
            frame_filename = f"{uuid.uuid4().hex}_frame.jpg"
            image_path = os.path.join(UPLOAD_DIR, frame_filename)
            image.save(image_path)
        else:
            return JSONResponse(
                status_code=400,
                content={"error": f"Unsupported file type: {content_type}"}
            )

        # Detect category using BLIP + GPT-4o
        category = detect_category(image)

        return {
            "image_path": image_path,
            "category": category
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Upload failed: {str(e)}"}
        )
