import json
from pathlib import Path
from datetime import datetime

class ManifestGenerator:
    @staticmethod
    def generate_project_metadata(project_title: str, author: str, chapters: list) -> dict:
        return {
            "title": project_title,
            "author": author,
            "exported_at": datetime.now().isoformat(),
            "chapter_count": len(chapters),
            "chapters": [
                {"title": ch["title"], "order": i}
                for i, ch in enumerate(chapters)
            ],
            "version": "1.0"
        }

    @staticmethod
    def generate_recovery_manifest(project_path: Path) -> dict:
        manifest = {
            "recovered_at": datetime.now().isoformat(),
            "items": []
        }
        for folder in ["Chapters", "Drafts"]:
            p = project_path / folder
            if p.exists():
                for f in p.glob("*.md"):
                    manifest["items"].append({
                        "type": folder.lower(),
                        "filename": f.name,
                        "path": str(f)
                    })
        return manifest
