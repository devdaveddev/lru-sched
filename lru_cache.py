class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRU:
    def __init__(self, cap):
        if cap <= 0:
            raise ValueError("error in capacity")
        self.cap = cap

        self.nodes = {}

        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        node = self.nodes.get(key)
        if node is None:
            return -1

        self._bump(node)
        return node.value

    def put(self, key, value):
        node = self.nodes.get(key)
        if node is not None:
            node.value = value
            self._bump(node)
            return

        if len(self.nodes) >= self.cap:
            self._evict()

        node = Node(key, value)
        self.nodes[key] = node
        self._push(node)

    def _push(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _bump(self, node):
        self._remove(node)
        self._push(node)

    def _evict(self):
        lru = self.tail.prev
        self._remove(lru)
        del self.nodes[lru.key]


if __name__ == "__main__":
    cache = LRU(2)
    cache.put(1, 10)
    cache.put(2, 20)
    assert cache.get(1) == 10
    cache.put(3, 30)
    assert cache.get(2) == -1

    cache.put(1, 11)
    cache.put(4, 40)
    assert cache.get(3) == -1
    assert cache.get(1) == 11
    assert cache.get(4) == 40

    small = LRU(1)
    small.put(1, 1)
    small.put(2, 2)
    assert small.get(1) == -1
    assert small.get(2) == 2

    for bad in (0, -3):
        try:
            LRU(bad)
            assert False, "should have raised ValueError"
        except ValueError:
            pass

    print("LRU, checks passed")
