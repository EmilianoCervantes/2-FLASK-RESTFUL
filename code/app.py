# from flask import jsonify # flask_restful se encarga de mandarlo a json
from flask import Flask, request
from flask_restful import Resource, Api
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

    def post(self, name):
        # Porque se le agregó el 404 se regresa esto:
        # ({'name': None}, 404) ... el if hace cosas raras
        nombre = self.get(name)
        if nombre[1] != 404:
            return f'Ya existe {nombre}', 400

        data = request.get_json()

        item = { 'name': name, 'price': data['precio'] }
        items.append(item)
        # return jsonify(item) # Ya no tenemos que hacer esto
        # flask_restful lo hace por nosotros
        return item, 201 # 201 significa 'creado'

# Esto es en vez de @app.route('/student/<string:name>')
# Pero ya no tenemos que usar ese decorador en cada función
api.add_resource(Item, '/item/<string:name>')

api.add_resource(ItemList, '/items')

# Aquí está explícito pero el 5000 es el default

# debug=True crea un HTML con los errores
app.run(port=5000, debug=True)
