from flaskr import *

class Sub:

    def get_user_id():
        ''' Dummy function to receive the id of the active user '''
        
        return 0

    def get_topic_id():
        ''' Dummy function to receive the id of a topic '''
        
        return 0

    def create_subscription():
        ''' Create a user subscription to a topic and add it to the database '''
        
        user = get_user_id()
        topic = get_topic_id()
        db = get_db()
        db.execute('insert into subscriptions (userid, topicid, viewed) values (?, ?, ?)',
                   user, topic, True)
        db.commit()
        flash('Subscribed!')
        return redirect(url_for('show_entries'))

    def unsubscribe():
        ''' Remove a user subscription from a topic '''

        user = get_user_id()
        topic = get_topic_id()
        db = get_db()
        db.execute('delete from subscriptions where userid = (?), topicid = (?)', user, topic)
        db.commit()

    def show_notifications():
        ''' Show a user's notifications on all relevant topics. To be called every time entries are shown'''
        
        user = get_user_id()
        db = get_db()
        cur = db.execute('select topicid from subscriptions where userid = (?), viewed = (?)', user, False)
        sslist = cur.fetchall()
        #add code to check topicids against all ids in entries, highlight posts that match

    def view_notification():
        ''' Mark a notification as viewed. To be called when a user clicks on a notification'''
        
        user = get_user_id()
        topic = get_topic_id()
        db = get_db()
        db.execute('update subscriptions set viewed = (?) where userid = (?), topicid = (?)', True, user, topic)
        db.commit()
        return redirect(url_for('show_entries'))

    def update_subscription():
        ''' Update all subscriptions when a new post is made within a topic '''
        
        topic = get_topic_id()
        db = get_db()
        db.execute('update subscriptions set viewed = False where topicid = (?)', topic)
        db.commit()
        
