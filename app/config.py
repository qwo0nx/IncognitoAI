import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()

@dataclass
class Settings:
    bot_token: str = os.getenv('BOT_TOKEN','')
    api_key: str = os.getenv('DEEPSEEK_API_KEY','')
    base_url: str = os.getenv('DEEPSEEK_BASE_URL','http://localhost:11434/v1')
    model_chat: str = os.getenv('MODEL_CHAT','gemma3:1b')
    model_reasoner: str = os.getenv('MODEL_REASONER','gemma3:1b')
    max_history: int = int(os.getenv('MAX_HISTORY','10'))
    timeout: float = float(os.getenv('REQUEST_TIMEOUT','120'))
#    gemini_key: str = os.getenv('GEMINI_API_KEY', '') # <--- НОВОЕ

    def validate(self):
        e = []
        if not self.bot_token: e.append('BOT_TOKEN не задан')
        return e

settings = Settings()