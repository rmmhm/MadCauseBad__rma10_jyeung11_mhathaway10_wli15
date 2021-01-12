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
        self.db.commit()
        self.cursor.close()
        self.db.close()

    def __del__(self):
        self.close()

def createTables():
    instance = database()

    instance.cursor.execute("CREATE TABLE IF NOT EXISTS userInfo (Username TEXT, Password TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)")
    instance.cursor.execute("CREATE TABLE IF NOT EXISTS Uentries (id INTEGER, title TEXT, entry TEXT, eid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)")
    instance.cursor.execute("CREATE TABLE IF NOT EXISTS Ublogs (id INTEGER, username TEXT, title TEXT)")

def insertUserData(userN, passW):
    """ when given data, it inerts into the database/create it """
    instance = database()
    print(userN + ", " + passW)
    instance.cursor.execute("INSERT INTO userInfo (Username, Password) VALUES (?, ?)", (userN, passW))

def verifyLogin(username, password):
    """ gives user and pass to check if the info match """
    instance = database()
    data = instance.cursor.execute("SELECT COUNT(*) FROM userInfo WHERE Username=? AND Password=?", (username, password) ).fetchone()[0]
    return data == 1

def checkUser(userN):
    instance = database()
    data = instance.cursor.execute("SELECT COUNT(*) FROM userInfo WHERE Username=?", (userN,))
    return data.fetchone()[0] > 0

def getId(userN):
	instance = database()
	instance.cursor.execute('SELECT * FROM userinfo WHERE Username=?', (userN,))
	uId=instance.cursor.fetchall()
	return uId[0][2]

def createBlog(userID, username, title):
	instance = database()
	data = (userID, username, title)
	insert = "INSERT INTO Ublogs (id, username, title) VALUES (?, ?, ?);"
	instance.cursor.execute(insert, data)

def checkBlog(userID):
    instance = database()
    data = instance.cursor.execute("SELECT COUNT(*) FROM Ublogs WHERE id=?", (userID,))
    return data.fetchone()[0] > 0

def getBlogs():
	instance = database()
	instance.cursor.execute('SELECT * FROM Ublogs')
	blogs=instance.cursor.fetchall()
	return blogs

def getBlogTitle(userID):
	instance = database()
	instance.cursor.execute('SELECT * FROM Ublogs WHERE id=?', (userID,))
	data=instance.cursor.fetchall()
	return data[0][2]

def createEntry(userID, title, entry):
	instance = database()
	data = (userID, title, entry)
	insert = "INSERT INTO Uentries (id, title, entry) VALUES (?, ?, ?);"
	instance.cursor.execute(insert, data)

def editEntry(entryID, entryTitle, entryText):
    instance = database()
    data = (entryTitle, entryText, entryID)
    insert = 'UPDATE Uentries SET title=?, entry=? WHERE eid=?'
    instance.cursor.execute(insert, data)

def deleteEntry(entryID):
    instance = database()
    data = (entryID)
    delete = 'DELETE FROM Uentries WHERE eid=?'
    instance.cursor.execute(delete, data)

def getEntries(userID):
	instance = database()
	instance.cursor.execute('SELECT * FROM Uentries WHERE id=?', (userID,))
	data=instance.cursor.fetchall()
	return data
