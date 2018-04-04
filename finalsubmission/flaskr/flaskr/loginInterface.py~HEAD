
def registerUser():
    db = get_db()
    if (request.method =='GET'):
        return render_template('register.html')
    else:
        userName = request.form['username']
        password = request.form['password']
        question = request.form['question']
        answer = request.form['answer']
        cur = db.execute('select username from users where userName=?',[userName])
        user = cur.fetchall()
        print(user)
        if (len(user) == 0):
            db.execute('insert into users (userName, pass, question, answer, isLoggedIn) values (?, ?, ?, ?, ?)',
             [userName, password, question, answer,0])
            db.commit()
            flash('you have registered succesfuly')
            return redirect(url_for('login'))
        else:
            flash('user name already exists please try a new one')
            return redirect(url_for('register'))
def logUserOut():
    session.pop('logged_in', None)
    db = get_db()
    db.execute('update users set isLoggedIn=? where isLoggedIn=?',[0,1])
    db.commit()
    flash('You were logged out')
    return redirect(url_for('show_topics'))

def logUserIn():
    db = get_db()
    error = None
    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password']
        cur = db.execute('select username from users where userName=? and pass=?',[userName,password])
        user = cur.fetchall()
        if (len(user) == 0):
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            db.execute('update users set isLoggedIn=? where userName =?',[1,userName])
            db.commit()
            return redirect(url_for('show_topics'))
    return render_template('login.html', error=error)



from flaskr import *
