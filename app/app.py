#Team MadCauseBad - Ryan Ma, Jessica Yeung, May Hathaway, William Li
#SoftDev
#P0 : Da Art of Storytellin' (Pt.2)
#2021-01-08

from flask import Flask, render_template, request, session, redirect

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

        if(verifyLogin(request.form["username"], request.form["passw"])):

            #insert user data to database

            session["username"] = request.form["username"]
            session["passw"] = request.form["passw"]
            return redirect("/userhome") # directs user to user homepage on successful login
        else:
            return render_template('login.html', error = "Password")        #pass doesnt match with user
        return render_template('login.html', error = "Username does not exist")      #no record of username
    if("username" in session): # if user is already logged in, direct to user homepage
        return redirect("/userhome")
    return render_template("login.html")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if("signup" in session): # if register button is pressed, check the following

        # placeholder for checking if registration username is unique and for inserting user data into database upon successful registration

        return redirect("/login.html")
    return render_template("register.html")

@app.route("/userhome", methods=['GET', 'POST'])
def userhome():
    if("username" in session);
        if("myblog" in request.form):
            return redirect("/userhome/" + session["username"])
        if("createblog" in request.form && checkBlog(getId(session["username"]))): # checks if that user already has a blog
            return render_template("userhome.html", message = "Blog Created")
        else:
            return render_template("userhome.html", message = "Limited to one blog")
        if("logout" in request.form): # if logout button is pressed
            session.pop("username") # removes cookies upon logout
            session.pop("passw")
            return redirect("/home")
        return render_template("userhome.html", user = session["username"])
    return redirect("/")

@app.route("/browse", methods = ['GET', 'POST'])
def browse():
    if("username" in session):
        if("blog" in request.form):
            return redirect("/userhome/" + request.form["username"])
        return render_template("browse.html", blogs = getBlogs()) # getBlogs
    return redirect("/")

@app.route("/userhome/<string:username>", methods = ['GET', 'POST'])
def blog(username):
    if("username" in session):
        entries = getEntries(getId(username)) # getEntries
        if(!checkUser()): # does the username exist, if not, display error page
            return render_template("dne.html", user = username)
        creator = session["username"] == username
        if("create" in request.form):
            createEntry(request.form["title"], request.form["entrytext"]) # createEntry
            return render_template("blog.html", title = getBlogTitle(getId(username)), user = username, entry = getEntries(getId(username)), creator = creator, url = "/userhome/" + username)
        if("edit" in request.form):
            return redirect("/userhome/" + username + "/edit")
        return render_template("blog.html", title = getBlogTitle(getId(username)), user = username, entry = getEntries(getId(username)), creator = creator, url = "/userhome/" + username)
    return redirect("/")

@app.route("/userhome/<string:username>/edit", methods = ['GET', 'POST'])
def edit(username):
    if("username" in session):
        if(session["username"] == username):
            if("edit" in request.form):
                editEntry(getId(request.form["username"]), request.form["entrytitle"], request.form["entrytext"]) # editEntry
                return render_template("edit.html", message = "Edit successful", entries = getEntries(getId(username))) # getEntries
            if("back" in request.form):
                return redirect("/userhome/" + username)
            return render_template("edit.html", entries = getEntries(getId(username))) # getEntries
        return redirect("/userhome/" + username)
    return redirect("/")

if __name__ == "__main__":
    app.secret_key = os.urandom(32)
    app.debug = True
    app.run()
