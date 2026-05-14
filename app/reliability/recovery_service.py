from pathlib import Path
from datetime import datetime
import shutil
from app.storage.markdown_handler import MarkdownHandler

class RecoveryService:
    @staticmethod
    def create_snapshot(project_name: str, chapter_id: int, content: str):
        safe_name = MarkdownHandler.sanitize_filename(project_name)
        backup_dir = Path("Projects") / safe_name / "Backups"
        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ch_{chapter_id}_{timestamp}.bak"
        path = backup_dir / filename
        path.write_text(content, encoding="utf-8")
        return str(path)

    @staticmethod
    def save_autosave_temp(project_name: str, chapter_id: int, content: str):
        # Temp files for crash recovery
        temp_dir = Path("Projects") / MarkdownHandler.sanitize_filename(project_name) / "Drafts" / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)

        temp_file = temp_dir / f"autosave_ch_{chapter_id}.tmp"
        temp_file.write_text(content, encoding="utf-8")
        return str(temp_file)

    @staticmethod
    def get_recovery_data(project_name: str, chapter_id: int) -> str:
        temp_file = Path("Projects") / MarkdownHandler.sanitize_filename(project_name) / "Drafts" / "temp" / f"autosave_ch_{chapter_id}.tmp"
        if temp_file.exists():
            return temp_file.read_text(encoding="utf-8")
        return ""
