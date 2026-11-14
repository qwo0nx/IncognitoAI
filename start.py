import os, sys, subprocess
from pathlib import Path

here = Path(__file__).resolve().parent
os.chdir(here)

# В облаке (Render) мы используем системный python, локально - из .venv
if os.name == "nt" and (here / ".venv" / "Scripts" / "python.exe").exists():
    py = here / ".venv" / "Scripts" / "python.exe"
else:
    py = sys.executable

subprocess.call([str(py), "-m", "app.main"], cwd=here)
