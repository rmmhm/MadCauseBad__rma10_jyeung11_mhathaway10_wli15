#Team MadCauseBad - Ryan Ma, Jessica Yeung, May Hathaway, William Li
#SoftDev
#P0 : Da Art of Storytellin' (Pt.2)
#2021-01-08

from flask import Flask, render_template, request, session

import os
import sqlite3

from dbfunctions import insert_login_data
from dbfunctions import publish_draft, save_draft
from dbfunctions import publish_blog, spit_blog

app = Flask(__name__)

DB_FILE="userinfo.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXISTS userInfo (Username TEXT, Password TEXT, id INTEGER PRIMARY KEY)")

@app.route("/")
def landing():
    return redirect("/home") # directs user to home page

@app.route("/home", methods = ['GET', 'POST'])
def home():
    if("username" in request.form): # if user is already logged in, direct to user homepage
        return redirect('/userhome')
    if("gotologin" in request.form): # if login button is pressed, direct to login page
        return redirect('/login')
    if("register" in request.form): # if register button is pressed, direct to register page
        return redirect('/register')
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if("userlogin" in request.form): # if login button is pressed, check the following
        req = request.form
        accounts_db = c.execute("SELECT * FROM userInfo")
        for row in accounts_db:
            userArray = row             #creates arrays of every row in db to check if the pairing exist
            if(userArray[0] == req["username"]):        #if user matches
                if(userArray[1] == req["passw"]):       #if pass matches with user
                    session["username"] = req["username"] # stores user info in cookies
                    session["passw"] = req["passw"]
                    print (userArray + " " + "TEST")
                    return redirect("/userhome") # directs user to user homepage on successful login
                else:
                    return render_template('login.html', error = "Password")        #pass doesnt match with user
        return render_template('login.html', error = "Username does not exist")      #no record of username

    if("username" in session): # if user is already logged in, direct to user homepage
        return redirect("/userhome")
    return render_template("login.html")

@app.route("/userhome", methods=['GET', 'POST'])
def userhome():
    if("logout" in session): # if logout button is pressed
        session.pop("username") # removes cookies upon logout
        session.pop("passw")
        return redirect("/home")
    return render_template("userhome.html", user = session["username"])

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if("signup" in session): # if register button is pressed, check the following
        req = request.form

        accounts_db = c.execute("SELECT * FROM userInfo")

        i=0
        for row in accounts_db:
            i+=1
            userArray = row
            if(userArray[0] == req["username"]):                #when the username already exists
                return render_template("register.html", error = "Username already exists")
        userN = req["username"]
        passW= req["pw"]
        id = i
        data = (userN, passW, id)
        insert = "INSERT INTO userInfo (Username, Password, id) VALUES (?, ?, ?);" #if username is unique, then store input info into database
        c.execute(insert, data)
        return redirect("/login.html") # if register is successful, direct to login page
    return render_template("register.html")

if __name__ == "__main__":
    app.secret_key = os.urandom(32)
    app.debug = True
    app.run()
