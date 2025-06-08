"""
Модуль для обробки аргументів командного рядка.
"""

import argparse
from pathlib import Path

from source.logger import logger

async def add_parser_arguments(parser: argparse.ArgumentParser) -> None:
    """
    Додає аргументи командного рядка до парсера.

    :param parser: Парсер аргументів командного рядка.
    """
    parser.add_argument("-d", "--dictionary", required=False, type=Path, help="Шлях до словника для транслітерації.")
    parser.add_argument("-t", "--text", required=False, type=str, help="Текст для транслітерації.")
    parser.add_argument("-i", "--input", required=False, type=Path, help="Шлях до вхідного файлу з текстом для транслітерації.")
    parser.add_argument("-o", "--output", required=False, type=Path, help="Шлях до вихідного файлу для збереження результатів транслітерації.")

    parser.add_argument("-v", "--version")
    parser.add_argument("-a", "--author")
    parser.add_argument("-g", "--github")


    parser.add_argument("-l", "--language", required=False, type=str, help="Мова для інтернаціоналізації.")

async def parse_command_line_arguments() -> argparse.Namespace:
    """
    Парсить аргументи командного рядка.

    :return: Простір імен з аргументами командного рядка.
    """

    parser = argparse.ArgumentParser(description="Транслітерація тексту за словником.")
    await add_parser_arguments(parser)
    args = parser.parse_args()
    logger.debug(f"Було отримано аргументи командного рядка: {args}")
    return args