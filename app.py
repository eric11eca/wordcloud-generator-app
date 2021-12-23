import base64
from io import BytesIO
import flask
import json
from flask import Flask, request, jsonify
from matplotlib.figure import Figure

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    return flask.render_template("index.html")


@app.route("/", methods=["POST"])
def update_record():
    text = json.loads(request.data)

    return jsonify(text)


def hello():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=105)
