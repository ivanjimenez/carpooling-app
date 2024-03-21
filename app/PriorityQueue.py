# queues.py

from collections import deque
from heapq import heappop, heappush
from itertools import count

# ...

class PriorityQueue:
    def __init__(self):
        self._elements = []
        self._counter = count()

    def enqueue_with_priority(self, priority, value):
        element = (-priority, next(self._counter), value)
        heappush(self._elements, element)

    def dequeue(self):
        return heappop(self._elements)[-1]

    def is_empty(self):
        """
        Método para verificar si la cola prioritaria está vacía.
        Devuelve True si la cola está vacía, False en caso contrario.
        """
        return len(self._elements) == 0