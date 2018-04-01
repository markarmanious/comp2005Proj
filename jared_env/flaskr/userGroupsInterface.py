"""The interface for the user groups part of the 2005 group project.
Flaskr should import this interface and use it to make changes to
or get information from the user groups system.
This interface will take the data it is given, change it into a form
that is usable by the userGroups.py code and make the calls to the
userGroups.py code. It will then take the return information, change it
into a form that is usable by flaskr.py, and return it to flaskr.py (the
intended caller).

"""

import userGroups

def init_userGroupsDB():
    """Initializes the database for user groups"""
    userGroups.init_userGroupsDB()


def createGroup(group, users):
    """An interface method used to create a new user group

    group - the ID of the group to be created
    users - the users to add to the group

    return - returns a string message indicating success or failure
    """
    
    return userGroups.createGroup(group[0], users[0])

def addMemberToGroup(group, member):
    """An interface method used to add a user to a group

    Arguments:
    group - The ID of a group which already exists
    member - The username of the member to add to the list

    returns - A string containing a success or error message
    """
    group = str(group[0])#Convert the given list object into a string object for processing
    member = str(member[0])#Convert the given list object into a string object for processing
    for i in group:#Check for spaces in group id to ensure only one group was entered
        if i == " ":#If spaces found
            return "Error: A group ID has no spaces in it. Please enter only one group ID"#Return error message
    for i in member:#Check for spaces in username to ensure only one user was entered
        if i == " ":#If spaces found
            return "Error: A username has no spaces in it. Please add one group member at a time."#Return error message

    return userGroups.addMemberToGroup(group, member)

def removeMemberFromGroup(group, member):
    """An interface method used to remove a user from a group

    Arguments:
    group - The ID of a group which already exists
    member - The username of the member to add to the list

    returns:returns - String message indicating success or failure
    """

    group = str(group[0])#Convert the given list object into a string object for processing
    member = str(member[0])#Convert the given list object into a string object for processing
    for i in group:#Check for spaces in group id to ensure only one group was entered
        if i == " ":#If spaces found
            return "Error: A group ID has no spaces in it. Please enter only one group ID"#Return error message
    for i in member:#Check for spaces in username to ensure only one user was entered
        if i == " ":#If spaces found
            return "Error: A username has no spaces in it. Please remove one group member at a time."#Return error message


    return userGroups.removeMemberFromGroup(group, member)

def validateUser(userName, topicGroupID):
    """An interface method used to check if a user is a member of
    the group associated with the topic

    Arguments:
    userName - The username of the person trying to access the topic
    topicGroupID - The group ID associated with the topic the user is trying to access

    returns:
    True if the user is a member of the group
    False if the user is not a member of the group
    """

    return userGroup.validateUser(userName, topicGroupID)

def getGroupMembership(userName):
    """Given a username, returns a list of all groups to which the member belongs

    Arguments:
    userName - The username of the person

    returns:
    A list of all group's to which the user belongs
    """

    return userGroup.getGroupsByMember(userName)
