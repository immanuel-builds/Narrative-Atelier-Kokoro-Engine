from datetime import datetime
from pathlib import Path
from app.storage.markdown_handler import MarkdownHandler

class StorageService:
    def __init__(self, project_name: str):
        self.paths = MarkdownHandler.ensure_project_structure(project_name)

    def save_chapter(self, chapter_id: int, title: str, content: str) -> str:
        filename = f"chapter_{chapter_id:02d}_{MarkdownHandler.sanitize_filename(title)}.md"
        path = self.paths["chapters"] / filename
        MarkdownHandler.write_markdown(path, content)
        return str(path)

    def save_draft(self, chapter_id: int, draft_id: int, title: str, content: str) -> str:
        filename = f"chapter_{chapter_id:02d}_draft_{draft_id:02d}_{MarkdownHandler.sanitize_filename(title)}.md"
        path = self.paths["drafts"] / filename
        MarkdownHandler.write_markdown(path, content)
        return str(path)

    def create_backup(self, content: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{timestamp}.md"
        path = self.paths["backups"] / filename
        MarkdownHandler.write_markdown(path, content)
        return str(path)

    def get_content(self, file_path: str) -> str:
        return MarkdownHandler.read_markdown(Path(file_path))
