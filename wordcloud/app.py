import base64
import flask
import json

from io import BytesIO
from flask import Flask, request, jsonify
from matplotlib.figure import Figure
from wordcloud import WordCloud
from wordcloud import STOPWORDS
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    return flask.render_template("index.html")


def similar_color_func(
        word=None, font_size=None,
        position=None, orientation=None,
        font_path=None, random_state=None):
    h = 40  # 0 - 360
    s = 100  # 0 - 100
    l = random_state.randint(30, 70)  # 0 - 100
    return "hsl({}, {}%, {}%)".format(h, s, l)


def multi_color_func(
        word=None, font_size=None,
        position=None, orientation=None,
        font_path=None, random_state=None):
    colors = [
        [4, 77, 82],
        [25, 74, 85],
        [82, 43, 84],
        [158, 48, 79]
    ]
    rand = random_state.randint(0, len(colors) - 1)
    return "hsl({}, {}%, {}%)".format(colors[rand][0], colors[rand][1], colors[rand][2])


mask_map = {
    "africa": "./masks/africa.jpeg",
    "cross": "./masks/cross.jpg",
    "dove": "./masks/dove.jpg",
    "music": "./masks/music2.jpg",
    "texas": "./masks/texas.png",
    "usa": "./masks/US.png"
}


@app.route("/generate", methods=["POST"])
def update_record():
    generate_info = json.loads(
        request.get_data().decode('utf8').replace("'", '"'))
    mask_pth = generate_info['mask']
    mask = np.array(Image.open(mask_map[mask_pth]))
    cmap = generate_info['cmap']
    wc = WordCloud(
        stopwords=STOPWORDS,
        mask=mask, background_color="white",
        max_words=1000, max_font_size=256,
        random_state=42, width=mask.shape[1],
        height=mask.shape[0], colormap=plt.get_cmap(cmap)
    )
    text = generate_info['text']
    wc.generate(text)
    img = wc.to_image()
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    data = base64.b64encode(byte_io.getbuffer()).decode("ascii")
    return f"<img id='cloud' src='data:image/png;base64,{data}'/>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=105)
