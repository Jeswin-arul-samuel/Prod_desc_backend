from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load model
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_image_caption(image: Image.Image) -> str:
    """
    Generate a product-focused caption for an electronics product using BLIP.
    """
    prompt = "Describe this electronic product"
    inputs = blip_processor(images=image, text=prompt, return_tensors="pt")
    with torch.no_grad():
        output = blip_model.generate(**inputs, max_length=50)
        caption = blip_processor.decode(output[0], skip_special_tokens=True).strip()

    # Basic fallback if BLIP just echoes the prompt or gives nonsense
    if caption.lower().startswith("describe") or len(caption.split()) < 3:
        return "a modern electronic product"

    return caption

def generate_electronics_description(image: Image.Image) -> dict:
    """
    Uses BLIP + GPT-4o to create structured product metadata for electronics.
    """
    caption = generate_image_caption(image)

    prompt = f"""
You are a product copywriter for a tech e-commerce site.

The uploaded image was described by a vision-language model as:
"{caption}"

Using this information, write the following ONLY about the product (not people or surroundings):
1. A product title
2. A 40-50 word description
3. 5-6 bullet-point features

Output as JSON:
{{
  "title": "...",
  "description": "...",
  "features": ["...", "...", "..."]
}}
""".strip()

    return {
        "raw_prompt": prompt,
        "caption": caption
    }
