"""
Файл по роботи зі словниками.
"""
import json
from pathlib import Path

import aiofiles
import pydantic

from source.logger import logger


class DictionaryModel(pydantic.BaseModel):
    """Модель словника."""
    class InfoModel(pydantic.BaseModel):
        name: str

    data: dict[str, str] | None = None
    info: InfoModel

class IODictionary:
    """Клас для роботи з файлами словників."""

    path: Path = Path(Path(__file__).parent.parent, "dictionaries")

    def __init__(self, path: Path | None = None) -> None:
        if path:
            if not isinstance(path, Path):
                logger.error("[IODictionary] Об'єкт path має бути типу Path")
                raise TypeError("Path must be a Path object")
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
            return DictionaryModel.model_validate_json(content)

    async def write_dictionary(self, filename: Path | str, dictionary: DictionaryModel, directorate: Path | None = None) -> DictionaryModel:
        if isinstance(filename, str):
            path: Path = (self.path if directorate is None else directorate) / filename
        else:
            if not isinstance(filename, Path):
                logger.error("[IODictionary] Об'єкт filename має бути типу Path або str")
                raise TypeError("Filename must be a Path or str object")
            path = filename
        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            await f.write(dictionary.model_dump_json(indent=4, exclude_none=True))
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


    def __getitem__(self, key):
        return self.dictionary.data.__getitem__(key)

    def __setitem__(self, key, value):
        self.dictionary.data.__setitem__(key, value)

    def __delitem__(self, key):
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
