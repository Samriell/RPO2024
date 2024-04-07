from flask import Flask, request
from flask_mysqldb import MySQL
from flask_restful import Resource, Api, reqparse
import json
from flask import jsonify


app = Flask(__name__)
api = Api(app)
mysql = MySQL(app)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'user1'
app.config['MYSQL_PASSWORD'] = 'v2769470+'
app.config['MYSQL_DB'] = 'art'


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


if __name__ == '__main__':
    app.debug = True
    app.run()