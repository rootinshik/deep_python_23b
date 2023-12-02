import unittest

from lru_cache import LRUCache


class TestLruCache(unittest.TestCase):
    def test_cache_operations(self):
        cache = LRUCache()
        cache.set("key1", "value1")
        self.assertEqual(cache.get("key1"), "value1")
        cache.set("key2", 2)
        self.assertEqual(cache.get("key2"), 2)
        self.assertEqual(cache.get("key3"), None)
        cache.set("key2", 3)
        self.assertEqual(cache.get("key2"), 3)
        self.assertEqual(cache.get("key1"), "value1")
        self.assertEqual(cache.get("key3"), None)

    def test_cache_limit(self):
        cache = LRUCache(2)
        cache.set(1, 1)
        cache.set(2, 2)
        cache.set(3, 3)
        cache.set(3, 4)
        self.assertEqual(cache.get(1), None)
        self.assertEqual(cache.get(2), 2)
        self.assertEqual(cache.get(3), 4)

    def test_cache_priority(self):
        cache = LRUCache(2)
        cache.set(1, 1)
        cache.set(2, 2)
        cache.get(1)
        cache.set(3, 3)
        self.assertEqual(cache.get(1), 1)
        self.assertEqual(cache.get(2), None)
        self.assertEqual(cache.get(3), 3)

    def test_invalid_limit_type(self):
        with self.assertRaises(AttributeError):
            LRUCache("42")
        with self.assertRaises(AttributeError):
            LRUCache(42.0)

    def test_invalid_limit_value(self):
        with self.assertRaises(AttributeError):
            LRUCache(0)
        with self.assertRaises(AttributeError):
            LRUCache(-42)

    def test_invalid_key_type(self):
        cache = LRUCache()
        with self.assertRaises(AttributeError):
            cache.set([], 1)
        with self.assertRaises(AttributeError):
            cache.get([])

    def test_limit_eq_1(self):
        cache = LRUCache(1)
        cache.set(1, 1)
        self.assertEqual(1, cache.get(1))
        cache.set(2, 2)
        self.assertEqual(None, cache.get(1))
        self.assertEqual(2, cache.get(2))
        cache.set(3, 3)
        self.assertEqual(None, cache.get(1))
        self.assertEqual(None, cache.get(2))
        self.assertEqual(3, cache.get(3))

    def test_edit_value_by_key(self):
        cache = LRUCache(limit=2)
        cache.set(1, 1)
        cache.set(2, 2)
        self.assertEqual(1, cache.get(1))
        self.assertEqual(2, cache.get(2))
        cache.set(1, "val1")
        self.assertNotEqual(1, cache.get(1))
        self.assertEqual("val1", cache.get(1))
        cache.set(3, 3)
        self.assertEqual("val1", cache.get(1))
        self.assertEqual(3, cache.get(3))
        self.assertNotEqual(2, cache.get(2))
        self.assertEqual(None, cache.get(2))


if __name__ == "__main__":
    unittest.main()
