#!/usr/bin/python

# this program will scan a given range of hosts for servers that respond to SMTP VRFY
# if server is located, it will then check the server for valid usernames using the provided list
# planning to add some functionality to generate the list of smtp targets using nmap and a given IP range

import socket
import sys

# validate input parameters
if len(sys.argv) != 3:
	print "Usage: vrfy.py <user list> <target list>"
	print "both files should be list formatted text files"
	sys.exit(0)

# set arg 1 to user_file as the filename
user_file = sys.argv[1]

# set arg 2to target_file as the filename
target_file = sys.argv[2]

# open list of users and set values to a list
with open(user_file, 'r') as f:
	userlist = f.readlines()
	index = 0
	for user in userlist:
		user = user.rstrip("\n")
		userlist[index] = user
		index = index + 1
f.close()

# open list of targets and set values to a list
with open(target_file, 'r') as f:
	targetlist = f.readlines()
	index = 0
	for target in targetlist:
		target = target.rstrip("\n")
		targetlist[index] = target
		index = index + 1 
f.close()

print "LIST OF IP ADDRESSES TO SCAN:"
print targetlist
print "\n"

print "LIST OF USERS TO CHECK FOR:"
print userlist
print "\n"

# iterate through list of targets, checking to see if they respond to VRFY command
for target in targetlist:
	# create socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# connect using socket
	connect = s.connect((target,25))
	
	# receive the banner
	banner = s.recv(1024)
	print banner
	
	# test to see if VRFY is supported
	s.send('VRFY admin\r\n')
	result = s.recv(1024)
	code = result[:3]
	print "SMTP Server responded with code " + code
	if code != "250" and code != "550":
		print "SMTP Server does not support VRFY"
	else:
		print "SMTP Server support VRFY, Scanning list now...\n"
		# code 550 is user unknown, code 250 is user found
		# iterate through list of users to check
		for username in userlist:
			# VRFY users
			s.send('VRFY ' + username + '\r\n')
			result = s.recv(1024)
			print result
	s.close()

exit()
