from pathlib import Path
from app.storage.markdown_handler import MarkdownHandler

class ImportService:
    @staticmethod
    def import_file(file_path: Path) -> dict:
        if not file_path.exists():
            return {"error": "File not found"}

        content = file_path.read_text(encoding="utf-8")
        title = file_path.stem.replace('_', ' ').capitalize()

        return {
            "title": title,
            "content": content
        }
