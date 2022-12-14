import sqlite3

conn = sqlite3.connect('users.sqlite')

cursor = conn.cursor()

# Create users and favorites table
sql_query = """ CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL,
    password text NOT NULL
)"""
cursor.execute(sql_query)

sql_query2 = """ CREATE TABLE IF NOT EXISTS favorites (
    title text NOT NULL,
    link text NOT NULL,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES user (user_id)
)"""
cursor.execute(sql_query2)
cursor.close()
# Returns user data if username and password are correct


def grab_user_pass(username):
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    user = cursor.execute(
        f"SELECT user_id, password FROM user WHERE username=?", (f'{username}',))
    user = user.fetchone()
    if user:
        return user
    return


def register_user(username, password):
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    query = f"""INSERT INTO user (username, password) VALUES (?, ?)"""
    cursor.execute(query, (f'{username}', f'{password}'))
    conn.commit()
    conn.close()
    return


def grab_user_by_id(id):
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    query = f"""SELECT * FROM user WHERE user_id = ?"""
    user = cursor.execute(query, (f'{id}',)).fetchone()
    conn.close()
    return user


def save_post(post, user_id):
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    post = post.split(',')
    query = f"""INSERT INTO favorites (user_id, title, link) VALUES (?, ?, ?)"""
    cursor.execute(
        query, (f'{user_id}', f'{post[0]}', f'{post[1]}'))
    conn.commit()
    conn.close()
    return


def grab_user_favorites(user_id):
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    query = f"""SELECT title, link FROM favorites WHERE user_id = ?"""
    favorites = cursor.execute(query, (f'{user_id}',)).fetchall()
    conn.close()
    return favorites


def delete_post(post, user_id):
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    query = """DELETE FROM favorites WHERE title = ? AND user_id = ?"""
    cursor.execute(query, (f'{post}', f'{user_id}'))
    conn.commit()
    conn.close()
    return


def check_if_username_already_exists(username):
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    query = """SELECT user_id FROM user WHERE username=?"""
    user = cursor.execute(query, (f'{username}',))
    user = user.fetchall()
    if len(user) == 0:
        return False
    return True
