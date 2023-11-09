import asyncio
import json
import sys
from collections import Counter
from string import ascii_lowercase
from typing import Generator, Coroutine

import aiohttp
from bs4 import BeautifulSoup


class Fetcher:
    def __init__(self, num_conn: int, path_to_urls: str):
        self.num_conn = num_conn
        self.path_to_urls = path_to_urls

    async def batch_fetch(self) -> None:
        url_from_file_gen = Fetcher.url_from_file(self.path_to_urls)
        workers = [
            asyncio.create_task(self.fetch_worker(url_from_file_gen))
            for _ in range(self.num_conn)
        ]
        await asyncio.gather(*workers)

    @staticmethod
    async def fetch_worker(url_from_file_gen: Generator[str, None, None]
                           ) -> Coroutine[None, None, None]:
        while True:
            try:
                print(await Fetcher.fetch_url(next(url_from_file_gen)))
            except StopIteration:
                break

    @staticmethod
    def url_from_file(path_to_urls) -> Generator[str, None, None]:
        with open(path_to_urls, "r", encoding="utf-8") as file:
            for url in file.readlines():
                yield url.strip()

    @staticmethod
    async def fetch_url(url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return f"{url}: {Fetcher.parse_response(await resp.text())}"

    @staticmethod
    def parse_response(data: str, top_k: int = 5) -> str:
        data = BeautifulSoup(data, "html.parser"). \
            get_text().lower().split()
        words = filter(lambda word:
                       all(sym in ascii_lowercase for sym in word),
                       data)
        word_count = dict(Counter(words).most_common(top_k))
        return json.dumps(word_count, ensure_ascii=False)


def parse_args() -> tuple[int, str]:
    if 3 <= len(sys.argv) <= 4:
        return int(sys.argv[-2]), sys.argv[-1]
    raise ValueError


async def main():
    fetcher = Fetcher(*parse_args())
    await fetcher.batch_fetch()


if __name__ == "__main__":
    asyncio.run(main())
