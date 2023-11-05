import asyncio
import aiohttp

from utils import parse_data, parse_args


class Fetcher:
    def __init__(self,
                 num_conn: int,
                 path_to_urls: str,
                 page_callback: callable = parse_data
                 ):
        self.num_conn = num_conn
        self.path_to_urls = path_to_urls
        self.async_urls_queue = asyncio.Queue()
        self.page_callback = page_callback

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
                    self.async_urls_queue.put_nowait(url)
                else:
                    await self.async_urls_queue.put(url)

    async def fetch_url(self, url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return self.page_callback(await resp.text())


async def main():
    fetcher = Fetcher(*parse_args())
    await fetcher.batch_fetch()


if __name__ == "__main__":
    asyncio.run(main())
