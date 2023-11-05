import asyncio
import unittest
from unittest.mock import patch, mock_open, call

from fetcher import Fetcher


class TestFetcher(unittest.IsolatedAsyncioTestCase):
    URLS = "\n".join([f"link_{i}" for i in range(100)])

    @patch("fetcher.open", mock_open(read_data=URLS))
    @patch("fetcher.aiohttp.ClientSession.get")
    @patch("fetcher.print")
    async def test_fetch_all_urls(self, _, mock_get):
        fetcher = Fetcher(10, "/dev/null")
        await fetcher.batch_fetch()

        mock_get.assert_has_calls(
            [call(link)
             for link in TestFetcher.URLS.split("\n")],
            any_order=True
        )

    @patch("fetcher.open", mock_open(read_data=URLS))
    @patch("fetcher.aiohttp.ClientSession.get")
    @patch("fetcher.print")
    async def test_num_tasks(self, _, __):
        fetcher = Fetcher(10, "/dev/null")
        loop = asyncio.get_event_loop()
        await fetcher.batch_fetch()
        self.assertEqual(11, len(asyncio.all_tasks(loop)))

        fetcher = Fetcher(5, "/dev/null")
        loop = asyncio.get_event_loop()
        await fetcher.batch_fetch()
        self.assertEqual(6, len(asyncio.all_tasks(loop)))


if __name__ == "__main__":
    unittest.main()
