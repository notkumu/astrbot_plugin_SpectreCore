from collections import OrderedDict
from typing import Any
class LRUCache:
    def __init__(self, capacity: int = 500):
        self.capacity = capacity
        self._cache = OrderedDict()

    def get(self, key: str) -> Any:
        if key not in self._cache:
            return None
        self._cache.move_to_end(key)
        return self._cache[key]

    def put(self, key: str, value: Any) -> None:
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if len(self._cache) > self.capacity:
            self._cache.popitem(last=False)

    def __contains__(self, key: str) -> bool:
        return key in self._cache

    def __len__(self) -> int:
        return len(self._cache)

# 全局缓存实例
name_cache = LRUCache(200)  # 用户名缓存
message_cache = LRUCache(100)  # 消息缓存