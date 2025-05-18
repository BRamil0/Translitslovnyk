"""

"""
import json
import aiofiles
from pathlib import Path


class IODictionary:
    path: Path = Path(Path(__file__).parent.parent, "dictionaries")

    def __init__(self, path: Path | None = None) -> None:
        if path:
            self.path = path

    async def read_dictionary(self, filename: Path | str, directorate: Path | None = None) -> dict[str, str | dict]:
        if isinstance(filename, str):
            path: Path = (self.path if directorate is None else directorate) / filename
        else:
            path = filename
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            content = await f.read()
            return json.loads(content)

    async def write_dictionary(self, filename: Path | str, dictionary: dict[str, str | dict], directorate: Path | None = None) -> dict[str, str | dict]:
        if isinstance(filename, str):
            path: Path = (self.path if directorate is None else directorate) / filename
        else:
            path = filename
        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(dictionary, indent=4))
        return dictionary

class Dictionary:
    file: Path
    dictionary: dict
    iod: IODictionary

    def __init__(self, file: Path, iod: IODictionary | None) -> None:
        self.dictionary = {}
        self.file = file
        self.iod = iod if iod else IODictionary()

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