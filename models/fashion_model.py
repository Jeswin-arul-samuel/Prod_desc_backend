from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load model + processor once
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_image_caption(image: Image.Image) -> str:
    """
    Uses BLIP to generate a clean product-focused caption from the image.
    """
    prompt = "Describe this fashion product"

    inputs = blip_processor(images=image, text=prompt, return_tensors="pt")
    with torch.no_grad():
        output = blip_model.generate(**inputs, max_length=50)
        caption = blip_processor.decode(output[0], skip_special_tokens=True)
    
    return caption

def generate_fashion_description(image: Image.Image) -> dict:
    """
    Uses BLIP + GPT-4o to create a clean title, description, and features for a fashion product.
    """
    caption = generate_image_caption(image)

    prompt = f"""
You are a product copywriter for a fashion e-commerce platform.

A vision-language model described the product image like this:
"{caption}"

Based only on this, write:
1. A catchy product title
2. A 40-50 word product description
3. 5-6 bullet-point features

Do NOT refer to any person, model, or wearer — just describe the product itself.

Respond in this JSON format:
{{
  "title": "...",
  "description": "...",
  "features": ["...", "...", "..."]
}}
"""

    return {
        "raw_prompt": prompt,
        "caption": caption
    }
