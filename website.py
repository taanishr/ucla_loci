import secrets
from flask import Flask, render_template, request, jsonify, session
from interface import load_data, compareCareers, stats

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = secrets.token_hex()

load_data()

# num_guesses = 5

answer = "Kareem Abdul-Jabbar"

@app.before_first_request
def setParameters():
    session["num_guesses"] = 5
    session["won"] = False


@app.route("/", methods=["POST", "GET"])
def index():
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
    # global num_guesses
    if request.method == 'POST':
        session["num_guesses"] = session["num_guesses"] - 1
    return jsonify({"num_guesses" : session["num_guesses"]})

@app.route("/retrieve_categories", methods=['GET'])
def retrieveCategories():
    return jsonify(stats)

@app.route("/reset", methods=['GET'])
def reset():
    # global num_guesses
    session["num_guesses"] = 5
    session["won"] = False
    return jsonify({"num_guesses" : session["num_guesses"]})
