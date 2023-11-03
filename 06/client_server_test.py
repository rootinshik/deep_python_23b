import unittest
import threading
import time
from unittest.mock import patch, mock_open, MagicMock

from server import Server
from client import Client


class ServerTests(unittest.TestCase):
    @patch("server.socket")
    @patch("server.print")
    def test_base_functionality(self, _, __):
        server = Server(10, 10)
        server_thread = threading.Thread(target=server.start, daemon=True)
        server_thread.start()
        self.assertEqual(server_thread.is_alive(), True)
        server.stop()
        time.sleep(2)
        self.assertEqual(server_thread.is_alive(), False)


class ClientTests(unittest.TestCase):
    @patch("client.socket")
    @patch("client.print")
    def test_base_functionality(self, _, __):
        client = Client(10, "/dev/null")
        client_thread = threading.Thread(target=client.start, daemon=True)
        client_thread.start()
        self.assertEqual(client_thread.is_alive(), True)
        time.sleep(1)
        self.assertEqual(client_thread.is_alive(), False)


class ClientServerInteractionTests(unittest.TestCase):
    URLS = "https://en.wikipedia.org/wiki/History_of_Python\n" \
           "https://en.wikipedia.org/wiki/Centrum_Wiskunde_%26_Informatica\n" \
           "https://en.wikipedia.org/wiki/Netherlands\n" \
           "https://en.wikipedia.org/wiki/SETL\n" \
           "https://en.wikipedia.org/wiki/Exception_handling"

    @patch("client.open", mock_open(read_data=URLS))
    @patch("server.urlopen")
    @patch("server.print")
    @patch("client.print")
    def test_num_processed_urls(self, _, server_print_mock, urlopen_mock):
        # https://stackoverflow.com/questions/32043035/python-3-urlopen-context-manager-mocking
        mock = MagicMock()
        mock.getcode.return_value = 200
        mock.read.return_value = 'a a b'.encode()
        mock.__enter__.return_value = mock
        urlopen_mock.return_value = mock

        server_print_args = []
        server_print_mock.side_effect = \
            lambda args: server_print_args.append(str(args))

        server = Server(5, 5)
        client = Client(5, "/dev/null")
        server_thread = threading.Thread(target=server.start)
        client_thread = threading.Thread(target=client.start)
        server_thread.start()
        time.sleep(0.1)
        client_thread.start()
        client_thread.join()
        server.stop()

        server_thread.join()
        num_processed_urls = server_print_args[-1]
        self.assertEqual("Number of processed URLs: 5",
                         num_processed_urls)

    @patch("client.open", mock_open(read_data=URLS))
    @patch("server.urlopen")
    @patch("server.print")
    @patch("client.print")
    def test_server_response(self, client_print_mock, _, urlopen_mock):
        # https://stackoverflow.com/questions/32043035/python-3-urlopen-context-manager-mocking
        mock = MagicMock()
        mock.getcode.return_value = 200
        mock.read.return_value = 'a a b'.encode()
        mock.__enter__.return_value = mock
        urlopen_mock.return_value = mock

        client_print_args = []
        client_print_mock.side_effect = \
            lambda args: client_print_args.append(str(args))

        server = Server(5, 5)
        client = Client(5, "/dev/null")
        server_thread = threading.Thread(target=server.start)
        client_thread = threading.Thread(target=client.start)
        server_thread.start()
        time.sleep(0.1)
        client_thread.start()
        client_thread.join()
        server.stop()

        server_thread.join()
        expected = [
            'https://en.wikipedia.org/wiki/Centrum_Wiskunde_%26_Informatica: '
            '{"a": 2, "b": 1}',
            'https://en.wikipedia.org/wiki/History_of_Python: '
            '{"a": 2, "b": 1}',
            'https://en.wikipedia.org/wiki/Netherlands: '
            '{"a": 2, "b": 1}',
            'https://en.wikipedia.org/wiki/SETL: '
            '{"a": 2, "b": 1}',
            'https://en.wikipedia.org/wiki/Exception_handling: '
            '{"a": 2, "b": 1}'
        ]
        self.assertEqual(sorted(expected), sorted(client_print_args))

    @patch("server.urlopen")
    @patch("server.print")
    @patch("client.print")
    def test_depends_server_num_threads_on_speed(self, _, __, urlopen_mock):
        time_1_thread = time.time()
        # https://stackoverflow.com/questions/32043035/python-3-urlopen-context-manager-mocking
        mock = MagicMock()
        mock.getcode.return_value = 200
        mock.read.return_value = 'a a b'.encode()
        mock.__enter__.return_value = mock
        urlopen_mock.return_value = mock
        server = Server(1, 5)
        client = Client(1, "URLS.txt")
        server_thread = threading.Thread(target=server.start)
        client_thread = threading.Thread(target=client.start)
        server_thread.start()
        time.sleep(0.1)
        client_thread.start()
        client_thread.join()
        server.stop()
        server_thread.join()
        time_1_thread = time.time() - time_1_thread

        time.sleep(1)

        time_10_thread = time.time()
        server = Server(10, 5)
        client = Client(1, "URLS.txt")
        server_thread = threading.Thread(target=server.start)
        client_thread = threading.Thread(target=client.start)
        server_thread.start()
        time.sleep(0.1)
        client_thread.start()
        client_thread.join()
        server.stop()
        server_thread.join()
        time_10_thread = time.time() - time_10_thread

        self.assertGreater(time_1_thread, time_10_thread)

    @patch("server.urlopen")
    @patch("server.print")
    @patch("client.print")
    def test_depends_client_num_threads_on_speed(self, _, __, urlopen_mock):
        time_1_thread = time.time()
        # https://stackoverflow.com/questions/32043035/python-3-urlopen-context-manager-mocking
        mock = MagicMock()
        mock.getcode.return_value = 200
        mock.read.return_value = 'a a b c V K'.encode()
        mock.__enter__.return_value = mock
        urlopen_mock.return_value = mock
        server = Server(1, 5)
        client = Client(1, "URLS.txt")
        server_thread = threading.Thread(target=server.start)
        client_thread = threading.Thread(target=client.start)
        server_thread.start()
        time.sleep(0.1)
        client_thread.start()
        client_thread.join()
        server.stop()
        server_thread.join()
        time_1_thread = time.time() - time_1_thread

        time.sleep(1)

        time_10_thread = time.time()
        server = Server(1, 5)
        client = Client(10, "URLS.txt")
        server_thread = threading.Thread(target=server.start)
        client_thread = threading.Thread(target=client.start)
        server_thread.start()
        time.sleep(0.1)
        client_thread.start()
        client_thread.join()
        server.stop()
        server_thread.join()
        time_10_thread = time.time() - time_10_thread

        self.assertGreater(time_1_thread, time_10_thread)


if __name__ == "__main__":
    unittest.main()
