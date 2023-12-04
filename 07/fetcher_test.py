import time
import asyncio
import unittest
from unittest.mock import patch, mock_open, call

from fetcher import Fetcher


class TestFetcher(unittest.IsolatedAsyncioTestCase):
    @staticmethod
    def get_num_links(num: int) -> str:
        return "\n".join([f"link_{i}" for i in range(num)])

    @patch("fetcher.aiohttp.ClientSession.get")
    @patch("fetcher.print")
    async def test_fetch_all_urls(self, mock_print, mock_get):
        with patch(
            "fetcher.open",
            mock_open(read_data=TestFetcher.get_num_links(100))
        ) as _:
            response = [f"link_{i}" for i in range(100)]
            mock_get.return_value.__aenter__.\
                return_value.text.side_effect = response
            print_args = []
            mock_print.side_effect = lambda args: print_args.append(str(args))

            fetcher = Fetcher(10, "/dev/null")
            await fetcher.batch_fetch()

            mock_get.assert_has_calls(
                [call(link)
                 for link in TestFetcher.get_num_links(100).split("\n")],
                any_order=True,
            )
            self.assertEqual([resp + ": {}" for resp in response], print_args)

    @patch("fetcher.aiohttp.ClientSession.get")
    @patch("fetcher.print")
    async def test_different_num_urls(self, mock_print, mock_get):
        print_args = []
        for num_urls in [1, 10, 25, 100, 1_000]:
            with patch(
                "fetcher.open",
                mock_open(read_data=TestFetcher.get_num_links(num_urls))
            ) as _:
                response = [f"link_{i}" for i in range(num_urls)]
                mock_get.return_value.__aenter__\
                    .return_value.text.side_effect = response
                print_args.clear()
                mock_print.side_effect = \
                    lambda args: print_args.append(str(args))

                fetcher = Fetcher(10, "/dev/null")
                await fetcher.batch_fetch()

                links = TestFetcher.get_num_links(num_urls).split("\n")
                mock_get.assert_has_calls(
                    [call(link) for link in links],
                    any_order=True,
                )
                self.assertEqual([resp + ": {}" for resp in response],
                                 print_args)

    @patch("fetcher.aiohttp.ClientSession.get")
    @patch("fetcher.print")
    async def test_different_num_workers(self, mock_print, mock_get):
        print_args = []
        for num_workers in [1, 10, 25, 100, 1_000]:
            with patch(
                "fetcher.open",
                mock_open(read_data=TestFetcher.get_num_links(10))
            ) as _:
                response = [f"link_{i}" for i in range(10)]
                mock_get.return_value.__aenter__\
                    .return_value.text.side_effect = response
                print_args.clear()
                mock_print.side_effect = \
                    lambda args: print_args.append(str(args))

                fetcher = Fetcher(num_workers, "/dev/null")
                await fetcher.batch_fetch()

                mock_get.assert_has_calls(
                    [call(link)
                     for link in TestFetcher.get_num_links(10).split("\n")],
                    any_order=True,
                )
                self.assertEqual([resp + ": {}" for resp in response],
                                 print_args)

    @patch("fetcher.aiohttp.ClientSession.get")
    @patch("fetcher.print")
    async def test_speed_dependence_number_of_tasks(self, _, mock_get):
        with patch(
            "fetcher.open",
            mock_open(read_data=TestFetcher.get_num_links(100))
        ) as _:

            async def client_session_get_load():
                await asyncio.sleep(0.01)
                return "test content"

            mock_get.return_value.__aenter__.\
                return_value.text.side_effect = \
                client_session_get_load

            time_1_task = time.time()
            fetcher = Fetcher(1, "/dev/null")
            await fetcher.batch_fetch()
            time_1_task = time.time() - time_1_task

            time_10_task = time.time()
            fetcher = Fetcher(10, "/dev/null")
            await fetcher.batch_fetch()
            time_10_task = time.time() - time_10_task

            self.assertGreater(time_1_task, time_10_task)

    @patch("fetcher.aiohttp.ClientSession.get")
    @patch("fetcher.print")
    async def test_fetch_worker(self, mock_print, mock_get):
        mock_get.return_value.__aenter__\
            .return_value.text.return_value = "test"
        print_args = []
        mock_print.side_effect = \
            lambda args: print_args.append(str(args))

        await Fetcher.fetch_worker(iter(["link_0"]))
        mock_get.assert_called_once_with("link_0")
        self.assertEqual(["""link_0: {"test": 1}"""], print_args)

        await Fetcher.fetch_worker(iter(["link_1", "link_2"]))
        mock_get.assert_has_calls(
            [call(link) for link in ["link_0", "link_1", "link_2"]],
            any_order=True
        )
        result = [f"link_{i}" + ': {"test": 1}' for i in range(3)]
        self.assertEqual(result, print_args)

    @patch("fetcher.aiohttp.ClientSession.get")
    @patch("fetcher.print")
    async def test_fetch_url(self, _, mock_get):
        mock_get.return_value.\
            __aenter__.return_value.text.return_value \
            = "test"
        resp = await Fetcher.fetch_url("link_0")
        mock_get.assert_called_once_with("link_0")
        self.assertEqual("""link_0: {"test": 1}""", resp)


if __name__ == "__main__":
    unittest.main()
