"""
Файл відповідає за налаштування програми.
"""
import json
from pathlib import Path

import pydantic_settings
import aiofiles

class CustomJsonConfigSettingsSource(pydantic_settings.JsonConfigSettingsSource):
    """
    Спеціалізований завантажувач налаштувань з JSON, якій
    коректно обробляє порожні, відсутні або пошкоджені файли.
    """
    def _read_file(self, file_path: Path) -> dict[str, object]:
        """
        Перевизначаємо метод читання файлу, щоб обробити помилки.
        """
        try:
            return super()._read_file(file_path)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Файл налаштувань не знайдено або пошкоджено. Використовуються налаштування за замовчуванням.")
            return {}

class Settings(pydantic_settings.BaseSettings):
    """Клас налаштувань програми."""

    language: str = "ukr"
    version: str = "1.0.0"

    is_log: bool = True
    is_show_log: bool = False
    LOG_FORMAT: str = "<y>IDP:{process}</y> <ly>SPT:{elapsed}</ly> | <g>{time:YYYY-MM-DD}</g> <lg>{time:HH:mm:ss}</lg> | <level>{level}</level> | <m>F:{file}</m> <lm>L:{line} FU:{function}</lm> | {message}"

    path_dictionaries: Path = Path(__file__).parent.parent / "dictionaries"
    path_internationalization: Path = Path(__file__).parent.parent / "internationalization"

    PATH_LOG_DIR: Path = Path(__file__).parent.parent / "temp" / "logs"
    PATH_TEMP: Path = Path(__file__).parent.parent / "temp"
    PATH_JSON_FILE_SETTINGS: Path = Path(__file__).parent.parent / "config.json"

    model_config = pydantic_settings.SettingsConfigDict(json_file=PATH_JSON_FILE_SETTINGS)

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: type[pydantic_settings.BaseSettings],
            init_settings: pydantic_settings.PydanticBaseSettingsSource,
            env_settings: pydantic_settings.PydanticBaseSettingsSource,
            dotenv_settings: pydantic_settings.PydanticBaseSettingsSource,
            file_secret_settings: pydantic_settings.PydanticBaseSettingsSource,
    ) -> tuple[pydantic_settings.PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            CustomJsonConfigSettingsSource(settings_cls),
            file_secret_settings,
        )

    async def save_settings(self, save_path: bool = False) -> None:
        """
        Асинхронний метод для безпечного збереження налаштувань.
        """
        if save_path:
            exclude = {}
        else:
            exclude = {"PATH_LOG_DIR", "PATH_TEMP", "path_dictionaries", "path_internationalization"}

        async with aiofiles.open(self.PATH_JSON_FILE_SETTINGS, mode='w', encoding='utf-8') as f:
            await f.write(self.model_dump_json(indent=4, exclude_none=True, exclude=exclude))

settings: Settings = Settings()
