import unittest
import passwordReset

class passwordResetTest(unittest.TestCase):

    def setUP(self):
        self.wuser = 'icm'
        self.user = 'mark'
    
    def test_connection(self):
        self.resu
        r = self.createConnection()
        self.assertNotEqual(r, None)

    def test_WrongUser(self):
        self.ans
        r = self.getUserInfo('icm')
        if r is None:
            ans = True
        self.assertEqual(ans)

    def test_User(self):
        self.ans2
        r = self.getUserInfo('mark')
        if (len(r)>0):
            ans2 = True
        self.assertTrue(ans2)

if __name__ == '__main__':
    unittest.main()