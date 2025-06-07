"""
Інтерфейс користувача для консолі.
"""

from source.dictionary import DictionaryManager
from source.internationalization import i18n


class ConsoleUI:
    """
    Клас для взаємодії з користувачем через консоль.
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    async def display_message(message: str) -> None:
        """
        Відображає повідомлення в консолі.

        :param message: Повідомлення для відображення.
        """
        print(message)

    @staticmethod
    async def get_input(prompt: str) -> str:
        """
        Отримує вхідні дані від користувача.

        :param prompt: Запит для користувача.
        :return: Введені дані.
        """
        return input(prompt)

    async def display_dictionary_list(self, dictionary_manager: DictionaryManager) -> None:
        """
        Відображає список словників.

        :param dictionary_manager: Менеджер словників.
        """
        await self.display_message(i18n["list_dictionaries"])
        for key in dictionary_manager.get_list_dictionaries():
            await self.display_message(f"{dictionary_manager[key].dictionary.info.name} - {key}")

cui: ConsoleUI = ConsoleUI()

