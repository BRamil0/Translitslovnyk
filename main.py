"""
Основний файл програми.
"""
import asyncio
import argparse
from pathlib import Path

import aiofiles

from source.dictionary import Dictionary, DictionaryManager
from source.translate import Translate
from source.internationalization import internationalization, i18n
from source.console_ui import cui
from source.command_line_handler import parse_command_line_arguments
from source.logger import logger

async def interactive_mode(dm: DictionaryManager, selected_text: str | None = None, selected_dictionary: str | None = None) -> None:
    """
    Режим інтерактивного використання програми.
    """
    if selected_dictionary is None:
        await cui.display_dictionary_list(dm)
        while True:
            selected_dictionary: str = await cui.get_input(i18n["enter_dictionary"])
            if selected_dictionary in dm.get_list_dictionaries():
                dictionary: Dictionary = dm[selected_dictionary]
                await cui.display_message(i18n["dictionary_selected"].format(dictionary.dictionary.info.name))
                break
            else:
                await cui.display_message(i18n["dictionary_not_found"].format(selected_dictionary))
    else:
        dictionary = dm[selected_dictionary]

    translator: Translate = Translate(dictionary)
    if selected_text is None:
        while True:
            text: str = await cui.get_input(i18n["enter_text_to_transliterate"])
            if text.lower() == "exit_transliterate_mode":
                await cui.display_message(i18n["transliteration_exiting"])
                break
            await cui.display_message(i18n["transliteration_result"].format(translator.transliterate(text)))
    else:
        await cui.display_message(i18n["transliteration_result"].format(translator.transliterate(selected_text)))
    return None

async def files_mode(dm: DictionaryManager, dictionary: str, input_path: Path, output_path: Path):
    async with aiofiles.open(str(input_path), mode='r', encoding='utf-8') as infile, \
               aiofiles.open(str(output_path), mode='w', encoding='utf-8') as outfile:
        async for line in infile:
            processed_line: str = Translate(dm[dictionary]).transliterate(line)
            await outfile.write(processed_line + '\n')


async def main() -> None:
    """
    Головна функція програми.
    """
    await internationalization.load_localization()
    dm: DictionaryManager = DictionaryManager()
    await dm.index()
    args: argparse.Namespace = await parse_command_line_arguments()

    if all(value is None for value in vars(args).values()):
        await interactive_mode(dm)

    elif (args.dictionary or args.text or args.input) and not args.output:
        if args.input:
            input_path: Path = Path(args.input)
            if not input_path.exists():
                logger.error(f"Файл {input_path} не знайдено.")
                await cui.display_message(i18n["input_file_not_found"].format(input_path))
                return None
            async with aiofiles.open(input_path, mode='r', encoding='utf-8') as file:
                text = await file.read()
        else:
            text = args.text
        await interactive_mode(dm, text, args.dictionary)

    elif args.input and args.output and args.dictionary:
        input_path: Path = Path(args.input)
        output_path: Path = Path(args.output)
        if not input_path.exists():
            logger.error(f"Файл {input_path} не знайдено.")
            await cui.display_message(i18n["input_file_not_found"].format(input_path))
            return None
        if args.dictionary not in dm.get_list_dictionaries():
            logger.error(f"Словник {args.dictionary} не знайдено.")
            await cui.display_message(i18n["dictionary_not_found"].format(args.dictionary))
            return None
        logger.debug(f"Виконання транслітерації з файлу {input_path} за словником {args.dictionary} у файл {output_path}")
        await files_mode(dm, args.dictionary, input_path, output_path)

    return None

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError) as e:
        asyncio.run(cui.display_message(i18n["transliteration_exiting"] + "\n"))
        logger.debug(f"Вихід з програми через помилку: {e}, скоріше за все, це було викликано натисканням Ctrl+C або Ctrl+D.")