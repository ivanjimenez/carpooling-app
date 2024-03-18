from collections import deque

class ListaCircular:
    def __init__(self):
        self.lista = deque()

    def agregar_elemento(self, elemento):
        self.lista.append(elemento)

    def siguiente_elemento(self):
        if self.lista:
            elemento = self.lista.popleft()
            self.lista.append(elemento)
            return elemento
        else:
            return None

    def buscar_por_id(self, target_id):
        for elemento in self.lista:
            if elemento.get("id") == target_id:
                return elemento
        return None