import threading
import socket
import sys
from queue import Queue


HOST = "127.0.0.1"
PORT = 65410


class Client:
    def __init__(self, num_workers: int, file_name: str):
        self.num_workers = num_workers
        self.file_name = file_name
        self.urls_queue = Queue(maxsize=self.num_workers)
        self.file_worker = FileWorker(self.file_name, self.urls_queue)
        self.url_workers = [URLWorker(self.urls_queue)
                            for _ in range(self.num_workers)]

    def start(self):
        self.file_worker.start()
        for url_worker in self.url_workers:
            url_worker.start()
        self.file_worker.join()
        for url_worker in self.url_workers:
            url_worker.join()


class FileWorker(threading.Thread):
    def __init__(self, file_name: str, urls_queue: Queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_name = file_name
        self.urls_queue = urls_queue

    def run(self):
        with open(self.file_name, encoding="utf-8") as file:
            for line in file:
                self.urls_queue.put(line.strip())
        self.urls_queue.put(None)


class URLWorker(threading.Thread):
    def __init__(self, urls_queue: Queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.urls_queue = urls_queue

    def run(self):
        while True:
            url = self.urls_queue.get()

            if url is None:
                self.urls_queue.put(None)
                break

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                try:
                    server.connect((HOST, PORT))
                    server.sendall(url.encode())
                    data = server.recv(1024).decode()
                    print(f"{url}: {data}")
                except ConnectionRefusedError:
                    continue


def parse_args():
    if len(sys.argv) != 3:
        print("Usage: python client.py <num_workers> <file_name>")
        sys.exit(1)
    return int(sys.argv[1]), sys.argv[2]


if __name__ == "__main__":
    Client(*parse_args()).start()
