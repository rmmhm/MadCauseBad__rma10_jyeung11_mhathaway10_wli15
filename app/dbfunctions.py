import sqlite3
import csv
DB_FILE="userinfo.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

def createTables():
	c.execute("CREATE TABLE IF NOT EXISTS userInfo (Username TEXT, Password TEXT, id INTEGER PRIMARY KEY)")
	c.execute("CREATE TABLE IF NOT EXISTS Uentries (id INTEGER, title TEXT, entry TEXT)")
	c.execute("CREATE TABLE IF NOT EXISTS Ublogs (id INTEGER, title TEXT)")


def insertUserData(userN, passW, id):     #when given data, it inerts into the database/create it
	insert = "INSERT INTO userInfo (Username, Password, id) VALUES (?, ?, ?);"
	data = (userN, passW, id)
	c.execute(insert, data)

def verifyLogin(username, password):	#gives user and pass to check if the info match
	userN=username
	passW=password
	c.execute("SELECT * FROM userInfo")
	data = c.fetchall()
	for row in data:
		userArray=row
		if(userArray[0]==userN):
			print("correct user")
			if(userArray[1]==passW):
				print("correct password")
				return True
	return False

def createBlog(userID, title):
	data=(userID, title)
	insert = "INSERT INTO Ublogs (id, title) VALUES (?, ?);"
	c.execute(insert, data)

def createEntry(userID, title, entry):
	data=(userID, title, entry)
	insert = "INSERT INTO Uentries (id, title, entry) VALUES (?, ?, ?);"
	c.execute(insert, data)

def editEntry(userID, title, revisedEntry):
	user=userID
	entryTitle=title
	c.execute('DELETE FROM Uentries WHERE id=? AND title=?', (user, entryTitle)) 
	newEntry=revisedEntry
	createEntry(user, entryTitle, newEntry)
def getBlogTitle(userID):
	user=userID
	c.execute('SELECT * FROM Ublogs WHERE id=?', (user,))
	data=c.fetchall()
	print(data[0][1])
	return data[0][1]
def getEntries(userID):
	user=userID
	c.execute('SELECT * FROM Uentries WHERE id=?', (user,))
	data=c.fetchall()
	return data
	#bigStr=""
	#i=0
	#for row in data:
	#	bigStr += data[i][1]
	#	bigStr += "-"
	#	bigStr += data[i][2]
	#	bigStr += "\n"
	#	i+=1
	#print(bigStr)
	#return bigStr
def getId(userN):
	user = userN
	c.execute('SELECT * FROM userinfo WHERE Username=?', (user,))
	uId=c.fetchall()
	print(uId[0][2])
	return uId[0][2]
def checkUser(userN):
	user=userN
	c.execute("SELECT * FROM userInfo")
	data = c.fetchall()
	for row in data:
		userArray=row
		if(userArray[0]==user):
			print("existing user")
			return True
	print("no user")
	return False

def getBlogs():			
	c.execute('SELECT * FROM Ublogs')
	blogs=c.fetchall()
	return blogs

def checkBlog(userID):
	user=userID
	c.execute("SELECT * FROM Ublogs")
	data = c.fetchall()
	for row in data:
		userArray=row
		if(userArray[0]==user):
			return True
	return False
#createTables()
#insertUserData("william", "Li", 12)
#verifyLogin("cat", "Li")
