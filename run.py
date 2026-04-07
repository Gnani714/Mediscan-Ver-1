#!/usr/bin/env python3
"""
MediScan AI — Quick Launcher
Loads .env, installs deps if needed, then starts Flask.
"""

import os
import sys
import subprocess

def load_env():
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, val = line.partition('=')
                    os.environ.setdefault(key.strip(), val.strip())
        print("[MediScan] Loaded environment from .env")
    else:
        print("[MediScan] No .env file found — using environment variables / rule-based fallback")

def check_deps():
    try:
        import flask, pdfplumber, docx, reportlab
    except ImportError:
        print("[MediScan] Installing dependencies...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    load_env()
    check_deps()

    from app import app
    import webbrowser, threading

    port = int(os.getenv('PORT', 5000))
    url = f"http://localhost:{port}"

    print(f"\n{'='*55}")
    print(f"  🏥  MediScan AI is running!")
    print(f"  🌐  Open: {url}")
    print(f"  🤖  Groq key:   {'✓ Set' if os.getenv('GROQ_API_KEY','').startswith('gsk') else '✗ Not set (fallback will be used)'}")
    print(f"  🤗  HF key:     {'✓ Set' if os.getenv('HF_API_KEY','').startswith('hf_') else '✗ Not set (fallback will be used)'}")
    print(f"{'='*55}\n")

    threading.Timer(1.2, lambda: webbrowser.open(url)).start()
    app.run(host='0.0.0.0', port=port, debug=False)
