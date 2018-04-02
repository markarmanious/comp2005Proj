"""This is the main code for the user groups functional requirement from the 2005 group project.
This code is intended to be used with flaskr.py and userGroupsInterface.py. All calles to this
code are expected to go through userGroupsInterface.py. This code is designed to be as compartmentalized
as possiable, meaning it handles it's own persistance through an sqlite database and is meant to be
detachable from the main code and replaced with minimial to no recoding needed in the flaskr.py file.
Should this code be modified or replaced, userGroupsInterface.py is the only code that would need to
be modified to work with whatever replaces this. flaskr.py should be completely unaware of any changes
made here.

"""

import sqlite3



def connect_db():
	"""Connects to the user group database."""
	
	databaseConnection = sqlite3.connect('schema.db')#Connect to the database
	databaseConnection.row_factory = sqlite3.Row#Set the row factory method to comply with sqlite3
	return databaseConnection#Return the connection object back to caller


def init_userGroupsDB():
    """Initialize the database for user groups using the userGroupSchema sql file"""
    
    db = connect_db()#Connect to the database
    with open('schema.sql', mode='r') as f:#Open the schema file
            db.cursor().executescript(f.read())#Apply the schema to the database
    db.commit()#Actually make the changes
    db.close()#Close the database connection


def searchDB():
    """Prints the entire user groups table from user groups database"""
    
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM userGroups")
    rows = cursor.fetchall()
    for row in rows:
        print("Group: ", row[0])
        print("Members: ", row[1])
    db.close()


def getMembersByGroup(group):
    """Search the database by group ID

    group - group ID of desired group

    return - group members in desired group if group exists
    """
    
    db = connect_db()#Connect to the user groups database
    cursor = db.cursor()#Create cursor object for searching the database table
    cursor.execute("SELECT usersInGroup FROM userGroups WHERE groupName=?", (group,))#Search the database for the user group id and return the members of that group
    rows = cursor.fetchall()#Store the group members in a variable
    if len(rows) == 1:#If there is only one item then the group was found
        db.close()#Close the database connection
        return rows[0][0]#Return the group members
    elif (len(rows) == 0):#If there are no items then the group is not in the table
        db.close()#Close the database
        return False#IMPLEMENT: Need to return an error message
    else:#If anything other than the above two conditions are met then something has gone very wrong
        print("Something has gone wrong and there are multiple results in the table")
        db.close()
        return#Need to report the issue for system maintaince

def getGroupsByMember(userName):
    """Given a username, returns a list of all groups to which the member belongs

    Arguments:
    userName - The username of the person

    returns:
    A list of all group's to which the user belongs
    """
    groupList = []#Create a blank list to fill with the members's groups
    db = connect_db()#Connect to the database
    cursor = db.cursor()#Create a cursor to search the database
    cursor.execute("SELECT * FROM userGroups")#Get all items in the user groups table
    rows = cursor.fetchall()#Place all the items in a variable
    for row in rows:#For each group and membership
        if row[1].find(userName) != -1:#If the member is in the group
            groupList.append(row[0])#Add the group to the list of groups
    db.close()#Close the database connection
    return groupList#Return the list of groups to which the given member belongs


def updateGroupMembership(group, membership):
    """Updates the given groups membership with the given membership

    group - the ID of the group to be updated
    membership - a string containing the new group membership

    returns - None
    """

    db = connect_db()#Connect to the user groups database
    cursor = db.cursor()#Create cursor object for manipulating the database table
    cursor.execute("UPDATE userGroups SET usersInGroup=? WHERE groupName=?", (membership, group))#Search the database for the user group id and update the list of group members
    db.commit()#Commit the changes to the database
    db.close()#Close the database connection
    return None



def createGroup(group, users):
    """A method used to create a new user group

    group - the ID of the group to be created
    users - the users to add to the group

    return - returns a string message indicating success or failure
    """

    db = connect_db()#Connect to the database
    try:#If the group doesn't exist, add the group and members to the database
        db.execute('insert into userGroups (groupName, usersInGroup) values (?, ?)', (group, users))#Add the group and it's members the the database
        db.commit()#Commit changes to the database
        db.close()#Close the connection to the database
        return 'New group was successfully created'#Return a succes message
    except sqlite3.IntegrityError:#If the group already exists, close the database and return an error
        db.close()#Close the connection to the database
        return 'Error. Group already exists'#Return a failure message

def checkIfGroupExists(group):
    """A method used to check if a group exists

    group - the ID of the group being checked

    return - returns True is group exists and False if it does NOT exist
    """
    
    db = connect_db()#Connect to the user groups database
    cursor = db.cursor()#Create cursor object for searching the database table
    cursor.execute("SELECT usersInGroup FROM userGroups WHERE groupName=?", (group,))#Search the database for the user group id and return the members of that group
    rows = cursor.fetchall()#Store the group members in a variable
    if (len(rows) == 0):#If there are no items then the group is not in the table
        db.close()#Close the database
        return False#The group does not exist (or has no members which is the same as not existing)
    else:#If there are group members in the group, it must exist
        db.close()
        return True#The group exists


def addMemberToGroup(group, member):
    """A method used to add a user to a group

    Arguments:
    group - The ID of a group which already exists
    member - The username of the member to add to the list

    returns - A string containing a success or error message
    """

    groupMembers = getMembersByGroup(group)#Get the members from the given group
    if groupMembers == False:#Group does not exist
        return "Error: Group " + group + " does not exist"#Return no group error message
    if groupMembers.find(member) == -1:#If member is not in list of group members
        groupMembers = groupMembers + " " + member#Add the member to the list of group members
        updateGroupMembership(group, groupMembers)#Update the group membership in the database
        return member + " successfully added to group " + group#Return a success message
    elif groupMembers.find(member) != -1:#If member is already in the list of group members
        return "Error: Member " + member + " is already in group " + group#Return a message indicating the member is already in the group
    
    
def removeMemberFromGroup(group, member):
    """A method used to remove a user from a group

    Arguments:
    group - The ID of a group which already exists
    member - The username of the member to add to the list

    returns - String message indicating success or failure
    """

    groupMembers = getMembersByGroup(group)#Get the members from the given group
    if groupMembers == False:#Group does not exist
        return "Error: Group " + group + " does not exist"#Return no group error message
    if groupMembers.find(member) == -1:#If member is not in list of group members
        return "Error: " + member + " is not in group " + group#Return a message indicating that the member is not in the given group
    else:
        groupMembersUpdated = groupMembers.replace(member, '')#Remove the member from the group membership
        updateGroupMembership(group, groupMembersUpdated)#Update the groups membership in the database
        return "Successfully removed " + member + " from group " + group#Return a message indicating success
    

def validateUser(userName, topicGroupID):
    """A method used to check if a user is a member of
    the group associated with the topic

    Arguments:
    userName - The username of the person trying to access the topic
    topicGroupID - The group ID associated with the topic the user is trying to access

    returns:
    True if the user is a member of the group
    False if the user is not a member of the group
    """

    groupMembers = getMembersByGroup(topicGroupID)#Get the members from the given group
    if groupMembers == False:#Group does not exist
        return "Error: Group " + group + " does not exist"#Return no group error message
    elif groupMembers.find(userName) == -1:#If member is not in list of group members
        return False
    else:#If member is in in the group
        return True
    
