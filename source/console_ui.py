"""
Інтерфейс користувача для консолі.
"""

from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

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

    async def display_message(self, message: str) -> None:
        """
        Відображає повідомлення в консолі.

        :param message: Повідомлення для відображення.
        """
        self.console.print(message)

    async def get_input(self, prompt: str) -> str:
        """
        Отримує вхідні дані від користувача.

        :param prompt: Запит для користувача.
        :return: Введені дані.
        """
        return self.console.input(prompt)


    async def display_dictionary(self, dictionary: Dictionary):
        """
        Відображає інформацію про словник.

        :param dictionary: Словник для відображення.
        """

        di = dictionary.get_dictionary().info
        text = f"__{i18n["dictionary_info_title"]}__ \n\n"

        for key, value in di.__dict__.items():
            if value is None or value == "":
                value = i18n["no_data"]
            text += f"__{i18n[key]}__: *{value}*  \n"

        self.console.print(Markdown(text))

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
        table.add_column(i18n["example"], style="blue", no_wrap=True, max_width=40)
        table.add_column(i18n["id"], style="cyan", no_wrap=True, min_width=5)
        table.add_column(i18n["version"], style="green", no_wrap=True, min_width=5)
        table.add_column(i18n["file_name"], style="cyan", no_wrap=True, min_width=5)

        for key in dictionary_manager.get_list_dictionaries():
            dictionary = dictionary_manager[key].get_dictionary()
            table.add_row(
                dictionary.info.name,
                dictionary.info.author,
                str(dictionary.info.example or i18n["no_data"]),
                dictionary.info.id,
                dictionary.info.version,
                str(dictionary.info.file_name),
            )
        self.console.print(table)

cui: ConsoleUI = ConsoleUI()

