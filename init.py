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

    return redirect('dashboard')


@app.route('/login', methods = ['GET','POST'])
def login():
    error = None
    if request.method == 'POST':

        username = str(request.form['username'])
        password = str(request.form['password'])

        user = mysql.checkUser(username, password)
        # pas = mysql.checkPassword(password)
        if (len(user) != 1):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials. Please try again'
            return redirect(url_for('login'))

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



    return render_template('signup.html', error=error)

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    if request.method == 'GET':
        temperature= mysql.getLatestTemperature()

        humidity= mysql.getLatestHumidity()

        pressure= mysql.getLatestPressure()

        rain = mysql.getLatestRainsensor()

        light = mysql.getLatestLight()

        timestamp = mysql.getLatestTimestamp()

        return render_template('dashboard.html',temperature=temperature,humidity=humidity,rain = rain,pressure=pressure,light=light,timestamp=timestamp)

@app.route('/chart')
@login_required
def chart():
    temperature = mysql.getLast60tempdata()
    timestamp = mysql.getLast60timedata()
    humidity = mysql.getLast60humdata()
    pressure = mysql.getLast60presdata()
    return render_template('chart.html',temperature=temperature, timestamp=timestamp, humidity = humidity, pressure=pressure)

@app.errorhandler(404)
def pagenotfound(error):
    return render_template("error.html", error=error)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    host = "0.0.0.0"
    app.run(host=host, port=port, debug=True)
