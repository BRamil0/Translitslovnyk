"""
Модуль для обробки аргументів командного рядка.
"""

import argparse
from pathlib import Path

from source.logger import logger
from source.internationalization import i18n

async def add_parser_arguments(parser: argparse.ArgumentParser) -> None:
    """
    Додає аргументи командного рядка до парсера.

    :param parser: Парсер аргументів командного рядка.
    """
    parser.add_argument("-h", "--help", action="help", help=i18n["--help_help"])

    parser.add_argument("-d", "--dictionary", required=False, type=str, help=i18n["--dictionary_help"])
    parser.add_argument("-t", "--text", required=False, type=str, help=i18n["--text_help"])
    parser.add_argument("-i", "--input", required=False, type=Path, help=i18n["--input_help"])
    parser.add_argument("-o", "--output", required=False, type=Path, help=i18n["--output_help"])

    parser.add_argument("-v", "--version", required=False, action="store_true", help=i18n["--version_help"])
    parser.add_argument("-a", "--author", required=False, action="store_true", help= i18n["--author_help"])
    parser.add_argument("-g", "--github", required=False, action="store_true", help= i18n["--github_help"])
    parser.add_argument("-info", "--information", required=False, action="store_true", help= i18n["--information_help"])

    parser.add_argument("-id", "--information_dictionary", required=False, type=str, help= i18n["--information_dictionary_help"])
    parser.add_argument("-ld", "--list_dictionary", required=False, action="store_true", help= i18n["--list_dictionary_help"])
    parser.add_argument("-l", "--language", required=False, type=str, help= i18n["--language_help"])

async def parse_command_line_arguments() -> argparse.Namespace:
    """
    Парсить аргументи командного рядка.

    :return: Простір імен з аргументами командного рядка.
    """

    parser = argparse.ArgumentParser(description=i18n["description_argparse"], add_help=False)
    await add_parser_arguments(parser)
    args = parser.parse_args()
    logger.debug(f"Було отримано аргументи командного рядка: {args}")
    return args