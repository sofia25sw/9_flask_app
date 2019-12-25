from flask import Flask, request, jsonify
import sqlite3
import hashlib
import datetime

app = Flask(__name__)


@app.route('/users', methods=['GET'])
def get_users():
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        cur.execute('select * from users')
        result = cur.fetchall()
        return jsonify(result)


@app.route('/users', methods=['POST'])
def registr():
    if not (request.json and 'user_name' in request.json and 'password' in request.json):
        return '', 400
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        cur.execute('select username from users where username = ?', (request.json['user_name'],))
        result = cur.fetchone()
        if result is not None:
            return jsonify({'status':'user already exists'}), 400
        pwd = request.json['user_name']+request.json['password']
        pwd = hashlib.md5(pwd.encode()).hexdigest()
        date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        cur.execute('insert into users values (?,?,?)', (request.json['user_name'], pwd, date))
        return jsonify({'status':'success'})


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')
