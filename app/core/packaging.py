import os
import sys
from pathlib import Path
from fastapi.templating import Jinja2Templates

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(os.path.abspath("."))

BASE_PATH = get_base_path()
STATIC_DIR = BASE_PATH / "app" / "static"
TEMPLATES_DIR = BASE_PATH / "app" / "templates"

# Re-initialize templates with the correct path for packaged app
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
