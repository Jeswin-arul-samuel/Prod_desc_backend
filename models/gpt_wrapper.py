import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_json_output(raw: str) -> str:
    """
    Cleans up markdown-style code blocks or any formatting around the JSON.
    Example: ```json { "key": "value" } ```
    """
    # Remove markdown triple-backtick blocks (e.g., ```json ... ```)
    cleaned = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()

    return cleaned

def call_gpt(prompt: str, expect_json=True) -> dict | str:
    """
    Calls GPT-4o and returns either parsed JSON or raw string.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert product AI."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        reply = response.choices[0].message.content.strip()
        print("\n[RAW GPT RESPONSE]\n" + reply + "\n")

        if expect_json:
            try:
                cleaned = clean_json_output(reply)
                return json.loads(cleaned)
            except json.JSONDecodeError as je:
                print("[ERROR] GPT returned non-JSON output.")
                return {"error": "Invalid JSON", "raw": reply}
        else:
            return reply

    except Exception as e:
        print(f"[ERROR] GPT-4o generation failed: {str(e)}")
        return {"error": str(e)}
