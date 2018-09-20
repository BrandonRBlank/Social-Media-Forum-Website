from db_funcs import create_connection, get_user, get_user_pwd


def validate(username, password, database, validType):
    if not (password and username):
        return "You need to enter a username and password"
    if "\'" in (username or password):
        return "Disallowed character (\" \' \"  and \" - \" not allowed)"
    if "-" in (username or password):
        return "Disallowed character (\" \' \"  and \" - \" not allowed)"

    conn = create_connection(database)
    if validType == "signup":
        if username == get_user(conn, username):
            return "Username already taken"

    if validType == "signin":
        if not (username == get_user(conn, username)) or not (password == get_user_pwd(conn, username, password)):
            return "Username or password not correct"

    return False


# TODO: validate a post (title/content present; etc.)
def validate_post():
    pass
