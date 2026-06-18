import pytest
import time
from src.cache import LRUCache

def test_lru_eviction():
    cache = LRUCache(capacity=2, ttl=60)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)
    assert cache.get("a") is None
    assert cache.get("b") == 2
    assert cache.get("c") == 3

def test_ttl_expiration():
    cache = LRUCache(capacity=10, ttl=1)
    cache.set("x", 100)
    time.sleep(1.1)
    assert cache.get("x") is None
