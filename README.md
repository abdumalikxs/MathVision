# Desmos-lite (No JS) + Gemini Q&A (v2)

Fixes:
- Uses `sympy.lambdify` correctly.
- Accepts `^` as power (auto-converted to `**`).
- Lets you set `GEMINI_API_KEY` inside `settings.py` (or via env).

## Quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Option A: put your key in desmoslite/settings.py (GEMINI_API_KEY = "PASTE_HERE")
# Option B: export GEMINI_API_KEY in your shell
python manage.py migrate
python manage.py runserver
```
Open http://127.0.0.1:8000/plot/
