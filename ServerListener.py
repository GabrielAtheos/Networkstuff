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
	length = 0
	BEGIN = "::"
	END = "%%"
	data = []
	stmt = ""

	serverConnection = ServerSQL.ConnectToSQL()

	while True:	
		command = ""
		serverConnection = ServerSQL.ConnectToSQL()
		c, addr = s.accept()
		info = c.recv(500)
		with open("log.txt", "w") as logFile:
			logFile.write("2. Got connection from %s\n SENT INFO: %s" % (addr, info))
		print ("2. Got connection from ", addr)
		print ("SENT INFO: ",info)

		info = info.rstrip('\r\n !#$^&*()_+-=][/,{}?><')
		info = info.lower()

		'''
		text parsing code
		'''
		for x in info:
			if isCommand:
				command += x
			if x == last and x==':':
				isCommand = True
			elif x == last and x=='%':
				isCommand = False
				command = command.rstrip('%')
			if x == ';':
				length += 1
			last = x

		toStrip = BEGIN + command + END
		info = info.replace(toStrip,'')

		for i in range(length):
			temp = ""
			for x in info:
				temp += x
				if x == ';':
					break
			info = info.replace(temp,'')
			temp = temp.rstrip(";")
			data.append(temp)

		'''
		end text parse
		'''
		
		print ("Command: ", command)

		if not command:
			stmt = "error - No command"
			print "No command"
		if command == "exit":
			serverConnection.close()
			c.send("Exiting Now")
			c.close()
			sys.exit(0)
		elif command == "adduser":
			serverConnection.addUser(data)
			stmt = "User Added!"
		'''
		elif command == "retrieveUser":
			some code here

		'''
		end = "\r\n"
		stmt = stmt + end
		c.send(stmt)
		c.close()

if __name__ == '__main__':
	main()
