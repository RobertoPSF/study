class Node:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:

    def __init__(self, size):
        self.size = size
        self.cache = {}

        self.head = Node(0, 0)
        self.tail = Node(0, 0)

        self.head.next = self.tail
        self.tail.prev = self.head

    
    def _remove(self, node):
        prev_node = node.prev
        next_node = node.next

        prev_node.next = next_node
        next_node.prev = prev_node
    

    def _insert_at_front(self, node):
        node.next = self.head.next
        node.prev = self.head

        self.head.next.prev = node
        self.head.next = node

    
    def get(self, key):
        if key not in self.cache:
            return -1
        
        node = self.cache[key]

        self._remove(node)
        self._insert_at_front(node)

        return node.value


    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.value = value

            self._remove(node)
            self._insert_at_front(node)
        else:
            if len(self.cache) == self.size:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]

            new_node = Node(key, value)
            self.cache[key] = new_node
            self._insert_at_front(new_node)



cache = LRUCache(2)

cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))  # 1

cache.put(3, 3)      # remove key 2
print(cache.get(2))  # -1

cache.put(4, 4)      # remove key 1
print(cache.get(1))  # -1
print(cache.get(3))  # 3
print(cache.get(4))  # 4