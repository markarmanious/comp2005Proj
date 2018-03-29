

def unfoldToList(tpl):
    toReturnList = []
    for element in tpl:
        toReturnList.append(element[0])
    return toReturnList
def isSubscribed(user):
    ''' Checks if a user is subscribed '''

    db = get_db()
    cur = db.execute('select topicId from subs where userId = (?)', [user])
    subsTuples = cur.fetchall()
    subsList = unfoldToList(subsTuples)
    return subsList

def create_subscription(user, topic):
    ''' Create a user subscription to a topic and add it to the database '''
    
    db = get_db()
    db.execute('insert into subs (userId, topicId, notified) values (?, ?, ?)',
               [user, topic, 1])
    db.commit()
    flash('Subscribed!')
    

def unsubscribe(user, topic):
    ''' Remove a user subscription from a topic '''

    db = get_db()
    db.execute('delete from subs where userId = ? and topicId = ?', [user, topic])
    db.commit()
    flash('Unsubscribed!') 

def show_notifications(user):
    ''' Show a user's notifications on all relevant topics. To be called every time entries are shown'''
    
    db = get_db()
    cur = db.execute('select topicId from subs where userId =? and notified =?', [user, 0])
    sslist = unfoldToList(cur.fetchall())
    return sslist

def view_notification(user, topic):
    ''' Mark a notification as viewed. To be called when a user clicks on a notification'''
    
    db = get_db()
    db.execute('update subs set notified = (?) where userId = (?) and topicId = (?)', [1, user, topic])
    db.commit()

def update_subscription(topic):
    ''' Update all subscriptions when a new post is made within a topic '''
    
    db = get_db()
    db.execute('update subs set notified = (?) where topicId = (?)', [0, topic])
    db.commit()
    
from .flaskr import *
