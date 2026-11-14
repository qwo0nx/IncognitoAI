import os, sys, subprocess
from pathlib import Path
here = Path(__file__).resolve().parent
os.chdir(here)
py = here / ('.venv/Scripts/python.exe' if os.name == 'nt' else '.venv/bin/python')
if not py.exists():
    print('[-] Нет .venv. Сначала: python install.py --venv')
    sys.exit(1)
subprocess.call([str(py), '-m', 'app.main'], cwd=here)
