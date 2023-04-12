from flask import Flask, render_template, request, jsonify, make_response
# from flask_session.__init__ import Session
# import secrets
# import redis
from interface import load_data, compareCareers, stats
import datetime

app = Flask(__name__, template_folder="templates", static_folder="static")

# r = redis.Redis()
# r.mset({"Guesses": 5})

load_data()

answer = "Kareem Abdul-Jabbar" # use redis for this

# @app.before_first_request
# def init():
#     resp = make_response()
#     resp.set_cookie('guesses', '5')
#     return resp

@app.route("/", methods=["POST", "GET"])
def index():
    resp = make_response(render_template('index.html'))
    # if ('guesses' not in request.cookies):
    if (True):
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=1, minutes=0, seconds=1500)
        # resp.set_cookie('expiry_date', f"{expire_date}", expires=expire_date)
        resp.set_cookie('guesses', '5', expires=expire_date)
    app.logger.info(request.cookies)
        
    return resp
    # return render_template('index.html')

@app.route("/submit_guess", methods=['POST'])
def handleForm():
    guess = request.json['guess']
    playerComparison = compareCareers(guess, answer)
    return jsonify(playerComparison)

@app.route("/retrive_careers", methods=['GET'])
def retrieveCareers():
    careers = jsonify(load_data.careers)
    return careers

# @app.route("/num_guesses", methods=['POST', 'GET'])
# def numGuesses():
#     # app.logger.info(r.get("Guesses"))
#     # if request.method == 'POST':
#     #     r.set("Guesses", int(r.get("Guesses")) - 1)
#     # return jsonify({"num_guesses": int(r.get("Guesses"))})
#     resp = make_response()
#     if request.method == 'POST':
#         resp.set_cookie('guesses', str(int(request.cookies.get('guesses')) - 1))
#     return jsonify({"num_guesses": request.cookies.get('guesses')})

@app.route("/retrieve_categories", methods=['GET'])
def retrieveCategories():
    return jsonify(stats)

@app.route("/reset", methods=['GET'])
def reset():
    # return jsonify({"num_guesses": int(r.get("Guesses"))})
    return jsonify({"num_guesses": request.cookies.get('guesses')})
