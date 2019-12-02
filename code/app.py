# from flask import jsonify # flask_restful se encarga de mandarlo a json
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
'''
La llave sectreta puede ser el texto que queramos,
generalmente es largo para hacerlo más complicado.
'''
app.secret_key = 'lo_que_sea'
'''

Api() trabaja con resources
Cada recurso debe ser una clase

'''
api = Api(app)

# JWT crea un nuevo endpoint --> /auth
jwt = JWT(app, authenticate, identity)

items = []

class ItemList(Resource):
    @jwt_required()
    def get(self):
        return items

class Item(Resource):
    '''
    Se sacó parser de los métodos
    Ahora pertenece a la clase como tal
    Y se debe llamar distinto dentro de los métodos
    '''
    # Inicializar un objeto para parsear el request
    # El parser analiza los json payloads
    # y los form payloads de HTML, iterar los campos
    parser = reqparse.RequestParser()

    # Los argumentos que se incluyen son los que se toman en cuenta
    # cualquier otro argumento es excluido/borrado/simplemente no pasa
    parser.add_argument('price', required=True, type=float, help='Este campo no puede estar vacío')

    @jwt_required()
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item, 200
        # Otro approach:
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return item

        # Para hacer un JSON retornable válido general
        # (postman, angular, react, etc, etc...)
        # Además, el estatus regresado es un 200. Lo cambiamos a 404
        return { 'name': None }, 404

    @jwt_required()
    def post(self, name):
        # Porque se le agregó el 404 se regresa esto:
        # ({'name': None}, 404) ... el if hace cosas raras
        nombre = self.get(name)
        if nombre[1] != 404:
            return f'Ya existe {nombre[0]}', 400

        # data = request.get_json()
        data = Item.parser.parse_args()

        item = { 'name': name, 'price': data['price'] }
        items.append(item)
        # return jsonify(item) # Ya no tenemos que hacer esto
        # flask_restful lo hace por nosotros
        return item, 201 # 201 significa 'creado'

    @jwt_required()
    def delete(self, name):
        # para evitar que python cree una variable local también llamada items
        global items

        nombre = self.get(name)
        if nombre[1] != 404:
            items = list(filter(lambda x:x['name'] != name, items))
            return f'{nombre[0]} fue borrado exitosamente', 200
        else:
            return f'{nombre[0]} no se encontró o ya fue borrado', 400

    @jwt_required()
    def put(self, name):
        # original
        # data = request.get_json()
        # con parser
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = { 'name': name, 'price': data['price'] }
            items.append(item)
            return item, 201
        else:
            item.update(data)

        return item

# Esto es en vez de @app.route('/student/<string:name>')
# Pero ya no tenemos que usar ese decorador en cada función
api.add_resource(Item, '/item/<string:name>')

api.add_resource(ItemList, '/items')

# Aquí está explícito pero el 5000 es el default

# debug=True crea un HTML con los errores
app.run(port=5000, debug=True)
