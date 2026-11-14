import datetime
import numexpr
import logging
from duckduckgo_search import DDGS

log = logging.getLogger(__name__)

def get_current_time():
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

def calculate_math(expression: str):
    try:
        return str(numexpr.evaluate(expression).item())
    except Exception:
        return "Ошибка вычисления"

def search_web(query: str):
    try:
        results = DDGS().text(query, max_results=3)
        if not results: return "Ничего не найдено."
        return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
    except Exception:
        return "Ошибка поиска."