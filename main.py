"""
Основний файл програми.
"""
import asyncio

from source.dictionary import Dictionary, DictionaryManager
from source.translate import Translate
from source.internationalization import internationalization, i18n
from source.console_ui import cui

async def main() -> None:
    """
    Головна функція програми.
    """
    await internationalization.load_localization()
    list_dictionaries = DictionaryManager()
    await list_dictionaries.index()
    await cui.display_dictionary_list(list_dictionaries)
    while True:
        selected_dictionary: str = await cui.get_input(i18n["enter_dictionary"])
        if selected_dictionary in list_dictionaries.get_list_dictionaries():
            dictionary: Dictionary = list_dictionaries[selected_dictionary]
            await cui.display_message(i18n["dictionary_selected"].format(dictionary.dictionary.info.name))
            break
        else:
            await cui.display_message(i18n["dictionary_not_found"].format(selected_dictionary))

    translator: Translate = Translate(dictionary)
    while True:
        text: str = await cui.get_input(i18n["enter_text_to_transliterate"])
        if text.lower() == "exit_transliterate_mode":
            await cui.display_message(i18n["transliteration_exiting"])
            break
        await cui.display_message(i18n["transliteration_result"].format(translator.transliterate(text)))

    return

if __name__ == "__main__":
    asyncio.run(main())