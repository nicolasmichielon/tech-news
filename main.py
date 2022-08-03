from flask import Flask, render_template
# Imports the list of dictionaries with news info
from scrape import news

app = Flask(__name__)

favorites = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/news")
def news_page():
    return render_template("news.html", news=news)


@app.route("/profile")
def favorite_page():
    return render_template("profile.html", favorites=favorites)
