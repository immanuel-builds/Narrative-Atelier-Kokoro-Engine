import logging
import os
from pathlib import Path
from datetime import datetime

class LoggingService:
    def __init__(self):
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)

        self.log_file = self.log_dir / f"kokoro_{datetime.now().strftime('%Y%m')}.log"

        logging.basicConfig(
            filename=str(self.log_file),
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("KokoroReliability")

    def log_event(self, event_type: str, message: str, level: str = "info"):
        msg = f"[{event_type.upper()}] {message}"
        if level == "error":
            self.logger.error(msg)
        elif level == "warning":
            self.logger.warning(msg)
        else:
            self.logger.info(msg)

    def log_failure(self, system: str, error: Exception):
        self.logger.error(f"[FAILURE] System: {system} | Error: {str(error)}", exc_info=True)

# Global logger instance
logger = LoggingService()
