from typing import Union, TextIO, Generator


def find_in_file(
    file_input: Union[str, TextIO],
    words_to_find: list[str],
    encoding: str = "UTF-8"
) -> Generator[str, TypeError]:
    def words_in_string(search_line: str, words: list[str]) -> bool:
        for word in map(lambda str_: str_.lower(), words):
            if word in search_line.lower().split():
                return True
        return False

    if not isinstance(file_input, str) and not isinstance(file_input, TextIO):
        return TypeError("file_input must be str or TextIO")

    is_opened = False
    if isinstance(file_input, str):
        file_input = open(file_input, encoding=encoding, mode="r")
        is_opened = True

    for line in file_input:
        if words_in_string(line, words_to_find):
            yield line

    if is_opened:
        file_input.close()
