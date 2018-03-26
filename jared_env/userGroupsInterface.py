import userGroups

def init_userGroupsDB():
    """Initializes the database for user groups"""
    userGroups.init_userGroupsDB()

def get_db():
    """Gets the database for user groups

    Returns the connection object to the caller
    """
    return userGroups.connect_db()

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

    return userGroups.addMemberToGroup(group, member)

def removeMemberFromGroup(group, member):
    """An interface method used to remove a user from a group

    Arguments:
    group - The ID of a group which already exists
    member - The username of the member to add to the list

    returns:returns - String message indicating success or failure
    """

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
