import collections.abc as ab
from typing import Hashable, Any


class LRUCache(dict):
    def __init__(self, limit: int = 42):
        super().__init__()
        if not isinstance(limit, int) or limit <= 0:
            raise AttributeError("Limit must be positive int")
        self.limit = limit

    def get(self, key: Hashable) -> Any:
        if not isinstance(key, ab.Hashable):
            raise AttributeError("Key must be hashable")
        if key not in self:
            return None
        val = self.pop(key)
        self[key] = val
        return val

    def set(self, key: Hashable, value: Any) -> None:
        if not isinstance(key, ab.Hashable):
            raise AttributeError("Key must be hashable")
        if key in self:
            self.pop(key)
        else:
            if self.limit > 0:
                self.limit -= 1
            else:
                self.pop(next(iter(self)))
        self[key] = value
