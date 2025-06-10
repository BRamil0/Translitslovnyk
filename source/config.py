"""
Файл відповідає за налаштування програми.
"""
import pydantic_settings
from pathlib import Path

import aiofiles

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
        return (pydantic_settings.JsonConfigSettingsSource(settings_cls),)

    async def safe_settings(self) -> None:
        """
        Асинхронний метод для безпечного збереження налаштувань.
        """
        async with aiofiles.open(self.PATH_JSON_FILE_SETTINGS, mode='w', encoding='utf-8') as f:
            await f.write(self.model_dump_json(indent=4, exclude_none=True))

settings: Settings = Settings()
