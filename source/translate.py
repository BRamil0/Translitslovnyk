from source.dictionary import Dictionary
from source.logger import logger


class Translate:
    """
    Клас для транслітування або зворотного транслітування тексту за словником.
    """

    dictionary: Dictionary
    text: str

    def __init__(self, dictionary: Dictionary, text: str) -> None:
        self.dictionary = dictionary
        self.text = text
        logger.debug(f"[Translate] Ініціалізовано об'єкт з текстом: '{self.text}' та словником з {len(self.dictionary.dictionary)} елементами")

    def set_text(self, new_text: str) -> None:
        logger.info(f"[Translate] Змінено текст з '{self.text}' на '{new_text}'")
        self.text = new_text

    def set_dictionary(self, new_dictionary: Dictionary) -> None:
        logger.info(f"[Translate] Оновлено словник з {len(self.dictionary.dictionary)} до {len(new_dictionary.dictionary)} елементів")
        self.dictionary = new_dictionary

    def transliterate(self) -> str:
        """
        Ітеративно транслітує текст, використовуючи словник.
        Якщо ключа не знайдено, символ залишається без змін.
        """
        logger.debug(f"[Translate] Початок транслітерації {self.text}")
        result = []
        i = 0
        text_len = len(self.text)

        # Сортуємо ключі словника за спаданням довжини ключа
        keys_sorted = sorted(self.dictionary.dictionary.keys(), key=len, reverse=True)

        while i < text_len:
            matched = False
            for key in keys_sorted:
                key_len = len(key)
                # Перевіряємо, чи входить ключ у підрядок тексту
                if i + key_len <= text_len and self.text[i:i + key_len] == key:
                    replacement = self.dictionary[key]
                    logger.info(
                        f"[Translate] Заміна: '{key}' -> '{replacement}' на позиції {i}"
                    )
                    result.append(replacement)
                    i += key_len
                    matched = True
                    break
            if not matched:
                logger.warning(
                    f"[Translate] Символ '{self.text[i]}' на позиції {i} не знайдено у словнику. Залишається без змін."
                )
                result.append(self.text[i])
                i += 1

        final_text = ''.join(result)
        logger.debug(f"[Translate] Результат транслітерації: '{final_text}'")
        return final_text
