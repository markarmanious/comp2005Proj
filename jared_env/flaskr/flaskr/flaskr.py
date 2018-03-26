#all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

import sys
print(sys.path)
import userGroupsInterface

app = Flask(__name__) #create the application instance
app.config.from_object(__name__) #load config from this file, flaskr.py

#load default config and override config from an environment variable
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

@app.cli.command('initdb')#When typing 'flask initdb' in terminal, flask recieves initdb as a "command". The decorator is then activated which wraps the function initdb_command() which calls the function init_db, runs it and on return prints 'Initialized the database.'So telling flask initdb is a command and it activates the decorator with that command
def initdb_command():
	"""Initializes the database"""
	init_db()
	userGroupsInterface.init_userGroupsDB()#POPE Added to initialize the user groups data base file
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


#POPE Added this for groups along with user_group.html template
@app.route('/groups', methods=['POST'])
def add_userGroup():
        if not session.get('logged_in'):
                abort(401)
        flash(userGroupsInterface.createGroup([request.form['groupName']], [request.form['usersInGroup']]))#Flash the message from the group creation attempt
        return redirect(url_for('user_groups'))

#POPE Added this for groups
@app.route('/user_groups')
def user_groups():
	return render_template('user_groups.html')#Displays the user groups web page


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
