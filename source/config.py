import pydantic_settings
from pathlib import Path

class Settings(pydantic_settings.BaseSettings):
    is_log: bool = True
    is_show_log: bool = False
    LOG_DIR: Path = Path(__file__).parent.parent / "temp" / "logs"
    LOG_FORMAT: str = "<y>IDP:{process}</y> <ly>SPT:{elapsed}</ly> | <g>{time:YYYY-MM-DD}</g> <lg>{time:HH:mm:ss}</lg> | <level>{level}</level> | <m>F:{file}</m> <lm>L:{line} FU:{function}</lm> | {message}"


    model_config = pydantic_settings.SettingsConfigDict(json_file=(Path(__file__).parent.parent / "config.json"))

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

settings = Settings()
