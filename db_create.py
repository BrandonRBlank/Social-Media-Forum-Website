import sqlite3

database = "database/Data.db"
conn = sqlite3.connect(database)

sql_create_user = """ CREATE TABLE IF NOT EXISTS User (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT,
                                password TEXT,
                                permission INTEGER); """

sql_create_post = """ CREATE TABLE IF NOT EXISTS Post (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT,
                                content TEXT,
                                score INTEGER); """

sql_create_votes_on = """ CREATE TABLE IF NOT EXISTS Votes_On (
                                post_id INTEGER,
                                user_id INTEGER,
                                vote INTEGER); """

sql_create_makes = """ CREATE TABLE IF NOT EXISTS Makes (
                                post_id INTEGER,
                                user_id INTEGER); """

conn.execute(sql_create_user)
conn.execute(sql_create_post)
conn.execute(sql_create_votes_on)
conn.execute(sql_create_makes)
