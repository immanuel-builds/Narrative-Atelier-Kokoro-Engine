import os
import re
from pathlib import Path

class MarkdownHandler:
    @staticmethod
    def sanitize_filename(name: str) -> str:
        # Remove non-alphanumeric characters and replace spaces with underscores
        return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_').lower()

    @staticmethod
    def ensure_project_structure(project_name: str) -> dict:
        base_path = Path("Projects") / MarkdownHandler.sanitize_filename(project_name)
        paths = {
            "root": base_path,
            "chapters": base_path / "Chapters",
            "drafts": base_path / "Drafts",
            "backups": base_path / "Backups",
            "exports": base_path / "Exports"
        }

        for p in paths.values():
            p.mkdir(parents=True, exist_ok=True)

        # Create metadata.json if it doesn't exist
        meta_file = base_path / "metadata.json"
        if not meta_file.exists():
            meta_file.write_text("{}")

        return paths

    @staticmethod
    def write_markdown(path: Path, content: str):
        path.write_text(content, encoding="utf-8")

    @staticmethod
    def read_markdown(path: Path) -> str:
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8")

    @staticmethod
    def delete_file(path: Path):
        if path.exists():
            path.unlink()
