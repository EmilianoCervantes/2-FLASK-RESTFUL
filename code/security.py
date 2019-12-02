from user import User

'''
Propósito: englobar funciones importantes
FUNCIONES:
- Mantener listado de nuestros usuarios
'''
users = [
    User(1, 'emiliano', '12345')
]

'''
Primera versión de los mappings
username_mapping = {
    'emiliano': {
        'id': 1,
        'username': 'emiliano',
        'password': '12345'
    }
}

userid_mapping = {
    1: {
        'id': 1,
        'username': 'emiliano',
        'password': '12345'
    }
}
'''

'''2DA versión de los mapping'''
username_mapping = { u.username: u for u in users }

userid_mapping = { u.id: u for u in users }

# Se llama automáticamente a través de JWT(..., authenticate, ...)
# cuando se manda unan credenciales al endpoint /auth

def authenticate(username, password):
    # Agregamos un valor por default
    # Si no se encuentra el nombre, regresamos como default None
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user

    return None

# Payload es el contenido del token jwt
# Se llama automáticamente gracias a JWT(..., identity)
def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
