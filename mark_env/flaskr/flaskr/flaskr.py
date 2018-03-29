import os
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

userId = 1

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

def getTopicId(topicName):
    db = get_db()
    cur = db.execute('select id from  topics where title=?',[topicName])
    cur = cur.fetchone()
    topicId = cur[0]
    return topicId


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/topic/<topic>/sub', methods=['POST'])
def subscribe(topic):
    topicId= getTopicId(topic)
    create_subscription(userId, topicId)
    return redirect(url_for('show_topics'))
    

@app.route('/topic/<topic>/unsub', methods=['POST'])
def unSubscribe(topic):
    topicId= getTopicId(topic)
    unsubscribe(userId, topicId)
    return redirect(url_for('show_topics'))




@app.route('/')
def show_topics():
    db = get_db()
    cur = db.execute('select title,id from topics order by createdAt desc')
    subsList = isSubscribed(userId)
    notifiedList = show_notifications(userId)
    topics = cur.fetchall()
    print(notifiedList)
    return render_template('show_topics.html', topics=topics, subsList=subsList, notifiedList=notifiedList)

@app.route('/addtopic', methods=['POST'])
def add_topic():
    title = request.form['title']
    db = get_db()
    db.execute('insert into topics (userId, title) values (?, ?)',
                 [userId, title])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_topics'))
@app.route('/topic/<topic>/addpost', methods=['POST'])
def add_post(topic):
    content = request.form['content']
    title = request.form['title']
    db = get_db()
    db.execute('insert into posts (userId, title, content, topic) values (?, ?, ?, ?)',
                 [userId, title, content, topic])
    db.commit()
    update_subscription(getTopicId(topic))
    flash('New entry was successfully posted')
    return redirect(url_for('show_posts',topic=topic))
@app.route('/post/<postId>/editpost', methods=['GET','POST'])
def edit_post(postId):
    db = get_db()
    cur = db.execute('select title,content,topic from posts where id=?',[postId])    
    post = cur.fetchone()
    topic = post['topic']
    if(request.method == 'GET'):
    	return render_template('edit_post.html' ,post=post,postId=postId, topic=topic)	
    elif(request.method == 'POST'): 
	title = request.form['title']
	content = request.form['content']
        db.execute('update posts set title=?, content=? where id=?', [title,content,postId])
	db.commit()
	update_subscription(getTopicId(topic))
	return redirect(url_for('show_posts', topic=topic))

@app.route('/topic/<topic>',methods=['GET'])
def show_posts(topic):
    db = get_db()
    cur = db.execute('select title, content, userId, id from posts where topic=? order by createdAt desc', [topic])
    posts = cur.fetchall()
    view_notification(userId,getTopicId(topic))
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

from .sub import *
