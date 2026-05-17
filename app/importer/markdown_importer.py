from pathlib import Path

class MarkdownImporter:
    @staticmethod
    def handle(file_path: Path) -> dict:
        content = file_path.read_text(encoding="utf-8")
        title = file_path.stem.replace('_', ' ').capitalize()
        return {"title": title, "content": content}
