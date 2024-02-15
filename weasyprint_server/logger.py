import os
import logging
import json

LOG_PATH = os.path.join(os.path.abspath(os.getcwd()), "log")
os.makedirs(LOG_PATH, exist_ok=True)
LOG_FILE = os.path.join(LOG_PATH, "weasyprint.log")


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
            log_record["exc_info"] = self.formatException(record.exc_info)

        if "context" in record.__dict__:
            log_record.update(record.__dict__["context"])

        return json.dumps(log_record)


LOGGER = logging.getLogger("weasyprint_server")
handler = logging.FileHandler(LOG_FILE)
handler.setFormatter(JsonFormatter())
LOGGER.addHandler(handler)

LOGGER.setLevel(logging.INFO)
