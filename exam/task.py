import threading
from typing import Generator


def create_files(
    file_name: str = "input.txt", k: int = 1, template_name: str = "output"
) -> None:
    def line_generator(source_file_name: str, line_num: int) -> Generator:
        with open(source_file_name, mode="r", encoding="UTF-8") as source_file:
            for num, line in enumerate(source_file):
                if num % k == line_num:
                    yield line

    def write_to_file(index: int, gen: Generator) -> None:
        new_file_name = f"{template_name}_{index}.txt"
        with open(new_file_name, mode="w", encoding="UTF-8") as new_file:
            for line in gen:
                new_file.write(line)

    generators = [line_generator(file_name, i) for i in range(k)]
    threads = []
    for i in range(k):
        thread = threading.Thread(target=write_to_file, args=(i + 1, generators[i]))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    create_files("input.txt", 3)
