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
    votes INTEGER NOT NULL,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES user (user_id)
)"""
cursor.execute(sql_query2)
cursor.close()
# Returns user data if username and password are correct


def grab_user_data(username, password):
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    user = cursor.execute(
        f"SELECT user_id, password FROM user WHERE username='{username}'")
    user = user.fetchone()
    print(user)
    if user and password == user[1]:
        return user
    return


def register_user(username, password):
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    query = f"""INSERT INTO user (username, password) VALUES ('{username}', '{password}')"""
    cursor.execute(query)
    conn.commit()
    print(f"Usuario {username} de senha {password} foi cadastrado")
    conn.close()
    return


def grab_user_by_id(id):
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    query = f"""SELECT * FROM user WHERE user_id = {id} """
    user = cursor.execute(query).fetchone()
    conn.close()
    return user


def save_post(post, user_id):
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    post = post.split(',')
    query = f"""INSERT INTO favorites (user_id, title, link, votes) VALUES ({user_id}, '{post[0]}', '{post[1]}', '{post[2]}')"""
    cursor.execute(query)
    conn.commit()
    conn.close()
    return


def grab_user_favorites(user_id):
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    query = f"""SELECT title, link, votes FROM favorites WHERE user_id = {user_id}"""
    favorites = cursor.execute(query).fetchall()
    conn.close()
    return favorites
