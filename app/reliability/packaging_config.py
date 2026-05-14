import os
import sys
from pathlib import Path

def get_base_path():
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path(os.path.abspath("."))
    return base_path

def get_storage_path():
    """Ensure storage directory exists in the user's local app data or current dir"""
    # For now, keep it in the current directory for simplicity,
    # but ensure it handles relative paths correctly.
    storage_path = get_base_path() / "Projects"
    storage_path.mkdir(exist_ok=True)
    return storage_path

class PackagingConfig:
    BASE_PATH = get_base_path()
    STORAGE_PATH = get_storage_path()
    STATIC_PATH = BASE_PATH / "app" / "static"
    TEMPLATES_PATH = BASE_PATH / "app" / "templates"
