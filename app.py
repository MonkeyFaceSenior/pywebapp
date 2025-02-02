import os
import mysql.connector
from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.exceptions import abort

config = {
  'user': 'diary',
  'password': 'Abc123321!',
  'host': '192.168.69.207',
  'port': 3307,
  'database': 'hannadiary',
  'raise_on_warnings': True
}

def get_db_connection():
    conn = mysql.connector.connect(**config)
    return conn

def get_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM posts WHERE id = %s', (post_id,))
    post = cursor.fetchone()
    if post is None:
        abort(404)
    cursor.close()
    conn.close()
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
PASSWORD = 'your_password'  # Replace with your desired password

# default website here... eg: http://localhost:5000
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM posts ORDER BY id DESC;')
    posts = cursor.fetchall()
    cursor.close()
    conn.close()

    # Check for image files
    for post in posts:
        post_date = post['created'].strftime('%Y-%m-%d')
        image_path = f'c:\\users\\shiuming\\pictures\\{post_date}.jpg'
        post['has_image'] = os.path.exists(image_path)

    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('index'))

@app.before_request
def restrict_to_authenticated_user():
    if request.endpoint in ['post'] and not session.get('authenticated'):
        return redirect(url_for('login'))

# view individual post here ... eg: http://localhost:5000/5 (show the detail of post #5)
@app.route('/<int:post_id>')
def post(post_id):
    postdata = get_post(post_id)
    return render_template('post.html', post=postdata)

# create new post here ... eg: http://localhost:5000/create
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
            cursor.execute('INSERT INTO posts (title, content) VALUES (%s, %s)',
                         (title, content))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')


# edit individual post here ... eg: http://localhost:5000/5/edit (show the detail of post #5 and allow for edit)
@app.route('/<int:post_id>/edit', methods=('GET', 'POST'))
def edit(post_id):
    post = get_post(post_id)    

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE posts SET title = %s, content = %s WHERE id = %s',
                         (title, content, post_id))

            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

# delete an individual post here ... eg: http://localhost:5000/5/delete (delete post #5)
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM posts WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
