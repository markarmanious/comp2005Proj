#all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__) #create the application instance
app.config.from_object(__name__) #load config from this file, flaskr.py

#load default config and override config from an environment variable
app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'flaskr.db'),
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default',
	QUESTION='none',
	ANSWER='none'
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

@app.cli.command('initdb')#When typing 'flask initdb' in terminal, flask recieves initdb as a "command". The decorator is then activated which wraps the function initdb_command() which calls the function init_db, runs it and on return prints 'Initialized the database.'So telling flask initdb is a command and it activates the decorator with that command
def initdb_command():
	"""Initializes the database"""
	init_db()
	print('Initialized the database.')

def get_db():
	"""Opens a new database connection if there is none yet for the current application context."""

	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	"""Closes the database again at the end of the request."""
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

@app.route('/')
def show_entries():
	db = get_db()
	cur = db.execute('select title, txtblock from entries order by id desc')#Database command ('select title, txtblock from entries order by id desc')
	entries = cur.fetchall()
	return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	db = get_db()
	#db.execute() is just shoving stuff at sqlite which will use it as commands (insert into entries (title, txtblock) values (?, ?) is actuall a series of sqlite commands to add data to the table)
	db.execute('insert into entries (title, txtblock) values (?, ?)',
			[request.form['title'], request.form['txtblock']])
	db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))
	

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))

temp_user = None #global variable to hold the user seeking to reset the password
@app.route('/security', methods=['GET', 'POST'])
def security():
'''
Get the username for the username seeking to reset password. If the username is in the database then render the question template with the user
question. If the username is not in the database reload the page.
'''
	if request.method == 'POST':
		global temp_user
		usr_in = request.form['usr']
		temp_user = usr_in
		db = get_db()
		curr = db.execute('select * from users where username=?',(usr_in,))
		u = curr.fetchone()
		if u:
			return render_template('question.html', user_details=u)
		else:
			flash('Worng Username')
			return redirect(url_for('security'))
	return render_template('security.html')

@app.route('/question', methods=['POST'])
def question():
'''
Get the answer entered by the user in response to the question and compare it to the one in the database. Renders the template to reset
the password. 
'''
	if request.method == 'POST':
		db = get_db()
		curr = db.execute('select * from users where username=?',(temp_user,))
		d = curr.fetchone()
		usr_ans = request.form['userAnswer']
		return render_template('enter_password.html', user_data=d, next=usr_ans)

#
@app.route('/newPassword', methods=['POST'])
def newPassword():
'''
Update the database with a new password password.
'''
	newP = request.form['newPass']
	db = get_db()
	db.execute('''update users set pass = ? where username=?''', (newP, temp_user,))
	db.commit()
	flash('Updated successfully')
	return redirect(url_for('show_entries')) #to update with new function from whoever

