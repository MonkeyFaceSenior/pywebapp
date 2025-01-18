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
    post = cursor.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    cursor.close()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
   
   # Convert rows to a list of dictionaries
    columns = [desc[0] for desc in cursor.description]  # Get column names
    result = [dict(zip(columns, post)) for post in posts]

    cursor.close()
    conn.close() 

    conn_old = get_db_connection_old()
    posts_old = conn_old.execute('SELECT * FROM posts').fetchall()
    conn_old.close() 

    return render_template('index.html', posts=result)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))