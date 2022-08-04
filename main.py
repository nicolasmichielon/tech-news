from flask import Flask, render_template, request, session, redirect, url_for, g
from numpy import save
# Imports the list of dictionaries with news info
from scrape import news
from db import grab_user_data, register_user, grab_user_by_id, save_post, grab_user_favorites
import requests

app = Flask(__name__)
app.secret_key = 'verysecretkey'

favorites = []


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user_data = grab_user_by_id(session['user_id'])
        g.user = user_data


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/news", methods=["GET", "POST"])
def news_page():
    if request.method == "POST":
        if not g.user:
            return redirect(url_for('login'))
        post_to_save = request.form['favorite']
        print(post_to_save)
        save_post(post_to_save, g.user[0])
        return redirect(url_for("profile"))
    return render_template("news.html", news=news)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        user_data = grab_user_data(username, password)
        if user_data:
            session['user_id'] = user_data[0]
            return redirect(url_for('profile'))
        return redirect(url_for('login'))
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        session.pop('user_id', None)
        register_user(request.form['username'], request.form['password'])
    return render_template("register.html")


@app.route("/profile")
def profile():
    if not g.user:
        return redirect(url_for('login'))
    favorites = grab_user_favorites(session['user_id'])
    print(favorites)
    return render_template("profile.html", favorites=favorites)
