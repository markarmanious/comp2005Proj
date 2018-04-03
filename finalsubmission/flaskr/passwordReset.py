import os
import sqlite3
from flaskr import *
"""
Module for the Reset Password feature. Returns the data of the provided user and as well has a functin to set a new password.
"""


def getUserInfo(temp_user):
	"""
	Get the user infomation from the database. 
	Pass a user name and get the information.

		e.g. getUserInfo("icm")
			 getUserInfo(username)
	"""
	db = get_db()
	curr = db.execute('select * from users where username=?',(temp_user,))
	d = curr.fetchone()
	return d
	

def setPassword(temp_user, newP):
	"""

	Call the function with the user to which you want to reset the password to.
	And the new password to be inserted.
	The function resets the password with the the new password in the database.

		e.g. setPassword("icm", "*****")
			 setPassword(username, password)
	"""
	db = get_db()
	db.execute('''update users set pass = ? where username=?''', (newP, temp_user,))
	db.commit()



