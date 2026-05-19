import sys
sys.path.append('.')

import sqlite3
import os

def get_db():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def create_user(username, password):
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def update_user(user_id, username, password):
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE users SET username = ?, password = ? WHERE id = ?', (username, password, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
