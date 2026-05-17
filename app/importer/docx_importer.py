from docx import Document
from pathlib import Path

class DOCXImporter:
    @staticmethod
    def handle(file_path: Path) -> dict:
        doc = Document(str(file_path))
        content = "\n".join([p.text for p in doc.paragraphs])
        title = file_path.stem.replace('_', ' ').capitalize()
        return {"title": title, "content": content}
