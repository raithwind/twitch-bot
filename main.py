import socket
import time
from configs import *
import threading

users = {}

class Connection:
	def __init__(self,host,port,username,owner,authcode,channel):
		self.host = (host,port)
		self.username = username
		self.owner = owner
		self.authcode = authcode
		self.channel = channel
		self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	
	
	def connect(self):
		self.socket.connect(self.host)
		self.socket.send('CAP REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership\r\n'.encode('utf-8'))
		print("Beginning handshake\n")
		self.socket.send("PASS {}\r\n".format(self.authcode).encode())
		time.sleep(0.1)
		self.socket.send("USER {0} {0} {0} :This is a fun bot!\r\n".format(botnick).encode())
		time.sleep(0.1)
		self.socket.send("NICK {}\r\n".format(botnick).encode())
		time.sleep(0.1)
		print("Joining "+self.channel)
		self.socket.send("JOIN #{}\r\n".format(self.channel).encode())
		print("Connected!\n")
		
	def chat_refresh(self):
		message  = self.socket.recv(1024).decode()
		if len(message) == 0:
			print("Should I leave boss?")
		elif message.startswith("PING"):
			message=message.split(":")
			self.socket.send("PONG :{}\r\n".format(message[1:]).encode())
			print("pingy: {}".format(message))
		elif "tmi.twitch.tv PRIVMSG #{} :".format(self.channel) in message:
			message= message.split("tmi.twitch.tv PRIVMSG #{} :".format(self.channel))
			messagedetails = message[0]
			message = message[1].strip()
			print("{}".format(message))
			if message.startswith("!"):
				process_command(self,messagedetails,message[1:])
		else:
			print(message)
			
	def send_to_chat(self,message):
			self.socket.send("PRIVMSG #{} :{}\r\n".format(self.channel,message).encode())
		
	def send_to_server(self,message):
		self.socket.send("{}\r\n".format(message).encode())
		
	def send_to_private(self,recipient,message):
		self.socket.send("PRIVMSG jtv :/w {} {}\r\n".format(recipient,message).encode())


def process_command(connection, messagedetails,command):
	messagedetails = messagedetails.split(";")
	username = messagedetails[2].replace("display-name=","")
	print("Username: {}. Command: {}".format(username,command))
	

test = Connection("irc.chat.twitch.tv",6667,
			botnick.lower(),owner.lower(),
			passw,channel.lower())

test.connect()

if __name__ == "__main__":
    while True:
        test.chat_refresh()
