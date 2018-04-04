import unittest
import passwordReset

class passwordResetTest(unittest.TestCase):

	def setUP(self):
		self.ans = False
		self.ans2 = False

    	#test if a connection is made
	def test_connection(self):
		r = passwordReset.createConnection()
		self.assertNotEqual(r, None)

	#test if a wrong user name is provided
	def test_WrongUser(self):
		r = passwordReset.getUserInfo('icm')
		if r is None:
			self.ans = True
		self.assertTrue(self.ans)

	#test if a correct user name is provided
	def test_User(self):
		r = passwordReset.getUserInfo('mark')
		if (len(r)>0):
			self.ans2 = True
		self.assertTrue(self.ans2)

if __name__ == '__main__':
    unittest.main()
