from collections import deque

class CircularQueue:
    def __init__(self):
        self.list = deque()

    def add_item(self, item):
        self.list.append(item)

    def next_item(self):
        if self.list:
            item = self.list.popleft()
            self.list.append(item)
            return item
        else:
            return None

    def search_by_id(self, target_id):
        for item in self.list:
            if item.get("id") == target_id:
                return item
        return None
    
    def reset(self):
        """
        Método para reiniciar la lista a 0.
        """
        self.list.clear()