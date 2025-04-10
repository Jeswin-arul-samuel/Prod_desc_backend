from fastapi import APIRouter, Request
from PIL import Image
from utils.image_utils import load_image
from models.fashion_model import generate_fashion_description
from models.electronics_model import generate_electronics_description
from models.gpt_wrapper import call_gpt

router = APIRouter()

@router.post("/generate/")
async def generate_metadata(request: Request):
    data = await request.json()
    image_path = data.get("image_path")
    category = data.get("category")

    if not image_path or not category:
        return {"error": "Missing image_path or category"}

    try:
        image = load_image(image_path)

        if category == "fashion":
            result = generate_fashion_description(image)
        elif category == "electronics":
            result = generate_electronics_description(image)
        else:
            return {"error": "Unknown category"}

        print(f"\n[BLIP Caption] {result['caption']}")
        print(f"\n[RAW GPT PROMPT]\n{result['raw_prompt']}\n")

        gpt_response = call_gpt(result["raw_prompt"], expect_json=True)

        print(f"\n[RAW GPT RESPONSE]\n{gpt_response}\n")

        return gpt_response

    except Exception as e:
        return {"error": str(e)}
