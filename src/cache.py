import time
import threading
from collections import OrderedDict
from typing import Any, Optional

class LRUCache:
    def __init__(self, capacity: int = 1000, ttl: int = 3600):
        self.capacity = capacity
        self.ttl = ttl
        self.cache = OrderedDict()
        self.lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                return None
            item = self.cache[key]
            if time.time() > item['expire_at']:
                del self.cache[key]
                return None
            self.cache.move_to_end(key)
            return item['value']

    def set(self, key: str, value: Any) -> None:
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = {
                'value': value,
                'expire_at': time.time() + self.ttl
            }
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)
