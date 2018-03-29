from flaskr import *

class Sub:

    def isSubscribed(user):
        ''' Checks if a user is subscribed '''

        db = get_db()
        cur = db.execute('select from subs topicId where userId = (?)', user)
        isSub = cur.fetchall()
        return isSub

    def create_subscription(user, topic):
        ''' Create a user subscription to a topic and add it to the database '''
        
        db = get_db()
        db.execute('insert into subs (userId, topicId, notified) values (?, ?, ?)',
                   user, topic, 1)
        db.commit()
        flash('Subscribed!')
        return redirect(url_for('show_topics'))

    def unsubscribe(user, topic):
        ''' Remove a user subscription from a topic '''

        db = get_db()
        db.execute('delete from subs where userId = (?), topicId = (?)', user, topic)
        db.commit()
        flash('Unsubscribed!')
        return redirect(url_for('show_topics'))

    def show_notifications(user):
        ''' Show a user's notifications on all relevant topics. To be called every time entries are shown'''
        
        db = get_db()
        cur = db.execute('select topicId from subs where userId = (?), notified = (?)', user, 0)
        sslist = cur.fetchall()
        return sslist

    def view_notification(user, topic):
        ''' Mark a notification as viewed. To be called when a user clicks on a notification'''
        
        db = get_db()
        db.execute('update subs set notified = (?) where userId = (?), topicId = (?)', 1, user, topic)
        db.commit()

    def update_subscription(topic):
        ''' Update all subscriptions when a new post is made within a topic '''
        
        db = get_db()
        db.execute('update subs set notified = (?) where topicId = (?)', 0, topic)
        db.commit()
        
