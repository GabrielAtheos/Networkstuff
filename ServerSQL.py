import sqlite3

conn = sqlite3.connect('database/users.db')

class ConnectToSQL:

	def recieveName(self, var1):
		cursor = conn.execute("SELECT name FROM users WHERE userEmail = '%s';" % var1)
		for row in cursor:
			return row[0]

	def recievePassword(self, var1):
		cursor = conn.execute("SELECT password FROM users WHERE userEmail = '%s';" % var1)
		for row in cursor:
			return row[0]
	
	def countUsers(self):
		cursor = conn.execute("SELECT COUNT (email) FROM users;")
		for row in cursor:
			return row[0]

	def addUser (self, email, password):
		conn.execute("INSERT INTO users VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s');" % (email,password[0],"no","no","no","no","no","no","no","no",""))
		conn.commit()

	def updateUserResume(self,email, d):
		conn.execute("REPLACE INTO users VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s');" % 
					(email, self.recievePassword(email), d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],self.getAuthorizedUsers(email)))
		conn.commit()

	def getUser(self, email):
		cursor = conn.execute("SELECT first_name, last_name, email, phone, school_name, major, company_name, company_position FROM users WHERE userEmail = '%s';" %email)
		data = ";"
		for row in cursor:
			data = data.join(row)
		toStrip = email + ";"
		data = data.replace(toStrip,'')
		toStrip = self.recievePassword(email) +";"
		data = data.replace(toStrip,'')
		return data

	def isUserAuthorized(self, email, requestingEmail):
		cursor = conn.execute("SELECT authorized_users FROM users WHERE useremail = '%s';" % email)
		authorized = False
		data = ";"
		for row in cursor:
			data = data.join(row)
		print "SQL: ", data
		data = data.split(";")
		print "SQL: ", data
		for x in data:
			if x == requestingEmail:
				print "X: ", x
				authorized = True
		return authorized

	def addAuthorizedUser(self, email, authorizedEmail):
		d = self.getUser(email)
		d = d.split(";")
		foo = self.getAuthorizedUsers(email)
		foo += authorizedEmail + ";"
		conn.execute("REPLACE INTO users VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s');" % 
					(email, self.recievePassword(email), d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],foo))
		conn.commit()

	def getAuthorizedUsers(self, email):
		cursor = conn.execute("SELECT authorized_users FROM users WHERE useremail = '%s';" % email)
		for row in cursor:
			return row[0]

	def deleteUser(self,email):
		conn.execute("DELETE FROM users WHERE userEmail = '%s';" % email)
		conn.commit()

	def doesItExist(self, var1):
		cursor = conn.execute("SELECT * FROM users WHERE userEmail = '%s';" % var1)
		value = -1
		for row in cursor:
			value = row[0]
		if (value == -1):
			return False
		elif(value <= 0):
			return False
		else:
			return True

	def checkPassword(self, email, data):
		if self.recievePassword(email) == data[0]:
			return True
		else:
			return False

	def close(self):
		conn.close()
