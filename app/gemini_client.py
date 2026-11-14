import logging
from google import genai
from google.genai import types
from .config import settings

log = logging.getLogger(__name__)
client = genai.Client(api_key=settings.gemini_key)

# Модель, которую мы будем использовать (сюда впишем рабочую после теста)
ACTIVE_MODEL = 'gemini-2.0-flash' 

async def analyze_image(image_bytes: bytes, prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model=ACTIVE_MODEL,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
                prompt
            ]
        )
        return response.text
    except Exception as e:
        log.error(f"Ошибка Vision: {e}")
        return f"⚠️ Ошибка при анализе фото: модель {ACTIVE_MODEL} недоступна."

async def generate_text(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model=ACTIVE_MODEL,
            contents=prompt
        )
        return response.text
    except Exception as e:
        log.error(f"Ошибка Text: {e}")
        return f"⚠️ Ошибка генерации: {e}"