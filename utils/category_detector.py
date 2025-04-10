from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from models.gpt_wrapper import call_gpt

# Load BLIP model and processor once globally
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption(image: Image.Image) -> str:
    """Generate an image caption using BLIP."""
    inputs = blip_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        output = blip_model.generate(**inputs)
    caption = blip_processor.decode(output[0], skip_special_tokens=True)
    return caption

def classify_caption_with_gpt(caption: str) -> str:
    system_prompt = (
        "You are a product classifier AI. Based on the given product description, classify the item into one of the two categories: 'fashion' or 'electronics'. "
        "Respond ONLY with this JSON format:\n\n"
        "{ \"category\": \"fashion\" }"
    )
    user_prompt = f"Product description: {caption}"

    result = call_gpt(system_prompt + "\n" + user_prompt, expect_json=True)

    # Check result structure
    if isinstance(result, dict) and "category" in result:
        category = result["category"].strip().lower()
        if category in ["fashion", "electronics"]:
            return category

    return "unknown"

def detect_category(image: Image.Image) -> str:
    """High-level function to detect category from image."""
    try:
        caption = generate_caption(image)
        print(f"[BLIP Caption] {caption}")

        category = classify_caption_with_gpt(caption)
        print(f"[GPT Classification] {category}")

        return category
    except Exception as e:
        print(f"[ERROR] Category detection failed: {str(e)}")
        return "unknown"
