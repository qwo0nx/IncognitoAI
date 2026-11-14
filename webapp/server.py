import aiohttp
from aiohttp import web
import logging
import os
from app.chain import stream_answer
from app.storage import build_storage

log = logging.getLogger(__name__)
storage = build_storage()

async def handle_index(request):
    return web.FileResponse('webapp/index.html')

async def handle_chat(request):
    try:
        data = await request.json()
        text = data.get('text')
        user_id = data.get('user_id')
        
        if not text:
            return web.json_response({'reply': 'Пустое сообщение'})
            
        messages = [{"role": "user", "content": text}]
        mode = storage.get_mode(user_id)
        
        stream = await stream_answer(messages, mode=mode, uid=user_id)
        
        full_text = ""
        async for chunk in stream:
            full_text += chunk
            
        return web.json_response({'reply': full_text})
        
    except Exception as e:
        log.error(f"WebApp Error: {e}")
        return web.json_response({'reply': f'Ошибка: {e}'})

def create_web_app():
    app = web.Application()
    app.router.add_get('/', handle_index)
    app.router.add_post('/api/chat', handle_chat)
    return app

async def start_web_server():
    app = create_web_app()
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render выдает порт через переменную окружения PORT
    port = int(os.getenv("PORT", 8080))
    
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    log.info(f"WebApp сервер запущен на порту {port}")
