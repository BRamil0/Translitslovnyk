"""
Інтерфейс користувача для консолі.
"""

from rich.console import Console
from rich.table import Table

from source.dictionary import DictionaryManager, Dictionary
from source.internationalization import i18n


class ConsoleUI:
    """
    Клас для взаємодії з користувачем через консоль.
    """
    console: Console

    def __init__(self, console: Console | None = None) -> None:
        if console is not None:
            self.console = console
        else:
            self.console = Console()

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


    async def display_dictionary(self, dictionary: Dictionary):
        """
        Відображає інформацію про словник.

        :param dictionary: Словник для відображення.
        """
        pass

    async def display_dictionary_list(self, dictionary_manager: DictionaryManager) -> None:
        """
        Відображає список словників.

        :param dictionary_manager: Менеджер словників.
        """
        if not dictionary_manager.get_list_dictionaries():
            await self.display_message(i18n["no_dictionaries_found"])
            return

        table = Table(title=i18n["dictionaries_list_title"])
        table.add_column(i18n["name"], style="cyan", no_wrap=True, min_width=5)
        table.add_column(i18n["author"], style="green", no_wrap=True, min_width=5)
        table.add_column(i18n["example"], style="blue", no_wrap=True, max_width=20)
        table.add_column(i18n["id"], style="cyan", no_wrap=True, min_width=5)
        table.add_column(i18n["version"], style="green", no_wrap=True, min_width=5)
        table.add_column(i18n["file_name"], style="cyan", no_wrap=True, min_width=5)

        for key in dictionary_manager.get_list_dictionaries():
            dictionary = dictionary_manager[key].get_dictionary()
            table.add_row(
                dictionary.info.name,
                dictionary.info.author,
                str(dictionary.info.example or i18n["no_example"]),
                dictionary.info.id,
                dictionary.info.version,
                str(dictionary.info.file_name),
            )
        self.console.print(table)

cui: ConsoleUI = ConsoleUI()

