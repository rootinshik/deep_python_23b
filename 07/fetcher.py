import asyncio
import json
import sys
from collections import Counter
from string import ascii_lowercase

import aiohttp
from bs4 import BeautifulSoup


class Fetcher:
    def __init__(
        self, num_conn: int, path_to_urls: str
    ):
        self.num_conn = num_conn
        self.path_to_urls = path_to_urls
        self.async_urls_queue = asyncio.Queue()

    async def batch_fetch(self) -> None:
        await self.url_from_file()
        workers = [
            asyncio.create_task(self.fetch_worker()) for _ in range(self.num_conn)
        ]
        await self.async_urls_queue.join()
        for worker in workers:
            worker.cancel()

    async def fetch_worker(self) -> None:
        while True:
            url = await self.async_urls_queue.get()
            try:
                print(await self.fetch_url(url))
            finally:
                self.async_urls_queue.task_done()

    async def url_from_file(self) -> None:
        with open(self.path_to_urls, "r", encoding="utf-8") as file:
            for num, url in enumerate(file.readlines(), start=1):
                if num % self.num_conn != 0:
                    self.async_urls_queue.put_nowait(url.strip())
                else:
                    await self.async_urls_queue.put(url.strip())

    @staticmethod
    async def fetch_url(url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return f"{url}: {Fetcher.parse_response(await resp.text())}"

    @staticmethod
    def parse_response(data: str, top_k: int = 5) -> str:
        data = BeautifulSoup(data, "html.parser").get_text().lower().split()
        words = filter(lambda word: all(sym in ascii_lowercase for sym in word), data)
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
