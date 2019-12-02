'''
Propósito: tener un objecto tipo usuario

Funciñón: en vez de tener un diccionario, tendremos objetos.
'''
class User:
    # _id porque id es un keyword de python
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
