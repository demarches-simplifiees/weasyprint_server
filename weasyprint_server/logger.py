from os import environ
from logging import getLogger, FileHandler, Formatter
import json
from pathlib import Path
import datetime

LOG_DIR = Path(environ.get("LOG_DIR", "~/weasyprint_log")).expanduser()
LOG_DIR.mkdir(parents=True, exist_ok=True)


class JsonFormatter(Formatter):
    def format(self, record):
        now = datetime.datetime.now().isoformat()

        log_record = {
            "time": now,
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


ERROR_LOGGER = getLogger("error")
handler = FileHandler(LOG_DIR / "error.log")
handler.setFormatter(JsonFormatter())
ERROR_LOGGER.addHandler(handler)
ERROR_LOGGER.setLevel(environ.get("ERROR_LOG_LEVEL", "WARNING").upper())

ACCESS_LOGGER = getLogger("access")
ACCESS_LOGGER.addHandler(FileHandler(LOG_DIR / "access.log"))
ACCESS_LOGGER.setLevel(environ.get("ACCESS_LOG_LEVEL", "INFO").upper())
