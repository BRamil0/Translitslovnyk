"""
Інтерфейс користувача для консолі.
"""

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

cui: ConsoleUI = ConsoleUI()
