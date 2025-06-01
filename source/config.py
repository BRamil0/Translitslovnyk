import pydantic_settings
from pathlib import Path

class Settings(pydantic_settings.BaseSettings):
    is_log: bool = False
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

print(Path(__file__).parent.parent / "config.json")
settings = Settings()
