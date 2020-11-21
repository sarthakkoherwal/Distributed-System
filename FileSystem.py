import socket                
from cryptography.fernet import Fernet 
import random
import os
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 12345
portself=00000
key=b""
# connect to the server on local computer 
turnon="1"
s.connect(('127.0.0.1', port)) 

s.sendall(bytes("1",'utf-8'))
print("Press 1 to register File System")
print("Press 2 to start File System")
choice=input()
s.sendall(bytes(choice,'utf-8'))
if choice=="1":
	while True:
		print("Enter unique ID for File System Registration")
		ID=input()
		s.sendall(bytes(ID,'utf-8'))
		x=s.recv(1024)
		x=x.decode('utf-8')
		if x=="1":
			print("Registration successful")
			s.sendall(bytes("2",'utf-8'))
			comp=s.recv(1024)
			comp=comp.decode('utf-8')
			portself,key=comp.split("|")
			portself=int(portself)
			key=bytes(key,'utf-8')
			break
		else:
			print("ID is not unique")
			print("Registration unsuccessful")
			print("Press 1 to exit")
			print("Press 2 to try again")
			x=input()
		if x=="1":
			turnon="0"
			s.sendall(bytes("2",'utf-8'))
			break;
		else:
			s.sendall(bytes("1",'utf-8'))
if choice=="2":
	print("Enter unique ID of File System")
	ID=input()
	s.sendall(bytes(ID,'utf-8'))
	chec=s.recv(1024)
	chec=chec.decode('utf-8')
	if chec=="1":
		comp=s.recv(1024)
		comp=comp.decode('utf-8')
		portself,key=comp.split("|")
		portself=int(portself)
		key=bytes(key,'utf-8')
	else:
		turnon="0"
		print("File System not yet registered")
s.close()
if turnon=="1":
	s = socket.socket() 
	s.bind(('', portself))       
	print("socket binded to %s" %(portself)) 

	# put the socket into listening mode 
	s.listen(10)  
	print ("socket is listening" )
	while True:
		c, addr = s.accept() 

		# step 3
		fBS=Fernet(key)
		comp=c.recv(1024)
		comp=comp.decode('utf-8')
		RA2,A,KAB=comp.split("|")
		KAB=bytes(KAB,'utf-8')
		KAB=fBS.decrypt(KAB)
		fAB=Fernet(KAB)
		RA2=bytes(RA2,'utf-8')
		RA2=fAB.decrypt(RA2)
		RA2=RA2.decode('utf-8')
		RB1=random.randint(1,100)
		RA2=int(RA2)

		# step 4
		RA2=RA2-1
		RA2=str(RA2)
		RB1=str(RB1)
		RA2=bytes(RA2,'utf-8')
		RB12=bytes(RB1,'utf-8')
		RB12=fAB.encrypt(RB12)
		RA2=fAB.encrypt(RA2)
		RA2=RA2.decode('utf-8')
		RB12=RB12.decode('utf-8')
		c.sendall(bytes(RA2+"|"+RB12,'utf-8'))

		# step 5
		RB12=c.recv(1024)
		RB12=fAB.decrypt(RB12)
		RB12=RB12.decode('utf-8')
		RB12=int(RB12)
		RB12=RB12+1
		RB12=str(RB12)
		if RB12==RB1:
			c.sendall(bytes("1",'utf-8'))
			while True:
				cmd=c.recv(1024)
				cmd=cmd.decode('utf-8')
				if cmd=="pwd":
					curr=os.getcwd()
					c.sendall(bytes(curr,'utf-8'))
				elif cmd=="ls":
					os.system("dir >me.txt")
					f=open("me.txt","r")
					text = f.read()
					f.close()
					os.system("del me.txt")
					c.sendall(bytes(text,'utf-8'))
				elif cmd=="cat":
					path=c.recv(1024)
					path=path.decode('utf-8')
					os.system("echo.>me.txt")
					os.system("copy "+path+" me.txt >me2.txt")
					f=open("me.txt","r")
					text = f.read()
					f.close()
					os.system("del me.txt")
					if len(text)==1:
						f=open("me2.txt","r")
						text = f.read()
						f.close()
					c.sendall(bytes(text,'utf-8'))
					os.system("del me2.txt")
					# curr=os.system
				elif cmd=="cp":
					comp=c.recv(1024)
					comp=comp.decode('utf-8')
					path1,path2=comp.split("|")
					os.system("copy "+path1+" "+path2+" >me.txt")
					f=open("me.txt","r")
					text = f.read()
					f.close()
					os.system("del me.txt")
					c.sendall(bytes(text,'utf-8'))
				elif cmd=="exit":
					break
		else:
			c.sendall(bytes("2",'utf-8'))
		c.close()
    	# print('Got connection from',addr)

