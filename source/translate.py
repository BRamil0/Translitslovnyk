"""
Клас для транслітерування тексту за словником.
Версія з покращеною нормалізацією Unicode та інтелектуальною обробкою регістру.
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
    _sorted_keys: list

    def __init__(self, dictionary: Dictionary, text: str | None = None) -> None:
        if not isinstance(dictionary, Dictionary):
            logger.error("[Translate] Помилка ініціалізації: 'dictionary' має бути екземпляром класу Dictionary")
            raise TypeError("Параметр 'dictionary' має бути екземпляром класу Dictionary")

        # Ініціалізація через сеттери для уникнення дублювання коду
        self.set_dictionary(dictionary)
        self.set_text(text if text is not None else "")

    def get_text(self) -> str:
        return self.text

    def set_text(self, new_text: str) -> None:
        if not isinstance(new_text, str):
            logger.error("[Translate] Помилка ініціалізації: 'text' має бути рядком")
            raise TypeError("Параметр 'text' має бути рядком")
        logger.info(f"[Translate] Змінено текст з '{self.text if hasattr(self, 'text') else ''}' на '{new_text}'")
        self.text = new_text

    def get_dictionary(self) -> Dictionary:
        return self.dictionary

    def set_dictionary(self, new_dictionary: Dictionary) -> None:
        if not isinstance(new_dictionary, Dictionary):
            logger.error("[Translate] Помилка ініціалізації: 'dictionary' має бути екземпляром класу Dictionary")
            raise TypeError("Параметр 'dictionary' має бути екземпляром класу Dictionary")

        self.dictionary = new_dictionary

        # Нормалізуємо дані словника ОДИН раз при його встановленні
        self._normalized_data = {
            unicodedata.normalize('NFC', k): v
            for k, v in self.dictionary.dictionary.data.items()
        }

        # Сортуємо ключі також ОДИН раз
        self._sorted_keys = sorted(self._normalized_data.keys(), key=len, reverse=True)

        logger.info(f"[Translate] Оновлено, нормалізовано та відсортовано ключі для словника з {len(self._normalized_data)} елементів")

    # Окрема функція для обробки регістру
    def _get_replacement_with_case(self, source_segment: str, replacement: str) -> str:
        """Аналізує регістр вхідного сегмента та застосовує його до заміни."""
        if source_segment.isupper() and len(source_segment) > 1:
            return replacement.upper()
        if source_segment.istitle():
            return replacement.title()
        # Для односимвольних або повністю нижнього регістру заміна залишається як є
        return replacement

    def transliterate(self, text: str | None = None) -> str:
        """
        Ітеративно транслітує текст, використовуючи нормалізований словник
        та інтелектуальну обробку регістру.
        """
        if text is not None:
            self.set_text(text)

        normalized_input_text = unicodedata.normalize('NFC', self.text)
        logger.debug(f"[Translate] Початок транслітерації нормалізованого тексту: {normalized_input_text}")

        result = []
        i = 0
        text_len = len(normalized_input_text)

        while i < text_len:
            matched = False
            for key in self._sorted_keys:
                key_len = len(key)
                source_segment = normalized_input_text[i:i + key_len]

                # Порівнюємо у нижньому регістрі для гнучкості
                if source_segment.lower() == key.lower():
                    #Використовуємо функцію для визначення регістру
                    base_replacement = self._normalized_data[key]
                    replacement = self._get_replacement_with_case(source_segment, base_replacement)

                    logger.info(
                        f"[Translate] Заміна: '{source_segment}' -> '{replacement}' (правило: '{key}' -> '{base_replacement}')"
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