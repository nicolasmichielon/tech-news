from flask import Flask, render_template
from scrape import news

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/news")
def news_page():
    return render_template("news.html", news=news)
