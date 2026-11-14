import logging
from telegraph import Telegraph
from telegraph.exceptions import TelegraphException

log = logging.getLogger(__name__)

# Создаем клиента (один раз)
telegraph = Telegraph()
telegraph.create_account(short_name='AgentMonster')

def create_telegraph_page(title: str, text: str) -> str:
    """Превращает текст нейросети в статью на Telegraph и возвращает ссылку"""
    try:
        # Разбиваем текст на строки
        lines = text.split('\n')
        nodes = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Если строка заканчивается на двоеточие и она короткая - это подзаголовок
            if line.endswith(':') and len(line) < 60:
                nodes.append({"tag": "h3", "children": [line]})
            else:
                # Обычный абзац
                nodes.append({"tag": "p", "children": [line]})
                
        # Создаем страницу
        response = telegraph.create_page(
            title=title,
            author_name="Agent-Monster",
            content=nodes
        )
        
        return f"https://telegra.ph/{response['path']}"
        
    except Exception as e:
        log.error(f"Ошибка Telegraph: {e}")
        return ""