import cv2
from PIL import Image
import numpy as np


def load_image(file_path: str) -> Image.Image:
    """Loads an image file as a PIL image."""
    try:
        image = Image.open(file_path).convert("RGB")
        return image
    except Exception as e:
        raise RuntimeError(f"Error loading image: {str(e)}")


def extract_image_from_video(video_path: str) -> Image.Image:
    """Extracts the middle frame of the video and returns it as a PIL image."""
    try:
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if total_frames == 0:
            raise RuntimeError("No frames found in video.")

        middle_frame = total_frames // 2
        cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)

        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise RuntimeError("Could not read frame from video.")

        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)

        return pil_image

    except Exception as e:
        raise RuntimeError(f"Error extracting frame from video: {str(e)}")
