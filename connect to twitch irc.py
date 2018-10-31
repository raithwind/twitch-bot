import socket
import time
import threading


botnick = "BOTNICK"
channel = "#{}".format(input("What channel to lurk: "))
host = ("irc.chat.twitch.tv",6667)
passw = "oauth:TOKEN"



s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(host)
#s.send("/join {}".format(channel).encode())

def send_command(command):
	s.send("PRIVMSG {} :{}\r\n".format(channel,command).encode())

def await_input():
	while True:
		send_command(input("Send to server: "))
		time.sleep(1)
def refresh():
	while True:
		text=s.recv(1024)
		print("{} :{}\n".format(text,len(text)))
		with open("twitchlog.txt","a") as f:
			f.write("{} \n".format(text.decode()))
def ping_pong():
	s.send("PRIVMSG :PONG tmi.twitch.tv".encode())

s.send("PASS {}\r\n".format(passw).encode())
time.sleep(0.1)
s.send("USER {0} {0} {0} :This is a fun bot!\r\n".format(botnick).encode())
time.sleep(0.1)
s.send("NICK {}\r\n".format(botnick).encode())
time.sleep(0.1)
s.send("JOIN {}\r\n".format(channel).encode())

t = threading.Thread(target=await_input)
#t.start()
u =threading.Thread(target=refresh)
u.start()

while True:
	await_input()
