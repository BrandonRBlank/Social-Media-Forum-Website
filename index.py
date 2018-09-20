from flask import Flask, render_template, request, session, redirect, jsonify, abort
from db_funcs import *
from helpers import validate
import os

app = Flask(__name__)
app.debug = True

database = os.path.dirname(os.path.realpath(__file__)) + "/database/Data.db"
app.secret_key = '<YOUR SECRET KEY HERE>'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/', methods=['GET'])
def main():
    conn = create_connection(database)
    postsList = get_posts(conn)

    try:
        userVotes = get_user_votes(conn, session['id'])
        context = {
            'postsList': postsList,
            'username': session['username'],
            'userVotes': [element for vote in userVotes for element in vote]
        }
    except KeyError:
        context = {'postsList': postsList}
    return render_template('index.html', **context)


@app.route('/test')
def testing():
    conn = create_connection(database)
    listi = get_user_posts(conn, 1363)
    context = {
        'postsList': listi
    }
    return render_template('test.html', **context)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        validError = validate(request.form['username'], request.form['pwd'], database, "signup")

        if not validError:
            conn = create_connection(database)

            if request.form.get('admin') is None:
                admin = 0
            else:
                admin = 1

            add_user(conn, request.form['username'], request.form['pwd'], admin)

            session['logged_in'] = True
            session['username'] = request.form['username']
            session['id'] = get_user_id(conn, request.form['username'])
            session['is_admin'] = get_admin_status(conn, request.form['username'])

            return redirect('/')
        else:
            return render_template('signup.html', error=validError)
    elif request.method == 'GET':
        return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        validError = validate(request.form['username'], request.form['pwd'], database, "signin")

        if not validError:
            conn = create_connection(database)

            session['logged_in'] = True
            session['username'] = request.form['username']
            session['id'] = get_user_id(conn, request.form['username'])
            session['is_admin'] = get_admin_status(conn, request.form['username'])

            return redirect('/')
        else:
            return render_template('signin.html', error=validError)
    elif request.method == 'GET':
        return render_template('signin.html')


@app.route('/newpost', methods=['POST'])
def make_post():
    conn = create_connection(database)
    add_post(conn, request.form['title'], request.form['content'], session['id'], session['is_admin'])
    return redirect('/')


@app.route('/vote', methods=['POST'])
def upvote():
    conn = create_connection(database)
    post_id = int(request.json)

    if not set_post_score(conn, post_id, session['id']):
        abort(401)

    score = get_post_score(conn, post_id)
    return jsonify(score=str(score))


@app.route('/remove', methods=['POST'])
def remove():
    conn = create_connection(database)
    post_id = int(request.json)

    remove_post(conn, post_id)
    return "Ok"


@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['username'] = None
    session['id'] = None
    session['is_admin'] = None
    return redirect('/')


if __name__ == '__main__':
    app.run()
