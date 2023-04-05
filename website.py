from flask import Flask, render_template, request, jsonify
from interface import load_data, compareCareerStat

app = Flask(__name__, template_folder="templates", static_folder="static")

load_data()

num_guesses = 5

stats = ["PPG", "RPG", "APG", "FG%"]

answer = "Kareem Abdul-Jabbar"

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
    global num_guesses
    if request.method == 'POST':
        num_guesses = num_guesses - 1
    return jsonify({"num_guesses" : num_guesses})

@app.route("/reset", methods=['GET'])
def reset():
    global num_guesses
    num_guesses = 5
    return jsonify({"num_guesses" : num_guesses})

def compareCareers(career1, career2):
    playerComparison = {}
    for stat in stats:
        playerComparison[stat] = compareCareerStat(career1, career2, stat)
    return playerComparison
      
def checkAnswer(career1, career2):
    if (career1 == career2):
        return True
    else:
        return False