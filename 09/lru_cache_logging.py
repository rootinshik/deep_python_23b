import sys
import logging
import argparse
import collections.abc as ab
from typing import Hashable, Any


class LRUCache(dict):
    def __init__(self, log_name: str, limit: int = 42):
        super().__init__()

        self.logger = logging.getLogger(log_name)
        if not isinstance(limit, int) or limit <= 0:
            self.logger.critical("LRUCache limit is not positive int, "
                                 "type: %s, "
                                 "value: %s", type(limit), limit)
            raise AttributeError("Limit must be positive int")
        self.max_limit = limit
        self.limit = limit

    def get(self, key: Hashable) -> Any:
        if not isinstance(key, ab.Hashable):
            self.logger.critical("Key is not hashable, "
                                 "type: %s", type(key))
            raise AttributeError("Key must be hashable")
        if key not in self:
            self.logger.info("Key not in LRUCache, "
                             "value: %s", key)
            return None
        val = self.pop(key)
        self[key] = val
        self.logger.debug("Get key: %s "
                          "with value: %s", key, val)
        return val

    def set(self, key: Hashable, value: Any) -> None:
        if not isinstance(key, ab.Hashable):
            self.logger.critical("Key is not hashable, "
                                 "type: %s", type(key))
            raise AttributeError("Key must be hashable")
        if key in self:
            self.logger.info("Key was already in LRUCache, "
                             "value: %s", value)
            self.pop(key)
        else:
            if self.limit > 0:
                self.limit -= 1
                self.logger.debug("Limit reached %s, "
                                  "max limit: %s", self.limit, self.max_limit)
            else:
                self.logger.debug("Max limit reached: %s", self.max_limit)
                pop_key = next(iter(self))
                pop_val = self.pop(pop_key)
                self.logger.debug("Remove key: %s, "
                                  "value: %s", pop_key, pop_val)
        self[key] = value
        self.logger.debug("Key set key: %s, value: %s", key, value)


def custom_filter(record) -> bool:
    return len(record.getMessage().split()) % 2 != 0


def arg_parse() -> (bool, bool):
    parser = argparse.ArgumentParser(description='LRU Cache with logging')
    parser.add_argument('-s',
                        action='store_true',
                        help='Enable logging to stdout with custom formatting')
    parser.add_argument('-f',
                        action='store_true',
                        help='Apply custom filter')
    args = parser.parse_args()
    return args.s, args.f


def set_up_logger(in_stdout: bool, add_filter: bool) -> str:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("cache.log", mode="w")
    file_handler.setLevel(logging.INFO)

    file_formatter = logging.Formatter('%(asctime)s - '
                                       '%(levelname)s - '
                                       '%(message)s')
    file_handler.setFormatter(file_formatter)

    logger.addHandler(file_handler)

    if in_stdout:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.WARNING)

        stdout_formatter = logging.Formatter('%(levelname)s - '
                                             '%(message)s')
        stdout_handler.setFormatter(stdout_formatter)

        logger.addHandler(stdout_handler)

    if add_filter:
        logger.addFilter(custom_filter)

    return __name__


if __name__ == "__main__":
    LOGGER_NAME = set_up_logger(*arg_parse())

    cache = LRUCache(limit=2,
                     log_name=LOGGER_NAME)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    cache.get("k3")
    cache.get("k2")
    cache.get("k1")

    cache.set("k3", "val3")

    cache.get("k3")
    cache.get("k2")
    cache.get("k1")

    cache.get("k4")

    try:
        cache.get([])
    except AttributeError:
        ...
    try:
        cache.set({}, 1)
    except AttributeError:
        ...
