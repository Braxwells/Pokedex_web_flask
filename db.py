# database.py
import sys
import pymongo
import ssl

try:
    client = pymongo.MongoClient("mongodb+srv://brunoesr999:Brunosr284844@cluster0.o5oxu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

except pymongo.errors.ConfigurationError:

    sys.exit(1)

# use a database named "pokedex"
db = client.pokedex
collection_pokemon = db["pokemon"]
collection_items = db["items"]
collection_moves = db["movimientos"]
collection_types = db["tipos"]
collection_users = db["usuarios"]




def leer_pokemon(name=None, id=None, types=None, hp=None, attack=None, defense=None, sp_attack=None, sp_defense=None, speed=None):
    # Construir la consulta
    consulta = {}

    if name:
        consulta["name.english"] = {"$regex": name, "$options": "i"}  # Búsqueda parcial, sin distinción de mayúsculas
    if id:
        consulta["id"] = int(id)
    if len(types) != 0:
        consulta["type"] = {"$all": [t for t in types if t]}  # Solo tipos seleccionados
    if hp:
        consulta["base.HP"] = {"$gte": int(hp)}
    if attack:
        consulta["base.Attack"] = {"$gte": int(attack)}
    if defense:
        consulta["base.Defense"] = {"$gte": int(defense)}
    if sp_attack:
        consulta["base.Sp. Attack"] = {"$gte": int(sp_attack)}
    if sp_defense:
        consulta["base.Sp. Defense"] = {"$gte": int(sp_defense)}
    if speed:
        consulta["base.Speed"] = {"$gte": int(speed)}

    # Ejecutar la consulta y devolver resultados
    return [res for res in collection_pokemon.find(consulta)]


def get_pokemon_by_name(nombre):
    # Aquí se busca por el nombre exacto, ya que el enlace es generado con el nombre completo.
    pokemon = collection_pokemon.find_one({"name.english": {"$regex": f"^{nombre}$", "$options": "i"}})

    return pokemon


def leer_movimientos(name=None, tipo=None, power=None, category=None, pp=None):
    # Construir la consulta
    consulta = {}

    if name:
        consulta["ename"] = {"$regex": name, "$options": "i"}  # Usar 'ename' para el nombre
    if tipo:
        consulta["type"] = tipo  # Solo un tipo
    if power:
        consulta["power"] = {"$gte": int(power)}
    if category:
        consulta["category"] = category  # Usar los valores '物理', '特殊', '变化'
    if pp:
        consulta["pp"] = {"$gte": int(pp)}

    # Ejecutar la consulta y devolver los resultados
    return list(collection_moves.find(consulta))

def leer_items(name=None, item_id=None):
    consulta = {}

    if name:
        consulta["name.english"] = { "$regex": name, "$options": "i"}
    if item_id:
        consulta["id"] = int(item_id)

    return list(collection_items.find(consulta))

def find_user(username):
    """Busca un usuario en la base de datos por nombre de usuario."""
    return collection_users.find_one({"username": username})

def create_user(username, password):
    """Crea un nuevo usuario en la base de datos."""
    collection_users.insert_one({"username": username, "password": password})
