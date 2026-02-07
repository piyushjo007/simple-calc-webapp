import time
import requests
import flask
import threading

app = flask.Flask(__name__)

READY = False
START_TIME = time.time()

def init_app():
    global READY
    time.sleep(60)  # Simulate initialization delay
    READY = True

@app.route("/startup")
def startup():
    if READY:
        return flask.jsonify(status="started"), 200
    return flask.jsonify(status="starting"), 503


@app.route("/health")
def health():
    # Liveness: process is running
    return flask.jsonify(status="ok"), 200


@app.route("/ready")
def readiness():
    # Readiness: app is ready to serve traffic
    if READY:
        return flask.jsonify(status="ready"), 200
    return flask.jsonify(status="not ready"), 503


@app.route("/live")
def liveness():
    # Optional: simulate crash detection logic
    uptime = time.time() - START_TIME
    return flask.jsonify(status="alive", uptime_seconds=int(uptime)), 200


@app.route("/<user>")
def get_gists(user):
    url = f"https://api.github.com/users/{user}/gists"
    response = requests.get(url)
    return flask.jsonify(response.json())


if __name__ == "__main__":
    # init_app()
    threading.Thread(target=init_app, daemon=True).start()

    app.run(host="0.0.0.0", port=8080)
