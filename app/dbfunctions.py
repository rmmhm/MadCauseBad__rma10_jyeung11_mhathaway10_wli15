import sqlite3
import csv
DB_FILE="userinfo.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXISTS userInfo (Username TEXT, Password TEXT, id INTEGER PRIMARY KEY)") #for register info

c.execute("CREATE TABLE IF NOT EXISTS Ublurb (id INTEGER, UserBlurbs TEXT)")	#for blurb to be posted on userpage

c.execute("CREATE TABLE IF NOT EXISTS Udraft (id INTEGER, Drafts TEXT)")	#for unfinished blogs

c.execute("CREATE TABLE IF NOT EXISTS Upublished (id INTEGER, Published TEXT)")	#for published blogs to be posted

def insert_login_data(userN, passW, id):     #when given data, it inerts into the database/create it
	insert = "INSERT INTO userInfo (Username, Password, id) VALUES (?, ?, ?);"
	data = (userN, passW, id)
	c.execute(insert, data)

def verify_login(username, password):
	accounts_db = c.execute("SELECT * FROM userInfo")
	for row in accounts_db:
		userArray = row
		if(userArray[0] == userN):		#suppose to look through every row of the userInfo table and see if the the userN exist
			if(userArray[1] == passW):
				return True
	return False

def publish_draft(userid):	#will move the entire draft to the Upublished database based on userid
	uid=userid
	c.execute('SELECT * FROM Udraft WHERE id=?', (uid,))
	data= c.fetchall()
	data = (userid, data[0][1])
	insert = "INSERT INTO Upublished (id, Published) VALUES (?,?);"			#move the entire draft to Upublished table
	c.execute(insert, data)
	c.execute("DELETE FROM Udraft WHERE id = ?", (uid,))

def save_draft(userid, userdraft):
	c.execute("DELETE FROM Udraft WHERE id = 123")		#deletes any old draft to be replaced with new one
	insert = "INSERT INTO Udraft (id, Drafts) VALUES (?,?);"
	data = (userid, userdraft)
	c.execute(insert,data)

def create_blog(userid, blog):
	data = (userid, blog)
	insert = "INSERT INTO Upublished (id, Published) Values (?,?);"
	c.execute(insert, data)

def spit_blog(userid):			#feed userid to get all blogs that have same uid
	username = userid
	c.execute('SELECT * FROM Upublished WHERE id=?', (username,))
	data = c.fetchall()
	i=0
	for row in data:
		blog = data[i][1]
		print(blog)
		i+=1


print("-------------this is a test----------------")
insert_login_data("william", "hi", 12) 		#actually passes html cookies to here to be given to the previous function
insert_login_data("dog", "cat", 23)

def verify_login(userN, passW):
	accounts_db = c.execute("SELECT * FROM userInfo")
	for row in accounts_db:
		userArray = row
		if(userArray[0] == userN):		#suppose to look through every row of the userInfo table and see if the the userN exist
			if(userArray[1] == passW):
				print("worked")				#correct userN and passW pair
			else:						#real userN but wrong password
				print("didn't work")

verify_login("dog", "cat")					#should return worked

accounts_db = c.execute("SELECT * FROM userInfo")		#looks through userInfo row by row and creates a csvfile with each row in the userInfo table
with open('account.csv', 'w') as f:
	csv_writer = csv.writer(f)
	for row in accounts_db:
		userArray = row
		csv_writer.writerow(userArray)

print("-----------------------------------")

save_draft(123,"The question is in a way meaningless, she knows, but one must ask.")
save_draft(23,"During the first part of your life, you only become aware of happiness once you have lost it.")
save_draft(1,"However, it had never occurred to me to contest this law, nor to imagine disobeying it")
publish_blog(1, "Christ, he thinks, by my age I ought to know")
publish_draft(23)
publish_blog(1, "But just as I didn not want to resent my kids")
spit_blog(1)
draft_db = c.execute("SELECT * FROM Udraft")			#should show Udraft that are saved in csv file drafts.csv
with open('draft.csv', 'w') as f:
	csv_writer = csv.writer(f)
	for row in draft_db:
		draftArray = row
		csv_writer.writerow(draftArray)

published_db = c.execute("SELECT * FROM Upublished")		#should show Upublished table in csv file published.csv
with open('published.csv', 'w') as f:
	csv_writer = csv.writer(f)
	for row in published_db:
		pubArray = row
		csv_writer.writerow(pubArray)
