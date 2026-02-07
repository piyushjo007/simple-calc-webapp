# from flask import Flask, jsonify
import requests
import flask
app = flask.Flask(__name__)

@app.route("/<user>")
def get_gists(user):
    url = f"https://api.github.com/users/{user}/gists"
    response = requests.get(url)
    return flask.jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
