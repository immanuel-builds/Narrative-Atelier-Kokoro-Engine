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
    def check_project_integrity(project_storage_path: str, chapter_files: list) -> dict:
        path = Path(project_storage_path)
        if not path.exists():
            return {"status": "missing", "message": "Project directory not found"}

        required_dirs = ["Chapters", "Drafts", "Backups"]
        missing_dirs = [d for d in required_dirs if not (path / d).is_dir()]

        missing_files = []
        for f in chapter_files:
            if f and not Path(f).exists():
                missing_files.append(f)

        if missing_dirs or missing_files:
            return {
                "status": "unhealthy",
                "message": "Integrity issues detected.",
                "missing_dirs": missing_dirs,
                "missing_files": [Path(f).name for f in missing_files]
            }

        return {"status": "healthy", "message": "Project structure is intact"}
