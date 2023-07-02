class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.order = []

    def get(self, key):
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        else:
            return None

    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.order) >= self.capacity:
            expired_key = self.order.pop(0)
            del self.cache[expired_key]
        self.cache[key] = value
        self.order.append(key)
    
    def cache_info(self):
        hits = sum(1 for key in self.order if key in self.cache)
        misses = len(self.order) - hits
        return hits, misses
