from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import redis
import secrets
from datetime import timedelta

app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = secrets.token_hex()

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost/ucla"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Players(db.Model):
    player = db.Column(db.VARCHAR, primary_key=True)
    ppg = db.Column(db.Float)
    rpg = db.Column(db.Float)
    apg = db.Column(db.Float)
    fg = db.Column(db.Float)
    tp = db.Column(db.Float)
    ft = db.Column(db.Float)

r = redis.Redis()
r.set('answer', str('Kareem Abdul-Jabbar'))
r.set('won', "0")
r.hset("stats", "0", "ppg")
r.hset("stats", "1", "rpg")
r.hset("stats", "2", "apg")
r.hset("stats", "3", "fg")

@app.route("/", methods=["POST", "GET"])
def index():
    if (session.get("userID") == None):
        session["userID"] = secrets.token_hex(4)
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=5)
        r.mset({session["userID"]: 5, 'won': 0, 'new_session': 1})
    else:
        r.set('new_session', 0)

    return render_template('index.html')

@app.route("/submit_guess", methods=['POST'])
def handleForm():
    guess = request.json['guess']
    answer = str(r.get('answer'), 'utf-8')
    playerComparison = compareCareers(guess, answer)
    return jsonify(playerComparison)

@app.route("/retrive_careers", methods=['GET'])
def retrieveCareers():
    q1 = db.select(Players.player)
    careers = [value[0] for value in db.session.execute(q1)]
    return jsonify({"careers": careers})

@app.route("/num_guesses", methods=['POST', 'GET'])
def numGuesses():
    key = session["userID"]
    if (request.method == 'POST'):
        r.set(key, int(r.get(key))-1)
    return jsonify({"num_guesses": int(r.get(key))})

@app.route("/retrieve_categories", methods=['GET'])
def retrieveCategories():
    stats = [str(value, 'utf-8') for value in r.hgetall("stats").values()]
    return jsonify(stats)

@app.route("/reset", methods=['GET'])
def reset():
    key = session["userID"]
    new_session = bool(int(r.get("new_session")))
    print(new_session)
    return jsonify({"num_guesses": int(r.get(key)), "new_session": new_session})

@app.route("/win_cond", methods=['Get'])
def checkWinCondition():
    key = session["userID"]
    state = {}

    if (int(r.get('won'))):
        state = {"num_guesses": int(r.get(key)), "won": True, "answer": str(r.get('answer'), 'utf-8')}
    else:
        state = {"num_guesses": int(r.get(key)), "won": False, "answer": str(r.get('answer'), 'utf-8')}

    return jsonify(state)

# after this is compare stat stuff
def compareStat(stat, career1, career2):
    career1Stat = 0
    career2Stat = 0

    q1 = db.select(getattr(Players, stat)).where(getattr(Players, "player") == career1)
    q2 = db.select(getattr(Players, stat)).where(getattr(Players, "player") == career2)
    for v in db.session.execute(q1):
        career1Stat = v[0]
    for v in db.session.execute(q2):
        career2Stat = v[0]

    if (career1Stat == career2Stat):
        return {"value" : career1Stat, "equality" : 1}
    elif (career1Stat > career2Stat):
        return {"value" : career1Stat, "equality" : 2}
    else:
        return {"value" : career1Stat, "equality" : 0}

def compareStats(dict, career1, career2):
    stats = [str(value, 'utf-8') for value in r.hgetall("stats").values()]
    for stat in stats:
        dict[stat] = compareStat(stat, career1, career2)
     
def compareCareers(career1, career2):
    playerComparison = {}
    playerComparison["player"] = career1

    if (career1 == career2):
        playerComparison["answer"] = True
        r.set("won", "1")
    else:
        playerComparison["answer"] = False

    compareStats(playerComparison, career1, career2)

    return playerComparison