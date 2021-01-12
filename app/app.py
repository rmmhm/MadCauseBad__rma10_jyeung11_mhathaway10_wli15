#Team MadCauseBad - Ryan Ma, Jessica Yeung, May Hathaway, William Li
#SoftDev
#P0 : Da Art of Storytellin' (Pt.2)
#2021-01-08

from flask import Flask, render_template, request, session, redirect

import os
import sqlite3

from dbfunctions import *

app = Flask(__name__)

createTables()

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

        if verifyLogin(request.form["username"], request.form["passw"]):
            session["username"] = request.form["username"]
            session["passw"] = request.form["passw"]
            return redirect("/userhome") # directs user to user homepage on successful login

        else:
            return render_template('login.html', error = "Could not authenticate")        #pass doesnt match with user

    if("username" in session): # if user is already logged in, direct to user homepage
        return redirect("/userhome")

    return render_template("login.html")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if("signup" in request.form): # if register button is pressed, check the following
        if(not(checkUser(request.form['username']))):
            insertUserData(request.form['username'],request.form['passw'])
            return redirect("/login")
        return render_template("register.html", error="Username already exists.")
    return render_template("register.html")

@app.route("/userhome", methods=['GET', 'POST'])
def userhome():
    if("username" in session):

        if("myblog" in request.form): # check if the my blog button is pressed
            if(checkBlog(getId(session["username"]))): # check if the user has a blog
                return redirect("/userhome/" + session["username"])
            return render_template("userhome.html", message = "No blog created")

        if("createblog" in request.form):
            if(not(checkBlog(getId(session["username"])))):
                createBlog(getId(session["username"]), session["username"], request.form["blogtitle"])
                message = "Blog Created"
            else:
                message = "Limited to one"
            return render_template("userhome.html", message = message)

        if("logout" in request.form): # if logout button is pressed
            session.pop("username") # removes cookies upon logout
            session.pop("passw")
            return redirect("/home")

        return render_template("userhome.html", user = session["username"])
    return redirect("/")

@app.route("/browse", methods = ['GET', 'POST'])
def browse():
    if("username" in session):
        return render_template("browse.html", blogs = getBlogs())
    return redirect("/")

@app.route("/userhome/<string:username>", methods = ['GET', 'POST'])
def blog(username):
    if("username" in session):

        if(not(checkUser(username))): # does the username exist, if not, display error page
            return render_template("dne.html", user = username)
        entries = getEntries(getId(username))
        creator = session["username"] == username # check if the person on the page is the creator of the blog

        if("create" in request.form):
            createEntry(getId(username), request.form["entrytitle"], request.form["entrytext"])
            return render_template("blog.html", title = getBlogTitle(getId(username)), user = username, entries = getEntries(getId(username)), creator = creator, url = "/userhome/" + username)

        if(len(entries) == 0): # check if entries exist for the blog
            return render_template("blog.html", title = getBlogTitle(getId(username)), user = username, creator = creator, url = "/userhome/" + username, error = "No entries yet")

        if("edit" in request.form):
            editEntry(request.form["eid"], request.form["edittitle"], request.form["edittext"])
            return render_template("blog.html", title = getBlogTitle(getId(username)), user = username, entries = getEntries(getId(username)), creator = creator, url = "/userhome/" + username)

        if("delete" in request.form):
            deleteEntry(request.form["eid"])
            return render_template("blog.html", title = getBlogTitle(getId(username)), user = username, entries = getEntries(getId(username)), creator = creator, url = "/userhome/" + username)

        return render_template("blog.html", title = getBlogTitle(getId(username)), user = username, entries = getEntries(getId(username)), creator = creator, url = "/userhome/" + username)
    return redirect("/")


if __name__ == "__main__":
    app.secret_key = os.urandom(32)
    app.debug = True
    app.run()
