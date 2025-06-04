"""
Файл відповідає за локалізацію (інтернаціоналізацію) програми.
"""
from pathlib import Path

import aiofiles
import pydantic

from source.config import settings
from source.logger import logger


class LanguageModel(pydantic.BaseModel):
    """Модель для зберігання даних локалізації."""

    class InfoModel(pydantic.BaseModel):
        code_3: str

    data: dict[str, str] | None = None
    info: InfoModel


class Internationalization:
    """Клас для управління локалізацією програми."""

    lm: LanguageModel | None = None
    path: Path = Path(Path(__file__).parent.parent, "internationalization")
    language: str = settings.language

    def __init__(self, path: Path | None = None, language: str | None = None) -> None:
        if path:
            if not isinstance(path, Path):
                logger.error("[Internationalization] Об'єкт path має бути типу Path")
                raise TypeError("Path must be a Path object")
            logger.debug(f"[Internationalization] Значення path встановлено: {path}, було {self.path}")
            self.path = path
        if language:
            if not isinstance(language, str):
                logger.error("[Internationalization] Об'єкт language має бути типу str")
                raise TypeError("Language must be a str object")
            self.language = language
            logger.debug(f"[Internationalization] Значення language встановлено: {language}, було {self.language}")
        self.lm = None
        logger.debug(f"[Internationalization] Ініціалізація Internationalization з path: {self.path}, language: {self.language}")

    def __getitem__(self, item: str) -> str:
        if not isinstance(item, str):
            logger.error(f"Ключ '{item}' має бути типу str, отримано {type(item)}")
            raise TypeError("Key must be a string")

        if not self.lm:
            logger.error("Словник локалізації не завантажено.")
            raise KeyError("Language data not loaded")
        if not self.lm.data:
            logger.warning(f"Словник локалізації порожній, повертається ключ: {item}")
            return item

        value = self.lm.data.get(item)
        if value is None:
            logger.warning(f"Значення для ключа '{item}' не знайдено, повертається ключ.")
            return item

        logger.debug(f"Значення для ключа '{item}' знайдено: {value}")
        return value


    def get_lm(self) -> LanguageModel:
        return self.lm

    def get_path(self) -> Path:
        return self.path

    def set_path(self, path: Path) -> None:
        if not isinstance(path, Path):
            logger.error("[Internationalization] Об'єкт path має бути типу Path")
            raise TypeError("Path must be a Path object")
        logger.debug(f"[Internationalization] Значення path встановлено: {path}, було {self.path}")
        self.path = path

    def get_language(self) -> str:
        return self.language

    def set_language(self, language: str) -> None:
        if not isinstance(language, str):
            logger.error("[Internationalization] Об'єкт language має бути типу str")
            raise TypeError("Language must be a str object")
        logger.debug(f"[Internationalization] Значення language встановлено: {language}, було {self.language}")
        self.language = language

    async def load_localization(self, language: str | None = None) -> LanguageModel:
        language = language or self.language
        if not isinstance(language, str):
            logger.error("[Internationalization] Об'єкт language має бути типу str")
            raise TypeError("Language must be a str object")
        path = self.path / f"{language}_language.json"
        try:
            async with aiofiles.open(path, "r", encoding="utf-8") as f:
                content = await f.read()
                self.lm = LanguageModel.model_validate_json(content)
                logger.info(f"[Internationalization] Локалізація завантажена з файлу: {path.name}")
                return self.lm
        except FileNotFoundError as e:
            logger.error(f"[Internationalization] Файл локалізації '{path.name}' не знайдено, помилка: {e}.")
            raise
        except pydantic.ValidationError as e:
            logger.error(f"[Internationalization] Помилка валідації локалізації з файлу: {path.name}, помилка: {e}.")
            raise
        except TypeError as e:
            logger.error(f"[Internationalization] Помилка типу при завантаженні локалізації з файлу: {path.name}, помилка: {e}.")
            raise
        except Exception as e:
            logger.exception(f"[Internationalization] Помилка при завантаженні локалізації з файлу: {path.name}, помилка: {e}.")
            raise


internationalization: Internationalization = Internationalization()
i18n: Internationalization = internationalization
