import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash



app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_topics():
    db = get_db()
    cur = db.execute('select title from topics order by createdAt desc')
    topics = cur.fetchall()
    return render_template('show_topics.html', topics=topics)

@app.route('/addtopic', methods=['POST'])
def add_topic():
    userId = "2"
    title = request.form['title']
    db = get_db()
    db.execute('insert into topics (userId, title) values (?, ?)',
                 [userId, title])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_topics'))
@app.route('/topic/<topic>/addpost', methods=['POST'])
def add_post(topic):
    userId = "2"
    content = request.form['content']
    title = request.form['title']
    print(content)
    db = get_db()
    db.execute('insert into posts (userId, title, content, topic) values (?, ?, ?, ?)',
                 [userId, title, content, topic])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_posts',topic=topic))
@app.route('/post/<postId>/editpost', methods=['GET','POST'])
def edit_post(postId):
    db = get_db()
    cur = db.execute('select title,content,topic from posts where id=?',[postId])    
    post = cur.fetchone()
    topic = post['topic']
    print(post['content'])
    if(request.method == 'GET'):
    	return render_template('edit_post.html' ,post=post,postId=postId, topic=topic)	
    elif(request.method == 'POST'): 
	title = request.form['title']
	content = request.form['content']
        db.execute('update posts set title=?, content=? where id=?', [title,content,postId])
	db.commit()
	return redirect(url_for('show_posts', topic=topic))

@app.route('/topic/<topic>',methods=['GET'])
def show_posts(topic):
    db = get_db()
    userId = "1"
    cur = db.execute('select title, content, userId, id from posts where topic=? order by createdAt desc', [topic])
    posts = cur.fetchall()
    return render_template('show_posts.html', posts=posts, topic = topic, userId=userId) 

    
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != "nana":
            error = 'Invalid username'
        elif request.form['password'] != "nana":
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_topics'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_topics'))


