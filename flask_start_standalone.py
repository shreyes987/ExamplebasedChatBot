from flask import Flask, render_template,request,session
import match
import action
import diary
from spacy import load
import sqlite3
import os
import re

app = Flask(__name__)
app.secret_key = "AQZXSWEDC"
# nlp = load('en')
# m = match.match(nlp)
# a = action.action(nlp)
# d = diary.diary(nlp)

conn = sqlite3.connect('test.db')
s_query = "SELECT id, name, pwd  from USER"

tex = [""]
act = ""
user=""
entry=""
date=""

@app.route('/')
def mainpage():
    return render_template("pro.html",tex=tex,act=act,login=False)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    session["login"] = False
    return render_template("pro.html", login=False)

@app.route('/login_data', methods=['POST'])
def login_data():
    user = request.form['user']
    pwd = request.form['pass']

    flag = False
    user_data = conn.execute(s_query)
    for row in user_data:
        print(row,user,pwd)
        if re.match(row[1],user) and re.match(row[2],pwd):
            flag = True
            break
    if flag == True:
        session["user"] = user;
        return render_template("pro.html", login=True, user=user)

    else:
        return render_template("login.html")

@app.route('/reg')
def reg():
    return render_template("reg.html")

@app.route('/reg_data', methods=['POST'])
def reg_data():
    user = request.form['user']
    pwd = request.form['pass']
    flag = False
    user_data = conn.execute(s_query)
    for row in user_data:
        if row[1] is user:
            flag = True
            break
    if flag == True:
            return render_template("reg.html")
    else:
        query = "INSERT INTO USER (Name,pwd) VALUES('" + user + "','" + pwd + "');"
        conn.execute(query)
        conn.commit()
        print("hello")
        os.mkdir("users/" + user)
        return render_template("login.html")

@app.route('/diary')
def diary():
    return render_template("diary.html")


@app.route('/diary_data', methods=['POST'])
def diary_data():
    entry = request.form['entry'].strip()
    date = request.form['date']
    # tuple = d.diary_to_tuple(entry)
    # d.print_tuple_to_file(tuple,user,date)
    # dia = d.create_diary(user,date)
    # print(dia)
    # d.add_new_verbs(dia)
    return render_template("diary.html",user=session['user'],entry=entry,date=date)

@app.route('/question_data', methods=['POST'])
def question_data():
    q = request.form['question']
    ans=""
    # dia = d.create_diary()
    # ans = d.retrieve_from_diary(q,dia)
    return render_template("diary.html",ans=ans, user=session['user'], entry=entry, date=date)


@app.route('/form_data', methods=['POST'])
def form_data():
    inp = request.form['projectFilepath']
    # matches = m.find_match(inp.lower())
    # best_match = m.get_dominant_res(matches)
    # act = a.get_action(best_match,inp)

    tex.append("YOU: " + inp)
    # if act is not None:
    #     tex.append("AI: " + act)
    # else:
    #     act = ""
    return render_template("pro.html",tex = tex, act=act)

@app.route('/bio')
def bio():
    return render_template("bio.html",user=session['user'])

@app.route('/bio_data', methods=['POST'])
def bio_data():
    name = request.form['name']
    dob = request.form['dob']
    gender = request.form['gender']
    email = request.form['email']
    web = request.form['web']
    prof = request.form['prof']
    org = request.form['org']
    study = request.form['study']
    hob = request.form['hob']


if __name__ == '__main__':
    app.run()
