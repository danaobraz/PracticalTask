import sqlite3
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

DB_FOLDER = '/data'
DB_PATH = os.path.join(DB_FOLDER, 'users.db')


def init_db():
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users 
                   (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                    (data.get('username'), data.get('password')))
        conn.commit()
        return jsonify({"message": "User created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                (data.get('username'), data.get('password')))
    user = cur.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful", "user_id": user[0]}), 200
    return jsonify({"message": "Invalid credentials"}), 401


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)