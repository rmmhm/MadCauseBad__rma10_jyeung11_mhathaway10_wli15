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

def publish_draft(Userid):	#will move the entire draft to the Upublished database based on Userid
	drafts_db = c.execute("SELECT * FROM Udraft")		#goes through the entire Udraft table
	draft=""
	for row in drafts_db:
		draftArray = row
		if(draftArray[0]==Userid):					#finds the row with matching Userid
			draft = draftArray[1]					#takes the draft from corresponding Userid
	insert = "INSERT INTO Upublished (id, Published) VALUES (?,?);"			#move the entire draft to Upublished table
	data = (Userid, draft)
	c.execute(insert, data)
	c.execute("DELETE FROM Udraft WHERE id = 123")			#issue rn with setting id to a variable

def save_draft(Userid, Userdraft):
	c.execute("DELETE FROM Udraft WHERE id = 123")		#deletes any old draft to be replaced with new one
	insert = "INSERT INTO Udraft (id, Drafts) VALUES (?,?);"
	data = (Userid, Userdraft)
	c.execute(insert,data)
	

insert_login_data("william", "hi", 12) 		#actually passes html cookies to here to be given to the previous function
insert_login_data("dog", "cat", 23)

def vertify_login(userN, passW):
	accounts_db = c.execute("SELECT * FROM userInfo")
	for row in accounts_db:
		userArray = row
		if(userArray[0] == userN):		#suppose to look through every row of the userInfo table and see if the the userN exist
			if(userArray[1] == passW):
				print("worked")				#correct userN and passW pair
			else:						#real userN but wrong password
				print("didn't work")

vertify_login("dog", "cat")					#should return worked

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
publish_draft(123)

draft_db = c.execute("SELECT * FROM Udraft")
with open('draft.csv', 'w') as f:
	csv_writer = csv.writer(f)
	for row in draft_db:
		draftArray = row
		csv_writer.writerow(draftArray)

published_db = c.execute("SELECT * FROM Upublished")
with open('published.csv', 'w') as f:
	csv_writer = csv.writer(f)
	for row in published_db:
		pubArray = row
		csv_writer.writerow(pubArray)
