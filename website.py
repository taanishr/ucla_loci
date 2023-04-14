from flask import Flask, render_template, request, jsonify, session
import secrets
import redis
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = secrets.token_hex()

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost/ucla"
db = SQLAlchemy(app)

r = redis.Redis()
answer = "Kareem Abdul-Jabbar" # use redis for this

@app.route("/", methods=["POST", "GET"])
def index():
    if (session.get("userID") == None):
        session["userID"] = secrets.token_hex(4)
        session.permanent = True
        r.mset({session["userID"]: 5})

    # # stat1 = db.select(Players.ppg).where(Players.player == "Kareem Abdul-Jabbar")
    # # res = db.session.execute(stat1)
    # # print(next(res)[0])
    # # for r in res:
    # #     print(r)

    # playerComparison = {}
    # compareStats(playerComparison, "Kareem Abdul-Jabbar", "Zach LaVine")
    # print(playerComparison)


    return render_template('index.html')

@app.route("/submit_guess", methods=['POST'])
def handleForm():
    guess = request.json['guess']
    playerComparison = compareCareers(guess, answer)
    return jsonify(playerComparison)
    # print(type(playerComparison))
    # print(playerComparison)
    # return ''

@app.route("/retrive_careers", methods=['GET'])
def retrieveCareers():
    careers = db.session.execute(db.select(Players.player))
    careerList = [career[0] for career in careers]
    res = jsonify({"careers": careerList})
    return res

@app.route("/num_guesses", methods=['POST', 'GET'])
def numGuesses():
    key = session["userID"]
    if (request.method == 'POST'):
        r.set(key, int(r.get(key))-1)
    return jsonify({"num_guesses": int(r.get(key))})
    

@app.route("/retrieve_categories", methods=['GET'])
def retrieveCategories():
    return jsonify(list(stats.keys()))

@app.route("/reset", methods=['GET'])
def reset():
    key = session["userID"]
    # r.set(key, 5)
    return jsonify({"num_guesses": int(r.get(key))})

class Players(db.Model):
    player = db.Column(db.VARCHAR, primary_key=True)
    ppg = db.Column(db.Float)
    rpg = db.Column(db.Float)
    apg = db.Column(db.Float)
    fg = db.Column(db.Float)
    tp = db.Column(db.Float)
    ft = db.Column(db.Float)
    
    def __repr__(self):
        return f'{self.player}'
    
def compareStat(stat, career1, career2):
    career1Stat = next(db.session.execute(db.select(stat).where(Players.player == career1)))[0]
    career2Stat = next(db.session.execute(db.select(stat).where(Players.player == career2)))[0]
    if (career1Stat == career2Stat):
          return {"value" : career1Stat, "equality" : 1}
    elif (career1Stat > career2Stat):
          return {"value" : career1Stat, "equality" : 2}
    else:
        return {"value" : career1Stat, "equality" : 0}
    
def compareStats(dict, career1, career2):
    for key, value in stats.items():
        dict[key] = compareStat(value, career1, career2)

def compareCareers(career1, career2):
    playerComparison = {}
    playerComparison["player"] = career1

    if (career1 == career2):
        playerComparison["answer"] = True
    else:
        playerComparison["answer"] = False

    compareStats(playerComparison, career1, career2)

    return playerComparison

stats = {"PPG": Players.ppg, "RPG": Players.rpg, "APG": Players.apg, "FG": Players.fg}