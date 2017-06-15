import os
from flask import Flask, render_template, redirect, url_for,request, session, flash, json
from DbClass import DbClass
from functools import wraps


app = Flask(__name__)
mysql = DbClass()
app.secret_key = "key"


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
@login_required
def index():

    return render_template('index.html')


@app.route('/login', methods = ['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
    #     if request.form['username'] != 'admin' or request.form['password'] != 'admin':
    #         error = 'Invalid credentials. Please try again'
    #         # flash(mysql.readUser())
    #     else:
    #         session['logged_in'] = True
    #         return redirect(url_for('index'))
    # return render_template('login.html', error=error)
    #
    # if 'username' in session:
    #     return redirect(url_for('index'))
        username = str(request.form['username'])
        password = str(request.form['password'])
        user = mysql.checkUser(username)
        if len(user) is 1:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials. Please try again'

    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return  redirect(url_for('index'))

@app.route('/signup', methods=['GET','POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = str(request.form['inputName'])
        password = str(request.form['inputPassword'])

        # validate the received values
        if  username and password:
            mysql.createUser(username,password)
            return redirect(url_for('login'))
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
        # if(mysql.checkuser(username)):
        #     error= 'This user already exists'
        # else:
        #     mysql.createUser(username,password)
        #     redirect(url_for('index'))

    return render_template('signup.html', error=error)

@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.errorhandler(404)
def pagenotfound(error):
    return render_template("error.html", error=error)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    host = "0.0.0.0"
    app.run(host=host, port=port,debug=True)
