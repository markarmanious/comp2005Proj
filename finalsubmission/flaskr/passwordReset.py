import os
import sqlite3
database = 'flaskr/flaskr.db'
"""
Module for the Reset Password feature. Returns the data of the provided user and as well has a functin to set a new password.
"""
def createConnection():
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	#cur = conn.cursor()
	return conn

def getUserInfo(temp_user):
	"""
	Get the user infomation from the database. 
	Pass a user name and get the information.

		e.g. getUserInfo("icm")
			 getUserInfo(username)
	"""
	db = createConnection()
	con = db.cursor()
	curr = con.execute('select * from Users where username=?',(temp_user,))
	d = curr.fetchone()
	db.close()
	return d
	

def setPassword(temp_user, newP):
	"""

	Call the function with the user to which you want to reset the password to.
	And the new password to be inserted.
	The function resets the password with the the new password in the database.

		e.g. setPassword("icm", "*****")
			 setPassword(username, password)
	"""
	db = createConnection()
	con = db.cursor()
	con.execute('''update Users set pass = ? where username=?''', (newP, temp_user,))
	db.commit()
	db.close()


