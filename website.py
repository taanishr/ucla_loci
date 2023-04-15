from flask import Flask, render_template, request, jsonify, session
import secrets
import redis
# from flask_sqlalchemy import SQLAlchemy
# import json
from interface import load_data, compareCareers, stats

app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = secrets.token_hex()

load_data()

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost/ucla"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# class Players(db.Model):
#     player = db.Column(db.VARCHAR, primary_key=True)
#     ppg = db.Column(db.Float)
#     rpg = db.Column(db.Float)
#     apg = db.Column(db.Float)
#     fg = db.Column(db.Float)
#     tp = db.Column(db.Float)
#     ft = db.Column(db.Float)

# stats = {"PPG": Players.ppg, "RPG": Players.rpg, "APG": Players.apg, "FG": Players.fg}

r = redis.Redis()
r.set('answer', str('Kareem Abdul-Jabbar'))

@app.route("/", methods=["POST", "GET"])
def index():
    if (session.get("userID") == None):
        session["userID"] = secrets.token_hex(4)
        session.permanent = True
        r.mset({session["userID"]: 5})
    return render_template('index.html')

@app.route("/submit_guess", methods=['POST'])
def handleForm():
    guess = request.json['guess']
    answer = str(r.get('answer'), 'utf-8')
    print(answer == "Kareem Abdul-Jabbar")
    playerComparison = compareCareers(guess, "Kareem Abdul-Jabbar")
    return jsonify(playerComparison)

@app.route("/retrive_careers", methods=['GET'])
def retrieveCareers():
    careers = jsonify(load_data.careers)
    return careers

@app.route("/num_guesses", methods=['POST', 'GET'])
def numGuesses():
    key = session["userID"]
    if (request.method == 'POST'):
        r.set(key, int(r.get(key))-1)
    return jsonify({"num_guesses": int(r.get(key))})

@app.route("/retrieve_categories", methods=['GET'])
def retrieveCategories():
    return jsonify(stats)

@app.route("/reset", methods=['GET'])
def reset():
    key = session["userID"]
    # r.set(key, 5)
    return jsonify({"num_guesses": int(r.get(key))})