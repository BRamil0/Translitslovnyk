"""
Модуль для обробки аргументів командного рядка.
"""

import argparse

from source.logger import logger

async def add_parser_arguments(parser: argparse.ArgumentParser) -> None:
    """
    Додає аргументи командного рядка до парсера.

    :param parser: Парсер аргументів командного рядка.
    """
    parser.add_argument("-d", "--dictionary", required=False)
    parser.add_argument("-t", "--text", required=False)
    parser.add_argument("-i", "--input", required=False)
    parser.add_argument("-o", "--output", required=False)

async def parse_command_line_arguments() -> argparse.Namespace:
    """
    Парсить аргументи командного рядка.

    :return: Простір імен з аргументами командного рядка.
    """

    parser = argparse.ArgumentParser(description="Транслітерація тексту за словником.")
    await add_parser_arguments(parser)
    args = parser.parse_args()

    if all(value is None for value in vars(args).values()):
        return args

    if not args.dictionary and not args.text and not args.input:
        logger.error("Необхідно вказати словник та текст або файл для транслітерації.")
        parser.error("Необхідно вказати словник та текст або файл для транслітерації.")

    return args