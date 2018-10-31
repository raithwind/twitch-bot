import socket
import time
import threading
import os

botnick = "username"
channel = "#channel to connect to"
host = ("irc.chat.twitch.tv",6667)
passw = "oauth:token"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(host)

def send_message(message):
	s.send("PRIVMSG {} :{}\r\n".format (channel,message).encode())

def await_input():
	while True:
		send_message(input("Send to server: "))
	time.sleep(0.1)
	
def refresh():
	while True:
		text = s.recv(1024)
		print(text)
		
s.send("PASS {}\r\n".format(passw).encode())
time.sleep(0.1)
s.send("USER {0} {0} {0}: This is a fun bot\r\n".format(botnick).encode())
time.sleep(0.1)
s.send("JOIN {}\r\n".format(channel).encode())

t=threading.Thread(target = refresh)

t.start()

await_input()