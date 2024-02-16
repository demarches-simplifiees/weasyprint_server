import os
import logging
import json
from pathlib import Path

LOG_DIR = Path(os.environ.get("LOG_DIR", "~/weasyprint_log")).expanduser()
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = LOG_DIR / "weasyprint.log"


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "name": record.name,
            "msg": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }

        if "exc_info" in record.__dict__ and record.exc_info is not None:
            log_record["exc"] = str(record.exc_info)

        if "context" in record.__dict__:
            log_record.update(record.__dict__["context"])

        return json.dumps(log_record)


LOGGER = logging.getLogger("weasyprint_server")
handler = logging.FileHandler(LOG_FILE)
handler.setFormatter(JsonFormatter())
LOGGER.addHandler(handler)

LOGLEVEL = os.environ.get("LOG_LEVEL", "WARNING").upper()
LOGGER.setLevel(LOGLEVEL)
