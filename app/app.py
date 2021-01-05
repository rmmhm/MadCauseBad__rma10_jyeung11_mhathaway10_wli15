
#Team MadCauseBad - Ryan Ma, Jessica Yeung, May Hathaway, William Li
#SoftDev
#P0 : Da Art of Storytellin' (Pt.2)
#2021-01-08

from flask import Flask, render_template, request, session
import os

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("home.html") # directs user to home page

@app.route("/home", methods = ['GET', 'POST'])
def home():
    if("username" in session): # if user is already logged in, direct to user homepage
        return render_template('userhome.html', user = session["username"])
    if("gotologin" in session): # if login button is pressed, direct to login page
        return render_template('login.html')
    if("register" in session): # if register button is pressed, direct to register page
        return render_template('register.html')
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if("userlogin" in session): # if login button is pressed, check the following
        req = request.form
        if(request.form["pw"] == database_password) # checks if input password matches password in database associated with input username
            session["username"] = req["username"] # stores user info in cookies
            session["passw"] = req["passw"]
            return render_template("userhome.html", user = session["username"]) # directs user to user homepage on successful login
        else:
             return render_template('login.html', error = "Wrong Username or Password") # if user info does not match database info, reload page with error message
    if("username" in session): # if user is already logged in, direct to user homepage
        return render_template("userhome.html", user = session["username"])
    return render_template("login.html")

@app.route("/userhome", methods=['GET', 'POST'])
def userhome():
    if("logout" in session): # if logout button is pressed
        session.pop("username") # removes cookies upon logout
        session.pop("passw")
        return render_template("/home")
    return redirect("/") # if user tries to access userhome without being logged in, redirect to home

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if("signup" in session): # if register button is pressed, check the following
        req = request.form
        if(req["username"] not in database_username): # if username is unique, then store input info into database
            database_username += req["username"] # placeholder for database
            database_password += req["pw"]
            return render_template("login.html") # if register is successful, direct to login page
        else: # if not, reload page with error message
            return render_template("register.html", error = "Username already exists")
    return render_template("register.html")

if __name__ == "__main__":
    app.secret_key = os.urandom(32)
    app.debug = True
    app.run()
