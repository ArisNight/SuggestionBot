import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
import os
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

class ColoredFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    reset = "\x1b[0m"
    format = "[%(asctime)s %(levelname)s]: [ArisSuggestionBot] %(message)s"

    FORMATS = {
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)

def setup_logger():
    # Генерация имени файла
    now = datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    
    # Находим последний номер лога за сегодня
    log_number = 1
    while (LOGS_DIR / f"{date_str}-{log_number}.log").exists():
        log_number += 1
    
    log_filename = f"{date_str}-{log_number}.log"
    log_path = LOGS_DIR / log_filename

    logger = logging.getLogger("ArisSuggestionBot")
    logger.setLevel(logging.INFO)

    # Консольный обработчик с цветным выводом
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)

    # Файловый обработчик с ротацией
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=5*1024*1024,  # 5 MB
        backupCount=3,
        encoding='utf-8'
    )
    file_formatter = logging.Formatter(
        "[%(asctime)s %(levelname)s]: [ArisSuggestionBot] %(message)s",
        datefmt='%H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()