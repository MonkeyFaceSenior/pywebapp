# main page in flask diary app
import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for, flash, redirect, session
from authlib.integrations.flask_client import OAuth
from werkzeug.exceptions import abort

load_dotenv()

config = {
  'user': 'diary',
  'password': 'Abc123321!',
  'host': 'homeysrv.local.lau.fm',
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
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key')
app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET')
app.config['OAUTHLIB_INSECURE_TRANSPORT'] = os.environ.get('OAUTHLIB_INSECURE_TRANSPORT', '1')

oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)

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

@app.route('/login')
def login():
    if session.get('authenticated'):
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/login/google')
def login_google():
    if not app.config['GOOGLE_CLIENT_ID'] or not app.config['GOOGLE_CLIENT_SECRET']:
        flash('Google OAuth is not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.', 'danger')
        return redirect(url_for('login'))
    redirect_uri = url_for('authorize_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/authorize/google')
def authorize_google():
    token = oauth.google.authorize_access_token()
    user_info = None
    try:
        user_info = oauth.google.parse_id_token(token)
    except Exception:
        pass
    if not user_info:
        resp = oauth.google.get('userinfo')
        user_info = resp.json()

    session['authenticated'] = True
    session['user'] = user_info.get('email') or user_info.get('name') or 'Google user'
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    session.pop('user', None)
    return redirect(url_for('index'))

@app.before_request
def restrict_to_authenticated_user():
    if request.endpoint in ['post', 'create', 'edit', 'delete'] and not session.get('authenticated'):
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
