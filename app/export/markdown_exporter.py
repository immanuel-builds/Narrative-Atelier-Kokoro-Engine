from pathlib import Path

class MarkdownExporter:
    @staticmethod
    def export(content: str, target_path: Path):
        target_path.write_text(content, encoding="utf-8")
        return str(target_path)
