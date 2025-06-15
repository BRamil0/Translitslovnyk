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
from source.config import settings

async def search_dictionary(dm: DictionaryManager, dictionary_name: str) -> Dictionary | None:
    """
    Пошук словника за назвою.

    :param dm: Менеджер словників.
    :param dictionary_name: Назва словника для пошуку.
    :return: Знайдений словник або None, якщо не знайдено.
    """
    dictionary: Dictionary | None = None
    fields = ["id", "name", "file_path", "file_name"]
    for field in fields:
        dictionary = dm.search_dictionary(dictionary_name, field)
        if dictionary is not None:
            break
    return dictionary

async def interactive_mode(dm: DictionaryManager, selected_text: str | None = None, selected_dictionary: str | None = None) -> None:
    """
    Режим інтерактивного використання програми.
    """
    if selected_dictionary is None:
        await cui.display_dictionary_list(dm)
        while True:
            selected_dictionary: str = await cui.get_input(i18n["enter_dictionary"])
            dictionary = await search_dictionary(dm, selected_dictionary)
            if dictionary is None:
                await cui.display_message(i18n["dictionary_not_found"].format(selected_dictionary))
                await cui.display_dictionary_list(dm)
                continue
            await cui.display_message(i18n["dictionary_selected"].format(dictionary.dictionary.info.name))
            break
    else:
        dictionary = await search_dictionary(dm, selected_dictionary)
        if dictionary is None:
            logger.error(f"Словник {selected_dictionary} не знайдено.")
            await cui.display_message(i18n["dictionary_not_found"].format(selected_dictionary))
            return None
        await cui.display_message(i18n["dictionary_selected"].format(dictionary.dictionary.info.name))

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
    logger.debug("Початок роботи програми.")
    try:
        await internationalization.load_localization()
    except FileNotFoundError as FNFError:
        logger.error(
            f"Файл локалізації не знайдено: {FNFError}. Перевірте наявність файлу в директорії {settings.path_internationalization}. Або змініть config.json, щоб вказати іншу мову."
        )
        await cui.display_message(
            "Не вдалося завантажити мову, рекомендується почистити файл config.json"
        )
        raise FNFError
    logger.debug("Завантаження локалізації завершено.")

    dm: DictionaryManager = DictionaryManager()
    await dm.index()
    args: argparse.Namespace = await parse_command_line_arguments()

    if not args.not_welcome:
        await cui.display_panel(i18n["welcome_message"].format(settings.version, i18n.get_lm().info.name))

    if args.language:
        try:
            internationalization.set_language(args.language)
            await internationalization.load_localization()
        except FileNotFoundError as FNFError:
            internationalization.set_language(settings.language)
            await internationalization.load_localization()

            logger.error(f"Файл локалізації для мови {args.language} не знайдено: {FNFError}.")
            await cui.display_message(i18n["language_file_not_found"].format(args.language))
            return None
        settings.language = args.language
        await cui.display_message(i18n["language_set"].format(settings.language))
        await settings.save_settings()

    if args.information:
        is_log = i18n["yes"] if settings.is_log else i18n["no"]
        is_show_log = i18n["yes"] if settings.is_show_log else i18n["no"]

        await cui.display_message(i18n["program_info"].format(settings.version,
                                                              "https://github.com/BRamil0/Translitbukv/",
                                                              i18n.get_lm().info.name, is_log, is_show_log))

    elif args.version:
        await cui.display_message(i18n["version_info"].format(settings.version))

    elif args.author:
        await cui.display_message(i18n["author_info"].format("https://radomyr.net/",
                                                             "https://github.com/BRamil0",
                                                             "qulowg@gmail.com"))

    elif args.github:
        await cui.display_message(i18n["github_info"].format("https://github.com/BRamil0/Translitbukv"))

    elif args.information_dictionary:
        if args.dictionary:
            dictionary_name = args.dictionary
        else:
            dictionary_name = args.information_dictionary

        dictionary: Dictionary | None = await search_dictionary(dm, dictionary_name)
        if dictionary is None:
            logger.error(f"Словник {dictionary_name} не знайдено.")
            await cui.display_message(i18n["dictionary_not_found"].format(dictionary_name))
            return None
        await cui.display_dictionary(dictionary)

    elif args.list_dictionary:
        if not dm.get_list_dictionaries():
            await cui.display_message(i18n["no_dictionaries_found"])
        else:
            await cui.display_dictionary_list(dm)

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
        logger.debug(
            f"Виконання транслітерації з файлу {input_path} за словником {args.dictionary} у файл {output_path}"
        )
        await files_mode(dm, args.dictionary, input_path, output_path)

    else:
        await interactive_mode(dm)

    return None

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError, UnicodeDecodeError) as error:
        asyncio.run(cui.display_message("\n" + i18n["transliteration_exiting"]))
        logger.debug(f"Вихід з програми через помилку: {error}, скоріше за все, це було викликано натисканням Ctrl+C або Ctrl+D.")