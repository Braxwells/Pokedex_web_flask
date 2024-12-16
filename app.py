from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from db import create_user, find_user
from db import leer_pokemon, collection_pokemon, leer_movimientos, leer_items



app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Ruta para mostrar el formulario de login/registro
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        action = request.form['action']

        if action == 'login':
            user = find_user(username)
            if user and check_password_hash(user['password'], password):
                session['user'] = user['username']
                flash('¡Inicio de sesión exitoso!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Usuario o contraseña incorrectos', 'danger')

        elif action == 'register':
            if find_user(username):
                flash('El usuario ya está registrado', 'danger')
            else:
                hashed_password = generate_password_hash(password)
                create_user(username, hashed_password)
                session['user'] = username
                flash('¡Usuario registrado exitosamente!', 'success')
                return redirect(url_for('home'))

    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('¡Cierre de sesión exitoso!', 'info')
    return redirect(url_for('home'))

# Modificar el home para mostrar un saludo si el usuario está logueado
@app.route('/')
def home():
    user = session.get('user')
    return render_template('home.html', user=user)

@app.route('/search')
def search_options():
    return render_template('search.html')



@app.route('/search/pokemon', methods=['GET', 'POST'])
def search_pokemon():
    if request.method == 'POST':
        name = request.form.get('name')
        id = request.form.get('pokedex_number')

        types = [request.form.get('type-electric'), request.form.get('type-normal'), request.form.get('type-fire'),
                 request.form.get('type-water'), request.form.get('type-grass'), request.form.get('type-ice'),
                 request.form.get('type-fighting'), request.form.get('type-poison'), request.form.get('type-ground'),
                 request.form.get('type-flying'), request.form.get('type-psychic'), request.form.get('type-bug'),
                 request.form.get('type-rock'), request.form.get('type-ghost'), request.form.get('type-dragon'),
                 request.form.get('type-dark'), request.form.get('type-steel'), request.form.get('type-fairy')]



        if all(t is None for t in types):
            types = []

        hp = request.form.get('hp')
        attack = request.form.get('attack')
        defense = request.form.get('defense')
        sp_attack = request.form.get('sp_attack')
        sp_defense = request.form.get('sp_defense')
        speed = request.form.get('speed')

        # Llamar a la función de consulta
        results = leer_pokemon(name, id, types, hp, attack, defense, sp_attack, sp_defense, speed)

        return render_template('pokemon.html', name=name, id=id, types=types, hp=hp, attack=attack,
                               defense=defense, sp_attack=sp_attack, sp_defense=sp_defense, speed=speed, results=results)

    elif request.method == 'GET':
        return render_template('pokemon.html')


@app.route('/pokemon/<name>')
def pokemon_detail(name):
    # Busca el Pokémon en la base de datos por su nombre exacto.
    pokemon = collection_pokemon.find_one({"name.english": name})
    if not pokemon:
        return "Pokémon no encontrado", 404

    return render_template("pokemon_details.html", pokemon=pokemon)



@app.route('/search/moves', methods=['GET', 'POST'])
def search_moves():
    if request.method == 'POST':
        # Obtener los filtros del formulario
        name = request.form.get('name')
        tipo = request.form.get('type')
        power = request.form.get('power')
        category = request.form.get('category')
        pp = request.form.get('pp')

        # Llamar a la función de consulta en db.py
        moves = leer_movimientos(name=name, tipo=tipo, power=power, category=category, pp=pp)

        # Renderizar la página con los resultados
        return render_template('moves.html', moves=moves, name=name, tipo=tipo, power=power, category=category, pp=pp)

    elif request.method == 'GET':
        # Renderizar la página sin resultados inicialmente
        return render_template('moves.html', moves=[])



@app.route('/search/items', methods=['GET', 'POST'])
def search_items():
    if request.method == 'POST':
        name = request.form.get('name')
        item_id = request.form.get('item_id')

        # Llamar a la función de búsqueda en la base de datos
        items = leer_items(name, item_id)

        return render_template('item.html', name=name, item_id=item_id, items=items)

    elif request.method == 'GET':
        return render_template('item.html')


if __name__ == '__main__':
    app.run(debug=True)



