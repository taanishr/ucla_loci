from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index(methods=["POST", "GET"]):
    request.form("guess")
    return render_template('index.html')
