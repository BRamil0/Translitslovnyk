"""
Клас для транслітерування тексту за словником.
"""
import unicodedata
from source.dictionary import Dictionary
from source.logger import logger


class Translate:
    """
    Клас для транслітерування або зворотного транслітерування тексту за словником.
    """

    dictionary: Dictionary
    text: str
    _normalized_data: dict

    def __init__(self, dictionary: Dictionary, text: str | None = None) -> None:
        if not isinstance(dictionary, Dictionary):
            logger.error("[Translate] Помилка ініціалізації: 'dictionary' має бути екземпляром класу Dictionary")
            raise TypeError("Параметр 'dictionary' має бути екземпляром класу Dictionary")
        if not isinstance(text, str) and text is not None:
            logger.error("[Translate] Помилка ініціалізації: 'text' має бути рядком")
            raise TypeError("Параметр 'text' має бути рядком")

        self.set_dictionary(dictionary)

        if text is None:
            text = ""
        self.text = text
        logger.debug(f"[Translate] Ініціалізовано об'єкт з текстом: '{self.text}' та словником з {len(self.dictionary.dictionary.data)} елементами")

    def get_text(self) -> str:
        return self.text

    def set_text(self, new_text: str) -> None:
        if not isinstance(new_text, str):
            logger.error("[Translate] Помилка ініціалізації: 'text' має бути рядком")
            raise TypeError("Параметр 'text' має бути рядком")
        logger.info(f"[Translate] Змінено текст з '{self.text}' на '{new_text}'")
        self.text = new_text

    def get_dictionary(self) -> Dictionary:
        return self.dictionary

    def set_dictionary(self, new_dictionary: Dictionary) -> None:
        if not isinstance(new_dictionary, Dictionary):
            logger.error("[Translate] Помилка ініціалізації: 'dictionary' має бути екземпляром класу Dictionary")
            raise TypeError("Параметр 'dictionary' має бути екземпляром класу Dictionary")

        self.dictionary = new_dictionary
        # <<< ЗМІНА: Нормалізуємо дані словника ОДИН раз при його встановленні
        self._normalized_data = {
            unicodedata.normalize('NFC', k): v
            for k, v in self.dictionary.dictionary.data.items()
        }
        logger.info(f"[Translate] Оновлено та нормалізовано словник з {len(self.dictionary.dictionary.data)} до {len(self._normalized_data)} елементів")

    def transliterate(self, text: str | None = None) -> str:
        """
        Ітеративно транслітує текст, використовуючи словник.
        Якщо ключа не знайдено, символ залишається без змін.
        """

        if text is not None:
            self.set_text(text)

        normalized_input_text = unicodedata.normalize('NFC', self.text)
        logger.debug(f"[Translate] Початок транслітерації нормалізованого тексту: {normalized_input_text}")

        result = []
        i = 0
        text_len = len(normalized_input_text)

        keys_sorted = sorted(self._normalized_data.keys(), key=len, reverse=True)

        while i < text_len:
            matched = False
            for key in keys_sorted:
                key_len = len(key)
                if i + key_len <= text_len and normalized_input_text[i:i + key_len] == key:
                    replacement = self._normalized_data[key]
                    logger.info(
                        f"[Translate] Заміна: '{key}' -> '{replacement}' на позиції {i}"
                    )
                    result.append(replacement)
                    i += key_len
                    matched = True
                    break
            if not matched:
                char_to_append = normalized_input_text[i]
                logger.warning(
                    f"[Translate] Символ '{char_to_append}' на позиції {i} не знайдено у словнику. Залишається без змін."
                )
                result.append(char_to_append)
                i += 1

        final_text = ''.join(result)
        logger.debug(f"[Translate] Результат транслітерації: '{final_text}'")
        return final_text