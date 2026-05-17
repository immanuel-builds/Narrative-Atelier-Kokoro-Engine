import zipfile
import shutil
import os
import json
from pathlib import Path
from datetime import datetime
from app.export.markdown_exporter import MarkdownExporter
from app.export.docx_exporter import DOCXExporter
from app.storage.markdown_handler import MarkdownHandler

class PackageBuilder:
    @staticmethod
    def build(project_title: str, author: str, chapters: list, drafts: list) -> str:
        safe_title = MarkdownHandler.sanitize_filename(project_title)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_base = Path("Exports") / f"{safe_title}_{timestamp}"
        export_base.mkdir(parents=True, exist_ok=True)

        (export_base / "chapters").mkdir(exist_ok=True)
        (export_base / "drafts").mkdir(exist_ok=True)

        # Manuscript MD
        full_md = f"# {project_title}\n\n"
        for i, ch in enumerate(chapters):
            full_md += f"## Chapter {i+1}: {ch['title']}\n\n{ch['content']}\n\n---\n\n"
        MarkdownExporter.export(full_md, export_base / "manuscript.md")

        # Manuscript DOCX
        DOCXExporter.export(project_title, author, chapters, export_base / "manuscript.docx")

        # Chapters & Drafts
        for i, ch in enumerate(chapters):
            MarkdownExporter.export(ch['content'], export_base / "chapters" / f"{i+1:02d}_{MarkdownHandler.sanitize_filename(ch['title'])}.md")
        for d in drafts:
            MarkdownExporter.export(d['content'], export_base / "drafts" / f"{MarkdownHandler.sanitize_filename(d['title'])}.md")

        # Metadata
        metadata = {"title": project_title, "author": author, "exported_at": timestamp}
        with open(export_base / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=4)

        # ZIP
        zip_path = export_base.with_suffix(".zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(export_base):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), export_base))

        shutil.rmtree(export_base)
        return str(zip_path)
