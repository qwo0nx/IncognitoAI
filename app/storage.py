import sqlite3
import os
from .config import settings

class Storage:
    def __init__(self, path="data/bot.db"):
        os.makedirs("data", exist_ok=True)
        self.path = path
        self._init_db()
        
    def _init_db(self):
        with sqlite3.connect(self.path) as c:
            c.execute("CREATE TABLE IF NOT EXISTS history (uid INTEGER, role TEXT, content TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS modes (uid INTEGER PRIMARY KEY, mode TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS stats (uid INTEGER PRIMARY KEY, requests INTEGER DEFAULT 0)")
            c.execute("CREATE TABLE IF NOT EXISTS prompts (uid INTEGER PRIMARY KEY, prompt TEXT)")
            
    def get(self, uid):
        with sqlite3.connect(self.path) as c:
            rows = c.execute("SELECT role, content FROM history WHERE uid=?", (uid,)).fetchall()
        return [{"role": r, "content": c} for r, c in rows][-settings.max_history:]
        
    def append(self, uid, role, content):
        with sqlite3.connect(self.path) as c:
            c.execute("INSERT INTO history (uid, role, content) VALUES (?,?,?)", (uid, role, content))
            
    def reset(self, uid):
        with sqlite3.connect(self.path) as c:
            c.execute("DELETE FROM history WHERE uid=?", (uid,))
            
    def set_mode(self, uid, mode):
        with sqlite3.connect(self.path) as c:
            c.execute("INSERT OR REPLACE INTO modes (uid, mode) VALUES (?,?)", (uid, mode))
            
    def get_mode(self, uid):
        with sqlite3.connect(self.path) as c:
            row = c.execute("SELECT mode FROM modes WHERE uid=?", (uid,)).fetchone()
        return row[0] if row else "normal"

    def add_stat(self, uid):
        with sqlite3.connect(self.path) as c:
            c.execute("INSERT OR IGNORE INTO stats (uid, requests) VALUES (?, 0)", (uid,))
            c.execute("UPDATE stats SET requests = requests + 1 WHERE uid=?", (uid,))
            
    def get_stats(self, uid):
        with sqlite3.connect(self.path) as c:
            row = c.execute("SELECT requests FROM stats WHERE uid=?", (uid,)).fetchone()
        return row[0] if row else 0

    def set_prompt(self, uid, prompt):
        with sqlite3.connect(self.path) as c:
            c.execute("INSERT OR REPLACE INTO prompts (uid, prompt) VALUES (?,?)", (uid, prompt))
            
    def get_prompt(self, uid):
        with sqlite3.connect(self.path) as c:
            row = c.execute("SELECT prompt FROM prompts WHERE uid=?", (uid,)).fetchone()
        return row[0] if row else None

    def clear_prompt(self, uid):
        with sqlite3.connect(self.path) as c:
            c.execute("DELETE FROM prompts WHERE uid=?", (uid,))

def build_storage():
    return Storage()