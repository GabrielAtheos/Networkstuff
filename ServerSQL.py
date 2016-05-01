import sqlite3

conn = sqlite3.connect('database/users.db')

class ConnectToSQL:

	def recieveName(self, var1):
		cursor = conn.execute("SELECT name FROM users WHERE email = '%s' ;" % var1)
		for row in cursor:
			return row[0]

	def recievePassword(self, var1):
		cursor = conn.execute("SELECT password FROM users WHERE email = '%s' ;" % var1)
		for row in cursor:
			return row[0]
	
	def countUsers(self):
		cursor = conn.execute("SELECT COUNT (email) FROM users;")
		for row in cursor:
			return row[0]

	def addUser (self, d):
		
		conn.execute("INSERT INTO users VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % 
					(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8]))
		conn.commit()

	def getUser(self, email):
		cursor = conn.execute("SELECT * FROM users WHERE email = '%s'" %email)
		data = prepareText(cursor)

	def doesItExist(self, var1):
		cursor = conn.execute("SELECT * FROM users WHERE email = '%s'" % var1)
		value = -1
		for row in cursor:
			value = row[0]
		if (value == -1):
			return False
		elif(value <= 0):
			return False
		else:
			return True

	def prepareText(self, data):


	def close(self):
		conn.close()