import queue
import threading
import argparse
import socket
import json
from string import ascii_lowercase
from queue import Queue
from collections import Counter
from urllib.request import urlopen

from bs4 import BeautifulSoup


HOST = "127.0.0.1"
PORT = 65410


class Server:
    def __init__(self, num_workers: int, k_freq_words: int):
        self.num_workers = num_workers
        self.k_freq_words = k_freq_words
        self.num_processed_urls = 0
        self.clients_queue = Queue()
        self.workers = [
            Worker(self.clients_queue, self.k_freq_words, self)
            for _ in range(self.num_workers)
        ]
        self.master = Master(self.clients_queue, self)
        self.working = False

    def start(self) -> None:
        print(
            f"Starting server with {self.num_workers} "
            f"workers and {self.k_freq_words} top frequency words."
        )

        self.working = True

        for worker in self.workers:
            worker.start()
        self.master.start()

        self.master.join()
        for worker in self.workers:
            worker.join()

    def stop(self) -> None:
        self.working = False

    def __repr__(self):
        return f"Number of processed URLs: {self.num_processed_urls}"


class Master(threading.Thread):
    def __init__(self, clients_queue: Queue, server: Server, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients_queue = clients_queue
        self.server = server
        self.socket.settimeout(1)

    def run(self):
        self.socket.bind((HOST, PORT))
        self.socket.listen()
        while self.server.working:
            try:
                client_socket, _ = self.socket.accept()
            except socket.timeout:
                continue
            self.clients_queue.put(client_socket)
        self.socket.close()


class Worker(threading.Thread):
    def __init__(
        self, clients_queue: Queue, top_k: int, server: Server, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.clients_queue = clients_queue
        self.top_k = top_k
        self.server = server
        self.lock = threading.Lock()
        self.num_urls = 0

    def run(self):
        while self.server.working:
            try:
                client = self.clients_queue.get(timeout=1)
            except queue.Empty:
                continue

            url = client.recv(1024).decode()

            client.sendall(self.parse_data(url, self.top_k).encode())
            client.close()

            self.num_urls += 1
            with self.lock:
                self.server.num_processed_urls += 1

            print(self.server)

    @staticmethod
    def get_data(url: str) -> str:
        with urlopen(url) as response:
            return response.read().decode()

    @staticmethod
    def parse_data(url: str, top_k: int) -> str:
        data = (
            BeautifulSoup(Worker.get_data(url), "html.parser")
            .get_text()
            .lower()
            .split()
        )
        words = filter(
            lambda word: all(symb in ascii_lowercase for symb in word),
            data
        )
        word_count = dict(Counter(words).most_common(top_k))
        return json.dumps(word_count, ensure_ascii=False)


def parse_args():
    parser = argparse.ArgumentParser("Server part")
    parser.add_argument(
        "-w",
        "--num_workers",
        type=int,
        dest="w",
        required=True,
        help="provide number of workers",
    )
    parser.add_argument(
        "-k",
        "--top_k_words",
        type=int,
        dest="k",
        required=True,
        help="provide top k frequency words",
    )
    args = parser.parse_args()
    return args.w, args.k


if __name__ == "__main__":
    Server(*parse_args()).start()
