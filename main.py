"""
Головний файл програми
"""
import asyncio
from source.logger import logger
from source.dictionary import Dictionary
from source.translate import Translate


async def main() -> None:
    """

    :return:
    """
    dictionary = Dictionary("test.json")
    await dictionary.load()
    translator = Translate(dictionary, input("Текст: "))
    print(translator.transliterate())

    return

if __name__ == "__main__":
    asyncio.run(main())