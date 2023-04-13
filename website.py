from flask import Flask, render_template, request, jsonify, session
from interface import load_data, compareCareers, stats
import secrets
import redis

app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = secrets.token_hex()

r = redis.Redis()

load_data()

answer = "Kareem Abdul-Jabbar" # use redis for this

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
    playerComparison = compareCareers(guess, answer)
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
