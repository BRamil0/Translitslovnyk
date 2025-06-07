"""
Основний файл програми.
"""
import asyncio
import argparse

from source.dictionary import Dictionary, DictionaryManager
from source.translate import Translate
from source.internationalization import internationalization, i18n
from source.console_ui import cui
from source.command_line_handler import parse_command_line_arguments
from source.logger import logger

async def interactive_mode(dm: DictionaryManager, selected_text: str | None = None, selected_dictionary: Dictionary | None = None) -> None:
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
        return None
    if (args.dictionary or args.text) and not args.output:
        if args.input:
            pass
        else:
            text = args.text
        await interactive_mode(dm, text, args.dictionary)
    elif args.input and args.output:
        pass
    return None

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError) as e:
        print("\n")
        asyncio.run(cui.display_message(i18n["transliteration_exiting"]))
        logger.debug(f"Вихід з програми через помилку: {e}, скоріше за все, це було викликано натисканням Ctrl+C або Ctrl+D.")