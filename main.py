"""
Основний файл програми.
"""
import asyncio

from source.dictionary import Dictionary
from source.translate import Translate
from source.internationalization import internationalization, i18n


async def main() -> None:
    """

    :return:
    """
    await internationalization.load_localization()
    dictionary = Dictionary("test.json")
    await dictionary.load()
    translator = Translate(dictionary, input(i18n["text"]))
    print(translator.transliterate())

    return

if __name__ == "__main__":
    asyncio.run(main())