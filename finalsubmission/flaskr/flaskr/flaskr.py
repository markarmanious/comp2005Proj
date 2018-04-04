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
    userId = getUserId()
    topicId= getTopicId(topic)
    create_subscription(userId, topicId)
    return redirect(url_for('show_topics'))
    

@app.route('/topic/<topic>/unsub', methods=['POST'])
def unSubscribe(topic):
    userId = getUserId()
    topicId= getTopicId(topic)
    unsubscribe(userId, topicId)
    return redirect(url_for('show_topics'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    return registerUser()





@app.route('/')
def show_topics():
    userId = getUserId()
    db = get_db()
    cur = db.execute('select title,id,groupDisscution from topics order by createdAt desc')
    userNameCur = db.execute('select userName from users where isLoggedIn=?',[1])
    groupList = []
    subsList = []
    notifiedList = []
    groupsList = []
    userName = userNameCur.fetchone()
    if userName :
        userName = userName[0]
        groupsList = getGroupMembership(userName)
        subsList = isSubscribed(userId)
        notifiedList = show_notifications(userId)
    topics = cur.fetchall()
    return render_template('show_topics.html', topics=topics, subsList=subsList, notifiedList=notifiedList,groupsList=groupsList)

@app.route('/addtopic', methods=['POST'])
def add_topic():
    userId = getUserId()
    title = request.form['title']
    gorup = request.form['groupDisscution']
    db = get_db()
    db.execute('insert into topics (userId, title) values (?, ?)',
                 [userId, title])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_topics'))
@app.route('/topic/<topic>/addpost', methods=['POST'])
def add_post(topic):
    userId = getUserId()
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
    userId = getUserId()
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
    userId = getUserId()
    db = get_db()
    cur = db.execute('select title, content, userId, id from posts where topic=? order by createdAt desc', [topic])
    posts = cur.fetchall()
    view_notification(userId,getTopicId(topic))
    return render_template('show_posts.html', posts=posts, topic = topic, userId=userId) 

@app.route('/groups', methods=['POST'])
def add_userGroup():
        if not session.get('logged_in'):
                abort(401)
        flash(userGroupsInterface.createGroup([request.form['groupName']], [request.form['usersInGroup']]))#Flash the message from the group creation attempt
        return redirect(url_for('user_groups'))

@app.route('/user_groups')
def user_groups():
	return render_template('user_groups.html')#Displays the user groups web page
@app.route('/remove_user_from_a_group', methods=['POST'])
def remove_userFromAGroup():
        if not session.get('logged_in'):
                abort(401)
        flash(userGroupsInterface.removeMemberFromGroup([request.form['existingGroupNameRemove']], [request.form['memberToRemove']]))#Flash the message from the remove member attempt
        return redirect(url_for('user_groups'))

    
@app.route('/add_user_to_group', methods=['POST'])
def add_userToAGroup():
        if not session.get('logged_in'):
                abort(401)
        flash(userGroupsInterface.addMemberToGroup([request.form['existingGroupName']], [request.form['memberToAdd']]))#Flash the message from the add member attempt
        return redirect(url_for('user_groups'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return logUserIn()

@app.route('/logout')
def logout():
    return logUserOut()
temp_user = None #global variable to hold the user seeking to reset the password
@app.route('/security', methods=['GET', 'POST'])
def security():

	if request.method == 'POST':
		global temp_user
		usr_in = request.form['usr']
		temp_user = usr_in
		u = getUserInfo(usr_in)
		if u:
			return render_template('question.html', user_details=u)
		else:
			flash('Worng Username')
			return redirect(url_for('security'))
	return render_template('security.html')

@app.route('/question', methods=['POST'])
def question():

	if request.method == 'POST':
		d = getUserInfo(temp_user)
		usr_ans = request.form['userAnswer']
		return render_template('enter_password.html', user_data=d, next=usr_ans)


@app.route('/newPassword', methods=['POST'])
def newPassword():

	newP = request.form['newPass']
	setPassword(temp_user, newP)
	flash('Updated successfully')
	return redirect(url_for('show_topics')) #to update with new function from whoever
from passwordReset import *
from .subscriptions import *
from loginInterface import *
from userGroupsInterface import *
import userGroupsInterface
    
