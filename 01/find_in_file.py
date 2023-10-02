from typing import Union, TextIO, Generator


def find_in_file(
    file: Union[str, TextIO], words_to_find: list[str], encoding: str = "UTF-8"
) -> Generator[str, TypeError]:
    def words_in_string(search_line: str, words: list[str]) -> bool:
        for word in map(lambda str_: str_.lower(), words):
            if word in search_line.lower().split():
                return True
        return False

    if not isinstance(file, str) and not isinstance(file, TextIO):
        return TypeError("file_input must be str or TextIO")

    is_opened = False
    if isinstance(file, str):
        file = open(file, encoding=encoding, mode="r")
        is_opened = True

    for line in file:
        if words_in_string(line, words_to_find):
            yield line

    if is_opened:
        file.close()
