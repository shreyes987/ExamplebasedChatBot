from flask import Flask, render_template, request, session
import match
import action
import diary
from spacy import load
import sqlite3
import os
import re
import csv
import random

app = Flask(__name__)
app.secret_key = "AQZXSWEDC"
nlp = load('en')
m = match.match(nlp)
ac = action.action(nlp)
d = diary.diary(nlp)

conn = sqlite3.connect('test.db')
connbio = sqlite3.connect('users/bio.db')

s_query = "SELECT id, name, pwd,public  from USER"

tex = [""]
act = ""
user = ""
entry = ""
date = ""
ans=[""]
dans =[""]
q_count = ["0"]
login_user = ""

@app.route('/')
def mainpage():
    global tex,act,user,entry,date,ans,dans,q_count
    tex = [""]
    act = ""
    user = ""
    entry = ""
    date = ""
    ans = [""]
    dans= [""]
    session["q"] = False
    q_count =["0"]
    try:
        return render_template("pro.html", tex=tex, act="", login=session["login"],user=session["user"])
    except:
        session["login"] = False
        return render_template("pro.html", tex=tex, act="",login=False)
@app.route('/login')
def login():
    ans=[""]
    return render_template("login.html")

@app.route('/login_data', methods=['POST'])
def login_data():
    user = request.form['user']
    pwd = request.form['pass']

    flag = False
    user_data = conn.execute(s_query)
    for row in user_data:
        print(row, user, pwd)
        if re.match(row[1], user) and re.match(row[2], pwd):
            flag = True
            break
    if flag == True:
        session["user"] = user
        session["login"] = True
        return render_template("pro.html",tex=tex,act="", login=session["login"], user=user)

    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    global tex, act, user, entry, date, ans,dans,q_count
    tex = [""]
    dans = [""]
    act = ""
    user = ""
    entry = ""
    date = ""
    ans = [""]
    session["login"] = False
    session["q"] = False
    q_count=["0"]
    return render_template("pro.html",tex=tex,act=act, login=False)

@app.route('/reg_data', methods=['POST'])
def reg_data():
    user = request.form['user']
    pwd = request.form['pass']
    email = request.form['email']
    flag = False
    user_data = conn.execute(s_query)
    for row in user_data:
        if re.match(row[1],user):
            flag = True
            break
    if flag == True:
        return render_template("login.html")
    else:
        os.mkdir("users/" + user)
        query = "INSERT INTO USER (Name,pwd) VALUES('" + user + "','" + pwd + "');"
        query1 = "INSERT INTO bio (user,email) values('"+user+"','"+email+"');"
        conn.execute(query)

        connbio.execute(query1)

        conndia = sqlite3.connect("users/"+user+"/diary.db")
        sql_q = '''
        create table diary(
        date VARCHAR (20),
        public int default 0,
        primary key (date)
        )
        '''
        conndia.execute(sql_q)
        conndia.commit()
        connbio.commit()
        conn.commit()

        print("hello")


        return render_template("login.html")

@app.route('/diary')
def diary():
    return render_template("diary.html")

@app.route('/diary_data', methods=['POST'])
def diary_data():
    entry = request.form['entry'].strip()
    date = request.form['date']
    user=session['user']
    with open("users/"+user+"/"+date+".txt","w") as f:
        f.write(entry)

    return render_template("diary.html", user=session['user'], entry=entry, date=date)

@app.route('/get_diary', methods=['POST'])
def get_diary():
    entry = request.form['entry'].strip()
    date = request.form['date']
    user = session['user']
    try:
        with open("users/"+user+"/"+date+".txt","r") as f:
            return render_template("diary.html", user=session['user'], entry=f.read(), date=date)
    except:
        return render_template("diary.html", user=session['user'], entry=entry, date=date,ans=ans)

@app.route('/knowledge')
def knowledge(ans=[""]):
    users=[]
    user_data = conn.execute(s_query)
    for row in user_data:
        print(row)
        if row[3] is 1 and not re.match(row[1],session['user']):
            users.append(row[1])
    userdata = []
    for r in users:
        r = "".join(r)
        s_que = "SELECT * from bio where user='" + r + "'"
        tab = connbio.execute(s_que)
        entry = []
        for l in tab:
            for t in l:
                if t is None:
                    entry.append("")
                else:
                    entry.append(t)
        userdata.append(entry)

    return render_template("knowledge.html",entry=userdata,ans=ans,act=ans[-1])

@app.route('/knowledge_data', methods=['POST'])
def knowledge_data():
    q = request.form['question']
    user = request.form['user']
    global ans
    try:
        dia = d.get_entries(user)
        ansa = d.loop_qs(q,dia)

        ans.append(session["user"]+": "+q)
        ans.append(user+": "+ansa)
    except Exception as e:
        print("---"+e)
        ans.append(session["user"]+": "+q)
        ans.append(user+": I don't know what you are talking about")
    return knowledge(ans)

@app.route('/question_data', methods=['POST'])
def question_data():
    q = request.form['question']
    user = session['user']
    try:
        dia = d.get_entries(user)
        ansa = d.loop_qs(q,dia)
        ans.append(session["user"]+": "+q)
        ans.append(user+": "+ansa)
    except:
        ans.append(session["user"]+": "+q)
        ans.append(user+": I don't know what you are talking about")
    return render_template("diary.html", ans=ans, user=session['user'], entry=entry, date=date)

@app.route('/form_data', methods=['POST'])
def form_data():
    global q_count,login_user
    inp = request.form['projectFilepath'].lower()

    if inp.lower() == "exit":
        q_count =["0"]
        session["q"] = False
        return render_template("pro.html",tex=tex, act="",login=session["login"],user=session["user"])

    if inp.lower() == "login":
        if session["login"] == False:
            session["q"] =True
            tex.append("YOU: "+inp)
            tex.append("AI: What is your UserName?")
            act = "What is your UserName?"
            q_count = ["1"]
            return render_template("pro.html",tex=tex, act=act,login=False)
        else:
            tex.append("YOU: "+inp)
            tex.append("AI: You are already logged in")
            act = "You are already logged in"
            return render_template("pro.html",tex=tex, act=act,login=session["login"],user=session["user"])

    elif session["q"] and q_count[0] == "1":
        login_user = inp
        try:
            q = list(connbio.execute("SELECT q0,q1,q2 from bio where user='" + inp + "'"))[0]
            a = list(connbio.execute("SELECT a0,a1,a2 from bio where user='" + inp + "'"))[0]
            q_count.pop(0)
            for i in range(0,3):
                q_count.append("q")
                q_count.append(q[i])
                q_count.append("a")
                q_count.append(a[i])
            print(q_count)
        except Exception as e:
            print(e)
            tex.append("YOU: "+inp)
            tex.append("AI: User does not exist")
            act = "User does not exist"
            return render_template("pro.html",tex=tex, act=act,login=False)
        blog = ""
        user_data = conn.execute("SELECT blog from USER where name='"+inp+"'")
        for row in user_data:
            blog=row[0]
        print("blog:" + str(blog))
        if blog == 0:
            session["q"] = False
            q_count = ["0"]
            tex.append("YOU: "+inp)
            tex.append("AI: You have not enabled this service.")
            act = "You have not enabled this service"
            return render_template("pro.html",tex=tex, act=act,login=False)

    if session["q"] and len(q_count)>0:
        if q_count[0] == "q":
            tex.append("YOU: "+ inp)
            tex.append("AI: " + q_count[1])
            act = q_count[1]
            q_count.pop(0)
            q_count.pop(0)
            return render_template("pro.html",tex=tex, act=act,login=False)
        elif q_count[0] == "a":
            if inp.lower() == q_count[1].lower():
                q_count.pop(0)
                q_count.pop(0)
                if len(q_count)>0:
                    tex.append("YOU: "+ inp)
                    tex.append("AI: " + q_count[1])
                    act = q_count[1]
                    q_count.pop(0)
                    q_count.pop(0)
                    return render_template("pro.html",tex=tex, act=act,login=False)
                else:
                    tex.append("YOU: "+ inp)
                    tex.append("AI: Successfully logged in")
                    act = "Successfully logged in"
                    session["q"] = False
                    session["login"] = True
                    session["user"] = login_user
                    return render_template("pro.html",tex=tex, act=act,user = session["user"],login=True)
            else:
                tex.append("You: "+ inp)
                tex.append("AI: Wrong Answer please re-enter your answer")
                act = "Wrong Answer please re-enter your answer"
                return render_template("pro.html",tex=tex, act=act,login=False)
    if inp.lower() == "go to diary":
        if session["login"] == True:
            return render_template("diary.html")
        else:
            tex.append("YOU: "+inp)
            tex.append("AI: Login first")
            act = "Login first"
            return render_template("pro.html",tex=tex, act=act,login=session["login"],user=session["user"])

    elif inp.lower() == "go to knowledge":
        if session["login"] == True:
            return render_template("knowledge.html")
        else:
            tex.append("YOU: "+inp)
            tex.append("AI: Login first")
            act = "Login first"
            return render_template("pro.html",tex=tex, act=act,login=session["login"],user=session["user"])

    elif inp.lower() == "go to login":
        if session["login"] == False:
            return render_template("login.html")
        else:
            tex.append("YOU: "+inp)
            tex.append("AI: You are already logged in")
            act = "You are already logged in"
            return render_template("pro.html",tex=tex, act=act,login=session["login"],user=session["user"])

    elif inp.lower() == "logout":
        if session["login"] == True:
            return logout()
        else:
            tex.append("YOU: "+inp)
            tex.append("AI: Login first")
            act = "Login first"
            return render_template("pro.html",tex=tex, act=act,login=session["login"],user=session["user"])

    elif inp.lower() == "goto biodata":
        if session["login"] == True:
            return render_template("bio.html")
        else:
            tex.append("YOU: "+inp)
            tex.append("AI: Login first")
            act = "Login first"
            return render_template("pro.html", tex=tex, act=act, login=session["login"],user=session["user"])

    elif inp.lower() == "goto settings":
        if session["login"] == True:
            return render_template("settings.html")
        else:
            tex.append("YOU: "+inp)
            tex.append("AI: Login first")
            act = "Login first"
            return render_template("pro.html", tex=tex, act=act, login=session["login"],user=session["user"])
    matches = m.find_match(inp.lower(),0.90)
    best_match = m.get_dominant_res(matches)
    act = ac.get_action(best_match,inp)
    if act is None:
        act = m.get_da(matches[2])
    if session["login"] is True:
        tex.append(session["user"] +": "+ inp)
    else:
        tex.append("YOU: " + inp)
    if act is not None:
        tex.append("AI: " + str(act))
    else:
        act = ""
    return render_template("pro.html", tex=tex, act=act,login=session["login"],user=session["user"])


@app.route('/bio')
def bio():
    s_query = "SELECT * from bio where user='"+session['user']+"'"

    tab = connbio.execute(s_query)
    entry=[]
    for l in tab:
        for t in l:
            if t is None:
                entry.append("")
            else:
                entry.append(t)

    print(entry)
    return render_template("bio.html", entry=entry,user=session['user'])


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

    connbio.execute("update bio set name='"+name+"',dob='"+dob+"',gender='"+gender+"',email='"+email+"',website='"+web+"',profession='"+prof+"',work='"+org+"',study='"+study+"',hobbies='"+hob+"' where user='" + session["user"] + "'")
    print("update bio set name='"+name+"',dob='"+dob+"',gender='"+gender+"',email='"+email+"',website='"+web+"',profession='"+prof+"',work='"+org+"',study='"+study+"',hobbies='"+hob+"' where user='" + session["user"] + "'")
    connbio.commit()

    s_query = "SELECT * from bio where user='" + session['user'] + "'"
    tab = connbio.execute(s_query)
    entry = []
    for l in tab:
        for t in l:
            if t is None:
                entry.append("")
            else:
                entry.append(t)

    return render_template("bio.html", entry=entry,user=session['user'])

@app.route('/settings')
def settings():
    user_data = conn.execute("SELECT id, name,pwd,public,blog from USER where name='"+session["user"]+"'")
    for row in user_data:
        public=row[3]
        blog = row[4]
    q = list(connbio.execute("SELECT q0,q1,q2 from bio where user='" + session["user"] + "'"))
    a = list(connbio.execute("SELECT a0,a1,a2 from bio where user='" + session["user"] + "'"))
    print(q,a)
    return render_template("settings.html",public=public,blog = blog, q=q[0], a=a[0])


@app.route('/settings_data', methods=['POST'])
def settings_data():
    for i in range(0,3):
        i = str(i)
        q = request.form['q'+i]
        a = request.form['a'+i]
        connbio.execute("update bio set q"+i+"='"+q+"' where user='" + session["user"] + "'")
        connbio.execute("update bio set a"+i+"='"+a+"' where user='" + session["user"] + "'")
        connbio.commit()
    try:
        pub = request.form['public']
        if re.match(pub,"on"):
            conn.execute("update USER set public=1 where name='" + session["user"] + "'")
            conn.commit()
    except:
        conn.execute("update USER set public=0 where name='" + session["user"] + "'")
        conn.commit()
    try:
        blog = request.form['blog']

        if re.match(blog,"on"):
            conn.execute("update USER set blog=1 where name='" + session["user"] + "'")
            conn.commit()
    except:
        conn.execute("update USER set blog=0 where name='" + session["user"] + "'")
        conn.commit()

    user_data = conn.execute("SELECT id, name, pwd,public,blog  from USER where name='" + session["user"] + "'")
    for row in user_data:
        public = row[3]
        blog = row[4]
    q = list(connbio.execute("SELECT q0,q1,q2 from bio where user='" + session["user"] + "'"))
    a = list(connbio.execute("SELECT a0,a1,a2 from bio where user='" + session["user"] + "'"))
    return render_template("settings.html",public=public, blog = blog, q=q[0], a=a[0])

if __name__ == '__main__':
    app.run()
