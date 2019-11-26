from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)

'''

Api() trabaja con resources
Cada recurso debe ser una clase

'''
api = Api(app)

class Student(Resource):
    def get(self, name):
        return { 'student': name }

# Esto es en vez de @app.route('/student/<string:name>')
# Pero ya no tenemos que usar ese decorador en cada función
api.add_resource(Student, '/student/<string:name>')

# Aquí está explícito pero el 5000 es el default
app.run(port=5000)
