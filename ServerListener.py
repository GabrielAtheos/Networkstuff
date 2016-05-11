#!/usr/bin/python

import sys
import socket
import ServerSQL

from time import gmtime, strftime

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

	while True:	
		command = ""
		serverConnection = ServerSQL.ConnectToSQL()
		c, addr = s.accept()
		info = c.recv(500)
		print ("2. Got connection from ", addr)
		print ("SENT INFO: ",info)
		print strftime("%Y-%m-%d %H:%M:%S", gmtime())

		info = info.rstrip('\r\n !#$^&*()+-=][/,{}?><') #sql sanitation
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
		info = info.replace(toStrip,'',1)

		i = 0
		data = info.split(";")
		data.remove(data[len(data)-1])
		print "\nRecieved info: "
		print "------------------"
		for x in data:
			i = i + 1
			print i,":",x

		print "------------------"

		print "User account: ", userEmail
		
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
			if serverConnection.doesItExist(userEmail):
				stmt = serverConnection.getUser(userEmail)
			else:
				stmt = "User doesn't exist"
		elif command == "login":
			if serverConnection.doesItExist(userEmail):
				if serverConnection.checkPassword(userEmail, data):
					stmt = "success"
				else:
					stmt = "wrongpassword"
			else:
				stmt = "wrongemail"
		elif command == "addauthorizeduser":
			if serverConnection.doesItExist(data[0]):
				serverConnection.addAuthorizedUser(userEmail, data[0])
				stmt = "success"
			else:
				stmt = "nouser"
		elif command == "getlinked":
			if serverConnection.isUserAuthorized(userEmail, data[0]):
				stmt = serverConnection.getUser(data[0])
			else:
				stmt = "notauthorized"

		userEmail = ""
		command = ""
		info = ""
		data = None


		end = "\r\n"
		stmt = stmt + end
		sys.stdout.write("\nReturned info: ")
		print stmt
		c.send(stmt)
		c.close()

if __name__ == '__main__':
	main()
