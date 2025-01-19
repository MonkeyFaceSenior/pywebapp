# main page in flask diary app
import mysql.connector
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
config = {
  'user': 'diary',
  'password': 'Abc123321!',
  'host': '192.168.69.207',
  'port':3307,
  'database': 'hannadiary',
  'raise_on_warnings': True
}


def get_db_connection():
    conn = mysql.connector.connect(**config)
    return conn


def get_db_connection_old():
    conn = sqlite3.connect('./flask_blog/database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts WHERE id = %s', (post_id,))
    posts = cursor.fetchone()
    if posts is None:
        abort(404) 
    # Convert rows to a list of dictionaries
   # columns = [desc[0] for desc in cursor.description] 
    #result = [dict(zip(columns, posts))]
    cursor.close()
    conn.close()
    return posts

conn = get_db_connection()
cursor = conn.cursor()
cursor.execute('SELECT * FROM posts')
posts = cursor.fetchall()
# Convert rows to a list of dictionaries
columns = [desc[0] for desc in cursor.description]  # Get column names
result = [dict(zip(columns, post)) for post in posts]
print(cursor.description)
cursor.close()
conn.close() 
print("new!")

print(result)


conn_old = get_db_connection_old()
posts_old = conn_old.execute('SELECT * FROM posts').fetchall()
conn_old.close() 

print("old!")
print(posts_old)

post2 = get_post(7)
print(post2)