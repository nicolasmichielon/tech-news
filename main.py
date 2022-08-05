from flask import Flask, render_template, request, session, redirect, url_for, g
# Imports the list of dictionaries with news info
from db import grab_user_data, register_user, grab_user_by_id, save_post, grab_user_favorites, delete_post
import scrape
import importlib

app = Flask(__name__)
app.secret_key = 'verysecretkey'


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
        save_post(post_to_save, g.user[0])
        return ('', 204)
    return render_template("news.html", news=scrape.news)


@app.route("/reload")
def reload():
    importlib.reload(scrape)
    return redirect(url_for("news_page"))


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
        return ('', 204)
    return render_template("register.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == 'POST':
        post_to_delete = request.form['delete']
        delete_post(post_to_delete, g.user[0])
        return redirect(url_for('profile'))
    if not g.user:
        return redirect(url_for('login'))
    favorites = grab_user_favorites(session['user_id'])
    print(favorites)
    return render_template("profile.html", favorites=favorites)


@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect('login')
