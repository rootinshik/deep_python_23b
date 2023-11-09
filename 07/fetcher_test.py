import time
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
        mock_get.return_value.__aenter__.return_value.text.return_value\
            = "test content"

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
    async def test_speed_dependence_number_of_tasks(self, _, mock_get):
        async def client_session_get_load():
            await asyncio.sleep(0.01)
            return "test content"

        mock_get.return_value.__aenter__.return_value.text.side_effect\
            = client_session_get_load

        time_1_task = time.time()
        fetcher = Fetcher(1, "/dev/null")
        await fetcher.batch_fetch()
        time_1_task = time.time() - time_1_task

        time_10_task = time.time()
        fetcher = Fetcher(10, "/dev/null")
        await fetcher.batch_fetch()
        time_10_task = time.time() - time_10_task

        self.assertGreater(time_1_task, time_10_task)


if __name__ == "__main__":
    unittest.main()
