import unittest
from subscriptions import *

''' This module provides a test suite for the subscriptions.py package. It does so by initializing
    the database and inserting an entry into it, then testing if the methods can retrieve it. As
    there are only three functions in the subscriptions module that have return values, this test
    suite only tests those three functions. '''

class TestSubMethods(unittest.TestCase):

    ''' Initialize the database and insert a test entry into it. '''
    def setUp(self):
        init_db()
        db = get_db()
        db.execute('insert into subs (userId, topicId, notified) values (?, ?, ?)', [1000, 1000, 0])
        db.commit()

    ''' Test if the unfoldToList method can correctly extract information from sqlite3 tuple format. '''
    def test_unfold(self):
        tpl = ((1,),(2,),(3,))
        self.assertEqual([1, 2, 3], unfoldToList(tpl))

    ''' Test if the isSubscribed method is correctly retrieving topicIds. '''
    def test_is_subscribed(self):
        self.assertEqual([1000], isSubscribed(1000))

    ''' Test if the show_notifications method is correctly retrieving topicIds. '''
    def test_show_notifications(self):
        self.assertEqual([1000], show_notifications(1000))
        
