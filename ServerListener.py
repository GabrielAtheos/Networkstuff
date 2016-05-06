#!/usr/bin/python

import sys
import socket
import ServerSQL

def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = socket.gethostname()
	port = 9090

	s.bind(('', port))
	s.listen(5)

	last = ""
	command = ""
	isCommand = False
	isUser = False
	length = 0
	BEGIN = "::"
	END = "%%"
	data = []
	stmt = ""
	userEmail = ""

	serverConnection = ServerSQL.ConnectToSQL()

	while True:	
		command = ""
		serverConnection = ServerSQL.ConnectToSQL()
		c, addr = s.accept()
		info = c.recv(500)
		print ("2. Got connection from ", addr)
		print ("SENT INFO: ",info)

		info = info.rstrip('\r\n !#$^&*()_+-=][/,{}?><') #sql sanitation
		info = info.lower()

		'''
		Command & Login parser
		----------------------
		This section looks for a command in the string of info sent to 
		the server. The command is deliminated by "::" at the begining and
		"%%" at the end. Immediately following the command will be the
		user's login email address. This section of code locates and extracts
		both items and sends the rest of the user data on to be processed
		and handled as needed.
		'''
		for x in info:
			if isCommand:
				command += x
			if x == last and x==':':
				isCommand = True
			elif x == '%' and x==last:
				isCommand = False
				isUser = True
				command = command.rstrip('%')
			if not isCommand and isUser and x != '%':
				if x ==';':
					isUser = False
				else:
					userEmail += x
			if x == ';':
				length += 1
			last = x

		toStrip = BEGIN + command + END
		info = info.replace(toStrip,'')
		toStrip = userEmail + ";"
		info = info.replace(toStrip,'')

		data = info.split(";")
		
		for x in data:
			print x
		print userEmail
		
		'''
		end text parse
		'''
		
		print "Command: ", command

		if not command:
			stmt = "error - No command"
			print "No command"
		if command == "exit":
			serverConnection.close()
			c.send("Exiting Now")
			c.close()
			sys.exit(0)
		elif command == "adduser":
			if not serverConnection.doesItExist(userEmail):
				serverConnection.addUser(userEmail, data)
				stmt = "User Added!"
			else:
				stmt = "User Already Exists"
		elif command == "updateresume":
			serverConnection.updateUserResume(userEmail, data)
			stmt = "Resume Updated!"
		elif command == "getinfo":
			stmt = serverConnection.getUser(userEmail)
		elif command == "login":
			if serverConnection.doesItExist(userEmail):
				if serverConnection.checkPassword(userEmail, data):
					stmt = "success"
				else:
					stmt = "wrongpassword"
			else:
				stmt = "wrongemail"

		userEmail = ""


		end = "\r\n"
		stmt = stmt + end
		print stmt
		c.send(stmt)
		c.close()

if __name__ == '__main__':
	main()
