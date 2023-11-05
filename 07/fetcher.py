import asyncio
from typing import Callable

import aiohttp

from utils import parse_response, parse_args, return_status_code


class Fetcher:
    def __init__(self,
                 num_conn: int,
                 path_to_urls: str,
                 resp_callback: Callable = return_status_code
                 ):
        self.num_conn = num_conn
        self.path_to_urls = path_to_urls
        self.async_urls_queue = asyncio.Queue()
        self.resp_callback = resp_callback

    async def batch_fetch(self) -> None:
        await self.url_from_file()
        workers = [
            asyncio.create_task(self.fetch_worker())
            for _ in range(self.num_conn)
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

    async def fetch_url(self, url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await self.resp_callback(resp)


async def main():
    fetcher = Fetcher(*parse_args(),
                      resp_callback=parse_response)
    await fetcher.batch_fetch()


if __name__ == "__main__":
    asyncio.run(main())
