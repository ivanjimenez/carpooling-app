import heapq

class PriorityQueue:
    def __init__(self, maxsize=None):
        self.pq = []
        self.entry_finder = {}
        self.counter = 0
        self.maxsize = maxsize

    def insert(self, task_dict, priority=1):
        if self.maxsize is not None and len(self.pq) >= self.maxsize:
            raise ValueError("La cola de prioridades ha alcanzado su tamaño máximo")
        
        task_id = task_dict['id']
        if task_id in self.entry_finder:
            raise ValueError(f"ID '{task_id}' ya existe en la cola de prioridades")
        
        entry = [priority, self.counter, task_dict]
        self.counter += 1
        self.entry_finder[task_id] = entry
        heapq.heappush(self.pq, entry)

    def remove(self, task_id):
        entry = self.entry_finder.pop(task_id)
        entry[-1] = None

    def pop(self):
        while self.pq:
            priority, count, task_dict = heapq.heappop(self.pq)
            if task_dict is not None:
                task_id = task_dict['id']
                del self.entry_finder[task_id]
                return task_dict
        raise KeyError('pop from an empty priority queue')

    def increase_priority(self):
        if self.pq:
            _, _, task_dict = self.pq[0]
            if task_dict is not None:
                task_id = task_dict['id']
                self.remove(task_id)
                priority = task_dict.get('priority', 1) + 1
                task_dict['priority'] = priority
                self.insert(task_dict, priority)

  
    def print_elements(self):
        for entry in self.pq:
            if entry[-1] is not None:
                priority, _, task_dict = entry
                print(f"Prioridad: {priority}, Grupo: {task_dict}")

    def __len__(self):
        return len(self.entry_finder)
