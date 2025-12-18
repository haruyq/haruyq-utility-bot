import logging
import sys

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[90m",
        logging.INFO: "\033[92m",
        logging.WARNING: "\033[93m",
        logging.ERROR: "\033[91m",
        logging.CRITICAL: "\033[95m"
    }
    RESET = "\033[0m"

    def format(self, record):
        formatted = super().format(record)
        color = self.COLORS.get(record.levelno, self.RESET)
        return f"{color}{formatted}{self.RESET}"

LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

def Logger(name: str | None = None, level_name: str = "DEBUG") -> logging.Logger:
    logger = logging.getLogger(name or __name__)

    if logger.handlers:
        logger.setLevel(LEVEL_MAP.get(level_name, logging.INFO))
        return logger

    logger.setLevel(LEVEL_MAP.get(level_name, logging.INFO))
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColorFormatter("[%(asctime)s] [%(levelname)s | %(name)s] %(message)s", "%H:%M:%S"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger