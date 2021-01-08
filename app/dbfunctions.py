import sqlite3
import csv

# replace this with database instances in the functions
DB_FILE="userinfo.db"
# these should  be deleted
db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

# instead of using c = db.cursor()
# at the beginning of each function do
# instance = database()
# and reference the cursor with
# instance.cursor. or instance.db
# make sure to instance.db.commit() when changing a table's contents (createBlog, createEntry, editEntry)

class database:
    def __init__(self, file=DB_FILE):
        self.db = sqlite3.connect(file, check_same_thread=False)
        self.cursor = self.db.cursor()

    def close(self):
        self.cursor.close()
        self.db.close()

    def __del__(self):
        self.close()

def createTables():
    instance = database()

    instance.cursor.execute("CREATE TABLE IF NOT EXISTS userInfo (Username TEXT, Password TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)")
    instance.cursor.execute("CREATE TABLE IF NOT EXISTS Uentries (id INTEGER, title TEXT, entry TEXT)")
    instance.cursor.execute("CREATE TABLE IF NOT EXISTS Ublogs (id INTEGER, title TEXT)")

    instance.db.commit()


def insertUserData(userN, passW):
    """ when given data, it inerts into the database/create it """
    instance = database()
    print(userN + ", " + passW)
    instance.cursor.execute("INSERT INTO userInfo (Username, Password) VALUES (?, ?)", (userN, passW))
    instance.db.commit()

def verifyLogin(username, password):
    """ gives user and pass to check if the info match """
    instance = database()
    data = instance.cursor.execute("SELECT COUNT(*) FROM userInfo WHERE Username=? AND Password=?", (username, password) ).fetchone()[0]

    return data == 1

def createBlog(userID, title):
	instance = database()
	data=(userID, title)
	insert = "INSERT INTO Ublogs (id, title) VALUES (?, ?);"
	instance.cursor.execute(insert, data)
	instance.db.commit()
def createEntry(userID, title, entry):
	instance = database()
	data=(userID, title, entry)
	insert = "INSERT INTO Uentries (id, title, entry) VALUES (?, ?, ?);"
	instance.cursor.execute(insert, data)
	instance.db.commit()
def editEntry(userID, title, revisedEntry):
	instance = database()
	user=userID
	entryTitle=title
	instance.cursor.execute('DELETE FROM Uentries WHERE id=? AND title=?', (user, entryTitle))
	newEntry=revisedEntry
	createEntry(user, entryTitle, newEntry)
	instance.db.commit()
def getBlogTitle(userID):
	instance = database()
	user=userID
	instance.cursor.execute('SELECT * FROM Ublogs WHERE id=?', (user,))
	data=instance.cursor.fetchall()
	#print(data[0][1])
	return data
def getEntries(userID):
	instance = database()
	user=userID
	instance.cursor.execute('SELECT * FROM Uentries WHERE id=?', (user,))
	data=instance.cursor.fetchall()
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
	instance = database()
	user = userN
	instance.cursor.execute('SELECT * FROM userinfo WHERE Username=?', (user,))
	uId=instance.cursor.fetchall()
	print(uId[0][2])
	return uId[0][2]

def checkUser(user):
    instance = database()

    data = instance.cursor.execute("SELECT COUNT(*) FROM userInfo WHERE Username=?", (user,))
    return data.fetchone()[0] > 0

def getBlogs():
	instance = database()
	instance.cursor.execute('SELECT * FROM Ublogs')
	blogs=instance.cursor.fetchall()
	return blogs

def checkBlog(userID):
	instance = database()
	user=userID
	instance.cursor.execute("SELECT * FROM Ublogs")
	data = instance.cursor.fetchall()
	for row in data:
		userArray=row
		if(userArray[0]==user):
			return True
	return False

def printUsers():
    instance = database()

    num = instance.cursor.execute("SELECT COUNT(*) FROM userInfo" ).fetchone()[0]
    print("Number of users " + str(num))

    raw_data = instance.cursor.execute("SELECT * FROM userInfo")
    print("Printing users...")
    for row in raw_data:
        for col in row:
            print(col, end=" ")
        print()

#createTables()
#insertUserData("william", "Li", 12)
#verifyLogin("cat", "Li")
