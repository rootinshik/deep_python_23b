from typing import TextIO


class FileFilter:
    @staticmethod
    def file_to_string_generator(file: TextIO) -> str:
        for line in file:
            yield line

    @staticmethod
    def find_in_file_obj(file: TextIO, word_list: list[str]) -> list[str]:
        filtered_string = []
        for line in FileFilter.file_to_string_generator(file):
            if FileFilter.words_in_string(line, word_list):
                filtered_string.append(line)
        return filtered_string

    @staticmethod
    def find_in_file(path: str, word_list: list[str]) -> list[str]:
        with open(path, "r") as search_file:
            return FileFilter.find_in_file_obj(search_file, word_list)

    @staticmethod
    def words_in_string(search_string: str, words_to_find: list[str]) -> bool:
        for word in map(lambda str_: str_.lower(), words_to_find):
            if word in search_string.lower():
                return True
