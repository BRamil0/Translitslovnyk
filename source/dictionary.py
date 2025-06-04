"""
Файл по роботи з словниками.
"""
import json
from pathlib import Path

import aiofiles
import pydantic


class DictionaryModel(pydantic.BaseModel):
    class InfoModel(pydantic.BaseModel):
        name: str

    data: dict[str, str] | None = None
    info: InfoModel

class IODictionary:
    path: Path = Path(Path(__file__).parent.parent, "dictionaries")

    def __init__(self, path: Path | None = None) -> None:
        if path:
            self.path = path

    async def read_dictionary(self, filename: Path | str, directorate: Path | None = None) -> DictionaryModel:
        if isinstance(filename, str):
            path: Path = (self.path if directorate is None else directorate) / filename
        else:
            path = filename
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            content = await f.read()
            return DictionaryModel.model_validate_json(content)

    async def write_dictionary(self, filename: Path | str, dictionary: DictionaryModel, directorate: Path | None = None) -> DictionaryModel:
        if isinstance(filename, str):
            path: Path = (self.path if directorate is None else directorate) / filename
        else:
            path = filename
        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            await f.write(dictionary.model_dump_json(indent=4, exclude_none=True))
        return dictionary

class Dictionary:
    file: Path
    dictionary: DictionaryModel | None
    iod: IODictionary

    def __init__(self, file: Path, iod: IODictionary | None = None) -> None:
        self.dictionary = None
        self.file = file
        self.iod = iod if iod else IODictionary()

    def __getitem__(self, key):
        return self.dictionary.data.__getitem__(key)

    def __setitem__(self, key, value):
        self.dictionary.data.__setitem__(key, value)

    def __delitem__(self, key):
        self.dictionary.data.__delitem__(key)

    async def load(self) -> bool:
        try:
            self.dictionary = await self.iod.read_dictionary(self.file)
            return True
        except (IOError, json.JSONDecodeError):
            return False
    async def dump(self) -> bool:
        try:
            self.dictionary = await self.iod.write_dictionary(self.file, dictionary=self.dictionary)
            return True
        except (IOError, json.JSONDecodeError):
            return False
