''' This module provides functionality for user subscription to topic threads in flaskr, and for subsequent notification
    of new posts in subscribed threads. It is imported to the main module, flaskr.py, where its functions are called
    at corresponding trigger events. Subscriptions are stored in the subs table of the database, which is created during
    database initialization. This table contains a primary key ID for each subscription, as well as a userID, topicID,
    and a notified integer value (1 or 0) indicating if the latest version of a subscribed thread has been viewed by the
    user or not.'''

def unfoldToList(tpl):
    ''' Helper function that receives values from the sqLite3 database as tuples, and converts them to list format.

    Arguments:
    tpl - A tuple of values

    Returns:
    toReturnList - A list of values '''
    
    toReturnList = []
    for element in tpl:
        toReturnList.append(element[0])
    return toReturnList

def isSubscribed(user):
    ''' Identify all topic threads to which a user has subscribed. This function is used to determine whether the
    Subscribe or Unsubscribe button should be displayed on each topic.

    Arguments:
    user - The ID of a user (integer)

    Returns:
    subsList - A list of topicIDs (integers) for threads that the user has subscribed to '''

    db = get_db()
    cur = db.execute('select topicId from subs where userId = (?)', [user])
    subsTuples = cur.fetchall()
    subsList = unfoldToList(subsTuples)
    return subsList

def create_subscription(user, topic):
    ''' Create a new subscription in the database. Called whenever the Subscribe button is clicked.

    Arguments:
    user - The ID of a user (integer)
    topic - The ID of the topic to which the user is subscribing (integer)

    Returns:
    Nothing -- the function adds a row to the subs table and flashes a success message. '''
    
    db = get_db()
    db.execute('insert into subs (userId, topicId, notified) values (?, ?, ?)',
               [user, topic, 1])
    db.commit()
    flash('Subscribed!')
    

def unsubscribe(user, topic):
    ''' Delete a subscription from the database. Called whenever the Unsubscribe button is clicked.

    Arguments:
    user - The ID of a user (integer)
    topic - The ID of the topic from which the user is unsubscribing (integer)

    Returns:
    Nothing -- the function deletes a row from the subs table and flashes a success message. '''

    db = get_db()
    db.execute('delete from subs where userId = ? and topicId = ?', [user, topic])
    db.commit()
    flash('Unsubscribed!') 

def show_notifications(user):
    ''' Show a notification on each thread which a user has subscribed to, and has not viewed since it was last
    updated. Called whenever the Show Topics page is loaded.

    Arguments:
    user - The ID of a user (integer)

    Returns:
    ssList - A list of topicIDs (integers) for threads that should have a notification displayed. '''
    
    db = get_db()
    cur = db.execute('select topicId from subs where userId =? and notified =?', [user, 0])
    sslist = unfoldToList(cur.fetchall())
    return sslist

def view_notification(user, topic):
    ''' Mark a notification as viewed, turning it off until the next time the associated topic thread is updated.
    Called when a user navigates to the page of a topic that was displaying a notification.

    Arguments:
    user - The ID of a user (integer)
    topic - The ID of the topic displaying the notification (integer)

    Returns:
    Nothing -- the function switches the value of notified from 0 to 1 in the corresponding row of the subs table. '''
    
    db = get_db()
    db.execute('update subs set notified = (?) where userId = (?) and topicId = (?)', [1, user, topic])
    db.commit()

def update_subscription(topic):
    ''' Update all subscriptions when a new post (or edit) is made within a topic thread. This topic thread will subsequently
    display a notification to all subscribed users.

    Arguments:
    topic - The ID of a topic (integer)

    Returns:
    Nothing -- the function switches the value of notified to 0 for all rows of the subs table containing the given
               topicID. '''
    
    db = get_db()
    db.execute('update subs set notified = (?) where topicId = (?)', [0, topic])
    db.commit()
    
from .flaskr import *
