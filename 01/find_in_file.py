from typing import Union, Generator, TextIO
from io import IOBase


def find_in_file(
    file: Union[str, IOBase], words_to_find: list[str], encoding: str = "UTF-8"
) -> Generator[str, None, None]:
    def words_in_line(search_line: bytes, words: list[str]) -> bool:
        for word in map(lambda str_: str_.lower(), words):
            if word in search_line.lower().split():
                return True
        return False

    def base_generator(
        file_: str | IOBase | TextIO,
        words_to_find_: list[str],
    ) -> Generator[str, None, None]:
        for line in file_:
            if words_in_line(line, words_to_find_):
                yield line.strip()

    if not isinstance(file, (str, IOBase)):
        raise AttributeError("file_input must be str or TextIO")

    if isinstance(file, str):
        with open(file, encoding=encoding, mode="r") as file_obj:
            yield from base_generator(file_obj, words_to_find)

    else:
        yield from base_generator(file, words_to_find)
