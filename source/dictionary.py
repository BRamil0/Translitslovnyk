"""
Файл по роботи зі словниками.
"""
import json
from pathlib import Path

import aiofiles
import pydantic

from source.config import settings
from source.logger import logger


class DictionaryModel(pydantic.BaseModel):
    """Модель словника."""
    class InfoModel(pydantic.BaseModel):
        name: str
        description: str
        example: str = ""

        author: str
        author_url: str = ""
        author_email: str = ""

        from_language: str
        to_language: str

        version: str
        id: str

        license: str
        license_url: str = ""

        created_at: str = ""
        updated_at: str = ""

        source: str = ""
        source_url: str = ""

        file_name: str = ""
        file_path: Path = Path("")

    data: dict[str, str] | None = None
    info: InfoModel
    model_version: str = "1.0.0"

class IODictionary:
    """Клас для роботи з файлами словників."""

    path: Path = settings.path_dictionaries

    def __init__(self, path: Path | None = None) -> None:
        if path:
            if not isinstance(path, Path):
                logger.error("[IODictionary] Об'єкт path має бути типу Path")
                raise TypeError("Path must be a Path object")
            self.path = path
        logger.debug(f"[IODictionary] Ініціалізація IODictionary з шляхом: {self.path}")

    def get_path(self) -> Path:
        return self.path

    def set_path(self, path: Path) -> None:
        if not isinstance(path, Path):
            logger.error("[IODictionary] Об'єкт path має бути типу Path")
            raise TypeError("Path must be a Path object")
        logger.debug(f"[IODictionary] Значення path встановлено: {path}, було {self.path}")
        self.path = path

    async def read_dictionary(self, filename: Path | str, directorate: Path | None = None) -> DictionaryModel:
        if isinstance(filename, str):
            path: Path = (self.path if directorate is None else directorate) / filename
        else:
            if not isinstance(filename, Path):
                logger.error("[IODictionary] Об'єкт filename має бути типу Path або str")
                raise TypeError("Filename must be a Path or str object")
            path = filename
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            content = await f.read()
            logger.debug(f"[IODictionary] Читання словника з файлу: {path}")
            dictionary = DictionaryModel.model_validate_json(content)
            dictionary.info.file_name = path.name
            dictionary.info.file_path = path
            return dictionary

    async def write_dictionary(self, filename: Path | str, dictionary: DictionaryModel, directorate: Path | None = None) -> DictionaryModel:
        if isinstance(filename, str):
            path: Path = (self.path if directorate is None else directorate) / filename
        else:
            if not isinstance(filename, Path):
                logger.error("[IODictionary] Об'єкт filename має бути типу Path або str")
                raise TypeError("Filename must be a Path or str object")
            path = filename
        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            await f.write(dictionary.model_dump_json(indent=4, exclude_none=True, exclude={'info': {'file_name', 'file_path'}}))
        logger.debug(f"[IODictionary] Запис словника у файл: {path}")
        return dictionary

class Dictionary:
    """Клас для роботи зі словниками."""

    file: Path
    dictionary: DictionaryModel | None
    iod: IODictionary

    def __init__(self, file: Path | str, iod: IODictionary | None = None) -> None:
        if isinstance(file, str):
            file = Path(file)
        elif not isinstance(file, Path):
            raise TypeError("File must be a Path object")
        logger.debug(f"[Dictionary] Ініціалізація словника з файлом: {file}")
        self.dictionary = None
        self.file = file
        self.iod = iod if iod else IODictionary()


    def __getitem__(self, key: str) -> str:
        if self.dictionary is None:
            logger.error("[Dictionary] Словник не завантажено, неможливо отримати значення.")
            raise KeyError("Dictionary not loaded")
        if not isinstance(key, str):
            logger.error("[Dictionary] Ключ має бути типу str")
            raise TypeError("Key must be a string")
        return self.dictionary.data.__getitem__(key)

    def __setitem__(self, key: str, value: str) -> None:
        if self.dictionary is None:
            logger.error("[Dictionary] Словник не завантажено, неможливо встановити значення.")
            raise KeyError("Dictionary not loaded")
        if not isinstance(key, str) or (not isinstance(value, str) and not isinstance(value, dict)):
            logger.error("[Dictionary] Ключ і значення мають бути типу str або dict (тільки для значень словника)")
            raise TypeError("Key and value must be strings")
        self.dictionary.data.__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        if self.dictionary is None:
            logger.error("[Dictionary] Словник не завантажено, неможливо видалити значення.")
            raise KeyError("Dictionary not loaded")
        if not isinstance(key, str):
            logger.error("[Dictionary] Ключ має бути типу str")
            raise TypeError("Key must be a string")
        self.dictionary.data.__delitem__(key)

    def get_file(self) -> Path:
        return self.file

    def set_file(self, path: Path) -> None:
        if not isinstance(path, Path):
            logger.error("[Dictionary] Об'єкт path має бути типу Path")
            raise TypeError("Path must be a Path object")
        logger.debug(f"[Dictionary] Значення path встановлено: {path}, було {self.file}")
        self.file = path

    def get_dictionary(self) -> DictionaryModel | None:
        return self.dictionary

    def set_dictionary(self, dictionary: DictionaryModel) -> None:
        if not isinstance(dictionary, DictionaryModel):
            logger.error("[Dictionary] Об'єкт dictionary має бути типу DictionaryModel")
            raise TypeError("Dictionary must be a DictionaryModel object")
        logger.debug(f"[Dictionary] Значення dictionary встановлено: {dictionary.info.name}, було {self.dictionary.info.name}")
        self.dictionary = dictionary

    def get_iod(self) -> IODictionary:
        return self.iod

    def set_iod(self, iod: IODictionary) -> None:
        if not isinstance(iod, IODictionary):
            logger.error("[Dictionary] Об'єкт iod має бути типу IODictionary")
            raise TypeError("IOD must be an IODictionary object")
        logger.debug(f"[Dictionary] Значення iod встановлено: {iod}, було {self.iod}")
        self.iod = iod

    def get_data(self) -> dict[str, str] | None:
        if self.dictionary is None:
            logger.warning("[Dictionary] Словник не завантажено, повертається None.")
            return None
        return self.dictionary.data

    async def load(self) -> bool:
        try:
            self.dictionary = await self.iod.read_dictionary(self.file)
            if not self.dictionary.data:
                logger.warning(f"[Dictionary] Словник {self.file.name} не містить даних.")
                self.dictionary.data = {}
                return False
            logger.info(f"[Dictionary] Словник {self.file.name} завантажено успішно.")
            return True
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"[Dictionary] Помилка при завантаженні словника {self.file.name}. Детальніше: {e}")
            return False

    async def dump(self) -> bool:
        try:
            self.dictionary = await self.iod.write_dictionary(self.file, dictionary=self.dictionary)
            logger.info(f"[Dictionary] Словник {self.file.name} збережено успішно.")
            return True
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"[Dictionary] Помилка при збереженні словника {self.file.name}. Детальніше: {e}")
            return False

class DictionaryManager:
    """Клас для керування словниками."""
    path_dictionaries: Path = settings.path_dictionaries
    list_dictionaries: dict[str, Dictionary] | None = None

    def __init__(self, path: Path | None = None) -> None:
        if path:
            if not isinstance(path, Path):
                logger.error("[DictionaryManager] Об'єкт path має бути типу Path")
                raise TypeError("Path must be a Path object")
            self.path_dictionaries = path
        logger.debug(f"[DictionaryManager] Ініціалізація DictionaryManager з шляхом: {self.path_dictionaries}")

    def __getitem__(self, key: str) -> Dictionary | None:
        if self.list_dictionaries is None:
            logger.error("[DictionaryManager] Список словників не завантажено, неможливо отримати словник.")
            raise KeyError("Dictionary list not loaded")
        if not isinstance(key, str):
            logger.error("[DictionaryManager] Ключ має бути типу str")
            raise TypeError("Key must be a string")
        dictionary = self.list_dictionaries.get(key)
        if dictionary is None:
            logger.warning(f"[DictionaryManager] Словник з ключем {key} не знайдено.")
            return None
        logger.debug(f"[DictionaryManager] Словник з ключем {key} знайдено: {dictionary.get_file().name}")
        return dictionary

    def get_path_dictionaries(self) -> Path:
        return self.path_dictionaries

    def set_path_dictionaries(self, path: Path) -> None:
        if not isinstance(path, Path):
            logger.error("[DictionaryManager] Об'єкт path має бути типу Path")
            raise TypeError("Path must be a Path object")
        logger.debug(f"[DictionaryManager] Значення path встановлено: {path}, було {self.path_dictionaries}")
        self.path_dictionaries = path

    def get_list_dictionaries(self) -> dict[str, Dictionary] | None:
        if self.list_dictionaries is None:
            logger.warning("[DictionaryManager] Список словників не завантажено, повертається None.")
            return None
        return self.list_dictionaries

    def search_dictionary(self, key: str, field: str | None = None) -> Dictionary | None:
        if not field:
            field = "file_name"
        if self.list_dictionaries is None:
            logger.error("[DictionaryManager] Список словників не завантажено, неможливо отримати словник.")
            raise KeyError("Dictionary list not loaded")
        if not isinstance(key, str):
            logger.error("[DictionaryManager] Ім'я словника має бути типу str")
            raise TypeError("Name must be a string")
        if not isinstance(field, str):
            logger.error("[DictionaryManager] Поле словника має бути типу str")
            raise TypeError("Type must be a string")

        for dictionary in self.list_dictionaries.values():
            if dictionary.get_dictionary() and key == str(getattr(dictionary.get_dictionary().info, field)):
                return dictionary

        for dictionary in self.list_dictionaries.values():
            if dictionary.get_dictionary() and key in str(getattr(dictionary.get_dictionary().info, field)):
                return dictionary

        logger.warning(f"[DictionaryManager] Словник з ім'ям {key} та атрибутом {field} не знайдено.")
        return None

    async def index(self) -> dict[str, Dictionary]:
        """Індексація словників у директорії."""
        if not self.path_dictionaries.exists():
            logger.error(f"[DictionaryManager] Директорія словників не існує: {self.path_dictionaries}")
            raise FileNotFoundError(f"Directory {self.path_dictionaries} does not exist")

        self.list_dictionaries = {}
        for file in self.path_dictionaries.glob("*.json"):
            if file.is_file():
                dictionary = Dictionary(file=file, iod=IODictionary(self.path_dictionaries))
                await dictionary.load()
                self.list_dictionaries[dictionary.get_dictionary().info.file_name] = dictionary
                logger.info(f"[DictionaryManager] Словник {file.name} додано до списку.")

        return self.list_dictionaries
