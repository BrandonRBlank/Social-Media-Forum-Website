import sqlite3
from sqlite3 import Error


# Safe connect to db
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(str(e) + " in create_connection")
    return None


# Adds user to DB
def add_user(conn, username, password, isAdmin):
    # In this case, User has attributes specified, this is to skip inserting into id (which is autoincremented)
    sql = " INSERT INTO User(username,password,permission) VALUES(?,?,?) "
    cur = conn.cursor()

    cur.execute(sql, (username, password, isAdmin))
    conn.commit()
    return


# Creates post, and connecting tables
def add_post(conn, title, content, user_id, is_admin):
    sql_make_post = " INSERT INTO Post(title,content,score,is_admin) VALUES(?,?,?,?)"
    sql_make_makes = " INSERT INTO Makes VALUES(?,?) "
    sql_get_post_id = " SELECT id FROM Post ORDER BY id DESC LIMIT 1 "
    cur = conn.cursor()

    cur.execute(sql_make_post, (title, content, 0, is_admin))
    cur.execute(sql_get_post_id)
    post_id = cur.fetchone()[0]

    cur.execute(sql_make_makes, (post_id, user_id))

    conn.commit()
    return

# ----------------------------------------------------------------------------------------------------------------------


# Gets a single username
def get_user(conn, username):
    sql = " SELECT username FROM User WHERE username=? "
    cur = conn.cursor()

    # input has to be tuple, that's why (username,)
    cur.execute(sql, (username,))

    # If the fetchone() isn't subscriptable, then the item doesn't exist; in this case return 'None-type'
    try:
        return cur.fetchone()[0]
    except TypeError:
        return None


# Gets a single user id
def get_user_id(conn, username):
    sql = " SELECT id FROM User WHERE username=? "
    cur = conn.cursor()

    cur.execute(sql, (username,))
    try:
        return cur.fetchone()[0]
    except TypeError:
        return None


# Get user password
def get_user_pwd(conn, username, password):
    sql = " SELECT password FROM User WHERE username=? AND password=? "
    cur = conn.cursor()

    cur.execute(sql, (username, password))
    try:
        return cur.fetchone()[0]
    except TypeError:
        return None


# Get user permission
def get_admin_status(conn, username):
    sql = " SELECT permission FROM User WHERE username=? "
    cur = conn.cursor()

    cur.execute(sql, (username,))
    try:
        return cur.fetchone()[0]
    except TypeError:
        return None


# Gets all posts in DB
def get_posts(conn):
    sql = " SELECT id,title,content,score,is_admin FROM Post ORDER BY score DESC"
    cur = conn.cursor()

    cur.execute(sql)
    return cur.fetchall()


def get_post_score(conn, post_id):
    sql = " SELECT score FROM Post WHERE id=? "
    cur = conn.cursor()

    cur.execute(sql, (post_id,))
    return cur.fetchone()[0]


# Gets all post_ids that a user voted on
def get_user_votes(conn, user_id):
    sql = "SELECT P.id " \
          "FROM Post as P,User as U,Votes_On as V " \
          "WHERE U.id=V.user_id AND P.id=V.post_id AND V.vote=1 AND U.id=?"
    cur = conn.cursor()

    cur.execute(sql, (user_id,))
    return cur.fetchall()


def get_user_posts(conn, user_id):
    sql = "SELECT Post.id,Post.title,Post.content,Post.score " \
          "FROM Post, Makes, User " \
          "WHERE Post.id = Makes.post_id AND User.id = Makes.user_id AND User.id=?"
    cur = conn.cursor()

    cur.execute(sql, (user_id,))
    return cur.fetchall()


# ----------------------------------------------------------------------------------------------------------------------


# This will check if a user has voted on a post, if so returns False and calls a 401 error, bypassing returning ajax
# request and not allowing the post to be upvoted multiple times by the same person.
def set_post_score(conn, post_id, user_id):
    sql_check_user_vote = " SELECT post_id,user_id FROM Votes_On WHERE post_id=? AND user_id=? "
    sql_update_score = " UPDATE Post SET score=score+1 WHERE id=? "
    sql_make_votes_on = " INSERT INTO Votes_On VALUES(?,?,?)"
    cur = conn.cursor()

    cur.execute(sql_check_user_vote, (post_id, user_id))
    try:
        cur.fetchone()[0]
    except TypeError:
        cur.execute(sql_make_votes_on, (post_id, user_id, 1))
        cur.execute(sql_update_score, (post_id,))

        conn.commit()
        return True
    else:
        return False

# ----------------------------------------------------------------------------------------------------------------------


def remove_post(conn, post_id):
    sql = " DELETE FROM Post WHERE id=? "
    cur = conn.cursor()

    cur.execute(sql, (post_id,))
    conn.commit()
    return
