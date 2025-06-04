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
            self.path = path
            logger.debug(f"Internationalization path set to: {self.path}")
        if language:
            self.language = language
            logger.debug(f"Internationalization language set to: {self.language}")
        self.lm = None

    def __getitem__(self, item):
        if not self.lm:
            logger.warning("Attempted to access language data before it was loaded.")
            raise KeyError("Language data not loaded")
        if not self.lm.data:
            logger.warning(f"Language model has no data for key '{item}', returning key itself.")
            return item
        value = self.lm.data.get(item)
        if value is None:
            logger.warning(f"Missing translation for key '{item}', returning key itself.")
            return item
        logger.debug(f"Translation found for key '{item}': '{value}'")
        return value


    def get_lm(self) -> LanguageModel:
        return self.lm

    def get_path(self) -> Path:
        return self.path

    def set_path(self, path: Path) -> None:
        self.path = path
        logger.debug(f"Internationalization path changed to: {self.path}")

    def get_language(self) -> str:
        return self.language

    def set_language(self, language: str) -> None:
        self.language = language
        logger.info(f"Language changed to: {self.language}")

    async def load_localization(self, language: str | None = None) -> LanguageModel:
        language = language or self.language
        path = self.path / f"{language}_language.json"
        try:
            async with aiofiles.open(path, "r", encoding="utf-8") as f:
                content = await f.read()
                self.lm = LanguageModel.model_validate_json(content)
                logger.info(f"Localization file '{path.name}' loaded successfully.")
                return self.lm
        except FileNotFoundError:
            logger.error(f"Localization file '{path.name}' not found.")
            raise
        except Exception as e:
            logger.exception(f"Error loading localization file '{path.name}': {e}")
            raise


internationalization: Internationalization = Internationalization()
i18n: Internationalization = internationalization
