from flask import Flask, request
from flask_mysqldb import MySQL
from flask_restful import Resource, Api, reqparse
import json
from flask import jsonify
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
api = Api(app)
mysql = MySQL(app)

# Время действия токена
TOKEN_EXPIRATION_TIME = timedelta(minutes=30)

tokens = {}

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'lisa'
app.config['MYSQL_PASSWORD'] = '7777'
app.config['MYSQL_DB'] = 'art'

# Функция для генерации токена
def generate_token():
    return secrets.token_hex(16) 


class Country(Resource):
    def put(self, country_id):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='Name of the country', required=True)
            args = parser.parse_args()
            name = args['name']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE countries SET name=%s WHERE id=%s", (name, country_id))
            mysql.connection.commit()
            cur.close()
            return f"Updated country with id {country_id} to '{name}'"
        except Exception as e:
            return f"An error occurred: {str(e)}"

api.add_resource(Country, '/update_country/<int:country_id>')


@app.route('/')
def display_countries_table():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM countries")
        results = cur.fetchall()
        cur.close()

        html = '<h1>Таблица Countries</h1>'
        html += '<table>'
        html += '<tr><th>Id</th><th>Name</th></tr>'
        for result in results:
            html += f'<tr><td>{result[0]}</td><td>{result[1]}</td></tr>'
        html += '</table>'

        return html
    except Exception as e:
        return f"An error occurred: {str(e)}"
    finally:
        if 'cur' in locals():
            cur.close()

@app.route('/artists')
def get_artists():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT artists.name, artists.age, countries.name FROM artists JOIN countries ON artists.country = countries.id")
        results = cur.fetchall()
        cur.close()

        artists = []
        for result in results:
            artist = {
                'name': result[0],
                'age': result[1],
                'country': result[2]
            }
            artists.append(artist)

        # Преобразуем кириллические символы в Unicode Escape-последовательности
        json_data = json.dumps({"artists": artists}, ensure_ascii=False)
        return json_data
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})
    finally:
        if 'cur' in locals():
            cur.close()

@app.route('/country_artists')
def get_country_artists():
    try:
        cur = mysql.connection.cursor()
        # Получаем список стран и их ID
        cur.execute("SELECT * FROM countries")
        countries = cur.fetchall()

        country_artists = {}
        # Для каждой страны получаем артистов, связанных с этой страной
        for country in countries:
            country_id = country[0]
            country_name = country[1]
            cur.execute("SELECT name, age FROM artists WHERE country = %s", (country_id,))
            artists = cur.fetchall()

            artist_list = []
            for artist in artists:
                artist_list.append({
                    'name': artist[0],
                    'age': artist[1]
                })

            country_artists[country_name] = artist_list

        # Преобразуем результат в JSON
        json_data = json.dumps(country_artists, ensure_ascii=False)
        return json_data
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})
    finally:
        if 'cur' in locals():
            cur.close()

@app.route('/users')
def display_users_table():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT users.id, users.username, users.password, museums.name AS museum_name, museums.location FROM users LEFT JOIN museums ON users.museum_id = museums.id")
        users = cur.fetchall()
        cur.close()

        html = '<h1>Таблица Users</h1>'
        html += '<table>'
        html += '<tr><th>ID</th><th>Username</th><th>Password</th><th>Museum Name</th><th>Museum Location</th></tr>'
        for user in users:
            html += f'<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td><td>{user[3]}</td><td>{user[4]}</td></tr>'
        html += '</table>'

        return html
    except Exception as e:
        return f"An error occurred: {str(e)}"
    finally:
        if 'cur' in locals():
            cur.close()


@app.route('/museums')
def display_museums():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM museums")
        museums = cur.fetchall()
        cur.close()

        html = '<h1>Список музеев</h1>'
        html += '<table>'
        html += '<tr><th>ID</th><th>Name</th><th>Location</th></tr>'
        for museum in museums:
            html += f'<tr><td>{museum[0]}</td><td>{museum[1]}</td><td>{museum[2]}</td></tr>'
        html += '</table>'

        return html
    except Exception as e:
        return f"An error occurred: {str(e)}"
    finally:
        if 'cur' in locals():
            cur.close()

@app.route('/museums_users')
def display_museums_users():
    try:
        cur = mysql.connection.cursor()

        # Получаем информацию о музеях
        cur.execute("SELECT * FROM museums")
        museums = cur.fetchall()

        # Для каждого музея получаем связанных с ним пользователей
        museums_users = []
        for museum in museums:
            museum_id = museum[0]
            museum_name = museum[1]
            museum_location = museum[2]

            # Получаем пользователей, связанных с текущим музеем
            cur.execute("SELECT * FROM users WHERE museum_id = %s", (museum_id,))
            users = cur.fetchall()

            users_info = []
            for user in users:
                users_info.append({
                    'id': user[0],
                    'username': user[1],
                    'password': user[2]
                })

            museums_users.append({
                'museum_id': museum_id,
                'museum_name': museum_name,
                'museum_location': museum_location,
                'users': users_info
            })

        cur.close()

        # Форматируем результат в HTML для отображения
        html = '<h1>Список музеев и пользователей</h1>'
        for museum_user in museums_users:
            html += f'<h2>{museum_user["museum_name"]} ({museum_user["museum_location"]})</h2>'
            html += '<ul>'
            for user in museum_user["users"]:
                html += f'<li>Username: {user["username"]}, Password: {user["password"]}</li>'
            html += '</ul>'

        return html
    except Exception as e:
        return f"An error occurred: {str(e)}"
    finally:
        if 'cur' in locals():
            cur.close()


@app.route('/add_country', methods=['POST'])
def add_country():
    try:
        name = request.form['name']
        if not name:
            return "Name cannot be empty"
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM countries WHERE name = %s", (name,))
        existing_country = cur.fetchone()
        if existing_country:
            return f"Country 'name' already exists in DATABASE"
        else:
            cur.execute("INSERT INTO countries (name) VALUES (%s)", (name,))
            mysql.connection.commit()
            cur.close()
            return f"Added country: {name}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
    finally:
        if 'cur' in locals():
            cur.close()

@app.route('/update_country/<int:country_id>', methods=['PUT'])
def update_country(country_id):
    try:
        data = json.loads(request.data.decode("utf-8"))  # декодируем полученные данные в формате UTF-8
        name = data['name']  # извлекаем имя страны из декодированных данных
        if not name:
            return "Name cannot be empty"
        cur = mysql.connection.cursor()
        cur.execute("UPDATE countries SET name=%s WHERE id=%s", (name, country_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": f"Updated country with id {country_id} to '{name}'"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})
    finally:
        if 'cur' in locals():
            cur.close()
@app.route('/delete_country/<int:country_id>', methods=['DELETE'])
def delete_country(country_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM countries WHERE id=%s", (country_id,))
        mysql.connection.commit()
        return jsonify({"message": f"Deleted country with id {country_id}"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})
    finally:
        if 'cur' in locals():
            cur.close()

@app.route('/add_artist', methods=['POST'])
def add_artist():
    try:
        name = request.form['name']
        age = request.form['age']
        country = request.form['country']  # Передаем ID страны, а не ее имя

        if not name or not age or not country:
            return "Name, age, and country_id are required fields"

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO artists (name, age, country) VALUES (%s, %s, %s)", (name, age, country))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": f"Added artist: {name}"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})
    finally:
        if 'cur' in locals():
            cur.close()

@app.route('/update_artist/<int:artist_id>', methods=['PUT'])
def update_artist(artist_id):
    try:
        name = request.form.get('name')
        age = request.form.get('age')
        country = request.form.get('country')

        if not name and not age and not country:
            return "At least one field (name, age, country) is required for update"

        cur = mysql.connection.cursor()
        update_query = "UPDATE artists SET "
        if name:
            update_query += f"name = '{name}', "
        if age:
            update_query += f"age = {age}, "
        if country:
            update_query += f"country = '{country}', "
        # Remove the trailing comma and space
        update_query = update_query[:-2]
        update_query += f" WHERE id = {artist_id}"
        
        cur.execute(update_query)
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": f"Updated artist with id {artist_id}"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})
    finally:
        if 'cur' in locals():
            cur.close()

@app.route('/delete_artist/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM artists WHERE id=%s", (artist_id,))
        mysql.connection.commit()
        return jsonify({"message": f"Deleted artist with id {artist_id}"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})
    finally:
        if 'cur' in locals():
            cur.close()

@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({"error": "Unauthorized. Token is missing or invalid"}), 401
        
        token = token.split('Bearer ')[1]  # извлекаем только токен, отбросив префикс "Bearer "
        
        if token not in tokens or datetime.now() > tokens[token]:
            return jsonify({"error": "Unauthorized. Invalid or expired token"}), 401
        
        username = request.form['username']
        password = request.form['password']
        museum_id = request.form.get('museum_id')  # Добавляем получение ID музея из запроса

        if not username or not password:
            return "Username and password are required fields"

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password, museum_id) VALUES (%s, %s, %s)", (username, password, museum_id))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({"message": f"User {username} added successfully"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})
    finally:
        if 'cur' in locals():
            cur.close()

#Чтобы удалить отправленный POST из таблицы без удаления самой таблицы, вам следует добавить возможность удаления записи по ее идентификатору (обычно первичному ключу). Вот как это сделать:

@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
        mysql.connection.commit()
        return jsonify({"message": f"Deleted user with id {user_id}"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})
    finally:
        if 'cur' in locals():
            cur.close()

@app.route('/add_museum', methods=['POST'])
def add_museum():
    try:
        name = request.form['name']
        location = request.form['location']

        if not name or not location:
            return "Name and location are required fields"

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO museums (name, location) VALUES (%s, %s)", (name, location))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({"message": f"Museum {name} added successfully"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})
    finally:
        if 'cur' in locals():
            cur.close()

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']

        # Проверка логина и пароля (здесь должна быть реализована проверка в базе данных)

        if username == 'Lissibeth' and password == '7777':
            # Генерация токена
            token = generate_token()
            tokens[token] = datetime.now() + TOKEN_EXPIRATION_TIME  # Сохранение времени истечения токена
            return jsonify({"token": token}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return jsonify({"error": "Unauthorized. Token is missing or invalid"}), 401
    
    token = token.split('Bearer ')[1]  # извлекаем только токен, отбросив префикс "Bearer "
    
    if token not in tokens or datetime.now() > tokens[token]:
        return jsonify({"error": "Unauthorized. Invalid or expired token"}), 401
    else:
        return jsonify({"message": "Welcome to the protected endpoint!"}), 200


if __name__ == '__main__':
    app.debug = True
    app.run()
