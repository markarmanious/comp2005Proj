import os
import sys
sys.path.append('../')
import userGroups
import unittest

class UserGroupTestCase(unittest.TestCase):

    def setUp(self):
        userGroups.dataBase = 'testdb.db'
        userGroups.schema = 'flaskr/schema.sql'
        userGroups.init_userGroupsDB()
        self.group = 'group1'
        self.member = 'John'
        self.notAGroup = 'notAGroup'
        self.member2 = 'Mark'

    def test_createGroup(self):
        self.assertEqual(userGroups.createGroup(self.group, self.member), 'New group was successfully created')
        self.assertEqual(userGroups.createGroup(self.group, self.member), 'Error. Group already exists')

    def test_checkIfGroupExists(self):
        userGroups.createGroup(self.group, self.member)
        self.assertTrue(userGroups.checkIfGroupExists(self.group))
        self.assertFalse(userGroups.checkIfGroupExists(self.notAGroup))

    def test_addMemberToGroup(self):
        userGroups.createGroup(self.group, self.member)
        self.assertEqual(userGroups.addMemberToGroup(self.notAGroup, self.member2), "Error: Group " + self.notAGroup + " does not exist")
        self.assertEqual(userGroups.addMemberToGroup(self.group, self.member2), self.member2 + " successfully added to group " + self.group)
        self.assertEqual(userGroups.addMemberToGroup(self.group, self.member), "Error: Member " + self.member + " is already in group " + self.group)

    def test_removeMemberFromGroup(self):
        userGroups.createGroup(self.group, self.member)
        self.assertEqual(userGroups.removeMemberFromGroup(self.notAGroup, self.member), "Error: Group " + self.notAGroup + " does not exist")
        self.assertEqual(userGroups.removeMemberFromGroup(self.group, self.member2), "Error: " + self.member2 + " is not in group " + self.group)
        self.assertEqual(userGroups.removeMemberFromGroup(self.group, self.member), "Successfully removed " + self.member + " from group " + self.group)

    def test_validateUser(self):
        userGroups.createGroup(self.group, self.member)
        self.assertTrue(userGroups.validateUser(self.member, self.group))
        self.assertFalse(userGroups.validateUser(self.member2, self.group))
    
if __name__ == '__main__':
    unittest.main()
