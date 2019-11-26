# Flask-restufl
Una extensión de Flask que se apega al estándar REST.

## Sección 4 del Curso de REST APIs with Flask and Python
https://www.udemy.com/course/rest-api-flask-and-python/learn/lecture/5960142


### A veces lo que queremos no es actualizar
Ej: API de la sección 3 usa flask v.1.0.3

#### Para ello, garantizar que nuestros proys no compartan librerías
Usar ambientes virtuales para la reinstalación de Python sin librerías

\> pip3 install virtualenv

\> virtualenv venv --python=pythonX.x

Ejemplo:

\> virtualenv venv --python=python3.7

##### Crea un folder 'venv' donde se instala python

\> source venv/bin/activate --\> Esto nos manda al virtual environment

\> deactivate --\> para salir

## Instalaciones
1. pip install Flask-RESTful --\> 0.3.7
  - flask 1.1.1 se instaló en conjunto

# Comandos terminal:
1. pip3 freeze --\> listado de librerías de python instaladas
