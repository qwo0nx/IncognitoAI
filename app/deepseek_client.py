import asyncio
from openai import AsyncOpenAI
from .config import settings

client = AsyncOpenAI(api_key=settings.api_key, base_url=settings.base_url)

async def stream_model(model: str, messages: list, prefill: str = "", timeout=None):
    timeout = timeout or settings.timeout
    
    # Если передан prefill, добавляем его как начало ответа ассистента
    if prefill:
        messages.append({"role": "assistant", "content": prefill})

    try:
        stream = await asyncio.wait_for(
            client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=1.0,        
                presence_penalty=0.8,   
                frequency_penalty=0.5,
                top_p=1.0,
                max_tokens=2048,
                stream=True
            ), timeout=timeout,
        )
        
        # Сначала отдаем prefill, чтобы он появился в чате
        if prefill:
            yield prefill
            
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        yield f"\n⚠️ Ошибка: {e}"