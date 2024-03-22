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
    
    def get_group_ids(priority_queue):
        group_ids = []
        # Iterar sobre todos los elementos en la cola prioritaria
        for _, _, group in priority_queue._elements:
            # Extraer el ID del grupo y agregarlo a la lista
            group_ids.append(group.id)
        return group_ids
    
    def remove_group_by_id(self, id):
        """
        Remove an element from the priority queue based on the ID in the dictionary.
        """
        self._elements = [element for element in self._elements if element[-1]['id'] != id]
