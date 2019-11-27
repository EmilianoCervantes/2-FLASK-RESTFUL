# from flask import jsonify # flask_restful se encarga de mandarlo a json
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)

'''

Api() trabaja con resources
Cada recurso debe ser una clase

'''
api = Api(app)

items = []

class ItemList(Resource):
    def get(self):
        return items

class Item(Resource):
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
        data = request.get_json()

        nombre = self.get(name)

        # Porque se le agregó el 404 se regresa esto:
        # ({'name': None}, 404) ... el if hace cosas raras
        if nombre[1] != 404:
            return 'Ya existe'

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
