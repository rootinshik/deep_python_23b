from typing import Union, TextIO, Generator


def find_in_file(
    file: Union[str, TextIO], words_to_find: list[str], encoding: str = "UTF-8"
) -> Generator[str, None, AttributeError]:
    def words_in_line(search_line: str, words: list[str]) -> bool:
        for word in map(lambda str_: str_.lower(), words):
            if word in search_line.lower().split():
                return True
        return False

    def base_generator(file_: TextIO, words_to_find_: list[str]):
        for line in file_:
            if words_in_line(line, words_to_find_):
                yield line.strip()

    if not isinstance(file, (str, TextIO)):
        raise AttributeError("file_input must be str or TextIO")

    if isinstance(file, str):
        with open(file, encoding=encoding, mode="r") as file_obj:
            yield from base_generator(file_obj, words_to_find)

    if isinstance(file, TextIO):
        yield from base_generator(file, words_to_find)
