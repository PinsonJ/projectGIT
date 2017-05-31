from flask import Flask, render_template
from DbClass import DbClass

app = Flask(__name__)


@app.route('/')
def index():

    return render_template('index.html')

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
    app.run()

#