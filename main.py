"""
Основний файл програми.
"""
import asyncio

from source.dictionary import Dictionary, DictionaryManager
from source.translate import Translate
from source.internationalization import internationalization, i18n

async def main() -> None:
    """

    :return:
    """
    await internationalization.load_localization()
    list_dictionaries = DictionaryManager()
    await list_dictionaries.index()

    translator = Translate(list_dictionaries["test"], input(i18n["text"]))
    print(translator.transliterate())

    return

if __name__ == "__main__":
    asyncio.run(main())