import uvicorn
import webview
import threading
import time
import socket
import sys
import os
from pathlib import Path

# Ensure we are in the correct directory for local storage
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

from app.main import app

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def run_server():
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    except Exception as e:
        print(f"Server failed: {e}")

if __name__ == "__main__":
    # Ensure Projects directory exists relative to the executable if not in dev
    if getattr(sys, 'frozen', False):
        exe_dir = Path(sys.executable).parent
        proj_dir = exe_dir / "Projects"
        proj_dir.mkdir(exist_ok=True)
        # We might want to symlink or mount this, but for now
        # the app logic handles Path("Projects") relative to CWD.
        os.chdir(exe_dir)

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Wait for server
    retries = 0
    while not is_port_in_use(8000) and retries < 20:
        time.sleep(0.5)
        retries += 1

    webview.create_window("Narrative Atelier: Kokoro Engine", "http://127.0.0.1:8000")
    webview.start()
