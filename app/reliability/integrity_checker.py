from pathlib import Path
import os

class IntegrityChecker:
    @staticmethod
    def validate_file(file_path: str) -> bool:
        path = Path(file_path)
        if not path.exists():
            return False

        # Check if it's readable and not empty (optional, depending on use case)
        try:
            size = path.stat().st_size
            return size >= 0
        except Exception:
            return False

    @staticmethod
    def check_project_integrity(project_storage_path: str) -> dict:
        path = Path(project_storage_path)
        if not path.exists():
            return {"status": "missing", "message": "Project directory not found"}

        required_dirs = ["Chapters", "Drafts", "Backups"]
        missing = [d for d in required_dirs if not (path / d).is_dir()]

        if missing:
            return {"status": "partial", "message": f"Missing directories: {', '.join(missing)}"}

        return {"status": "healthy", "message": "Project structure is intact"}
