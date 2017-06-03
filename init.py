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
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again'
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
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
        username = request.form['inputName']
        password = request.form['inputPassword']

        # validate the received values
        if  username and password:
            mysql.createUser(username,password)
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    return render_template('signup.html')

# @app.route('/collection')
# def collection():
#     Database = DbClass()
#     list_games = Database.getcollection()
#     return render_template('collection.html', collection=list_games)
#
# @app.route('/contact')
# def contact():
#     return render_template('contact.html')
#
# @app.route('/gamedetails/<gameid>')
# def gamedetails(gameid):
#     for game in gamedetails:
#         if gameid == game[0]:
#             gevondengame = game
#             return render_template("gamedetails.html", game=gevondengame)

@app.errorhandler(404)
def pagenotfound(error):
    return render_template("error.html", error=error)

if __name__ == '__main__':
    app.run(debug=True)

#