class Nodos:
    def __init__(self,data=None):
        self.data = data
        self.siguiente = None

class Lista_nodos:
    def __init__(self):
        self.cabeza = None


    def insertar_final_nodo(self,data):
        nuevo_nodo = Nodos(data)
        if self.cabeza == None:
            self.cabeza = nuevo_nodo
            return
        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente

        actual.siguiente = nuevo_nodo

    def obtener_y_eliminar_primero(self):
        """Obtiene el primer nodo (ticket_actual) y elimina la cabeza de la lista."""
        if self.cabeza is None:
            return None
        ticket_actual = self.cabeza
        self.cabeza = self.cabeza.siguiente  # Mueve la cabeza al siguiente nodo
        return ticket_actual

    def imprimir(self):
        nodos=[]
        actual_nodo = self.cabeza
        while actual_nodo:
            print(actual_nodo.data, end=' --> ')
            nodos.append(actual_nodo.data)
            actual_nodo = actual_nodo.siguiente
        print('none')
        return nodos

    def buscar(self, filtro, valor):
        resultados = []
        actual = self.cabeza
        while actual is not None:
            # Accede a los atributos a través de actual.data
            if (filtro == "nombre" and actual.data.nombre == valor) or \
                    (filtro == "cedula" and actual.data.cedula == valor) or \
                    (filtro == "edad" and actual.data.edad == int(valor)):
                resultados.append(actual.data)
                print("Usuario encontrado:", actual.data.nombre)

            actual = actual.siguiente

        return resultados
