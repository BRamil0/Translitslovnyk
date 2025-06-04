"""
Обробка та реєстрація журналів (логів) за допомогою loguru.
"""
import sys

from loguru import logger

from source.config import settings

logger.remove()

if settings.is_log:
    logger.add(settings.LOG_DIR / "info.log", rotation="10 MB", enqueue=True, backtrace=True, diagnose=True, format=settings.LOG_FORMAT, encoding="utf-8")
    logger.add(settings.LOG_DIR / "error.log", level="ERROR", rotation="10 MB", enqueue=True, backtrace=True, diagnose=True, format=settings.LOG_FORMAT, encoding="utf-8")
    logger.debug(f"(logger) Журналювання ввімкнено, файли журналів зберігаються в: {settings.LOG_DIR}")
    if settings.is_show_log:
        logger.info("(logger) Виведення журналів на консоль увімкнено.")
        logger.add(sys.stdout, colorize=True, format=settings.LOG_FORMAT)
    else:
        logger.info("(logger) Виведення журналів на консоль вимкнено.")