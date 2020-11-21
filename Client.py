import socket                
from cryptography.fernet import Fernet 
import random
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 12345   

# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 
auth="2"
portServer=000
print("Press 1 to register DS")
print("Press 2 to login to DS")
choice=input()
if choice=="1":
	s.sendall(bytes("2",'utf-8'))
	while True:
		print("Enter username for Client Registration")
		user=input()
		print("Enter password for Client Registration")
		passw=input()
		s.sendall(bytes(user,'utf-8'))
		s.sendall(bytes(passw,'utf-8'))
		x=s.recv(1024)
		x=x.decode('utf-8')
		if x=="1":
			print("Registration successful")
			s.sendall(bytes("2",'utf-8'))
			print("Enter 1 to exit")
			print("Enter 2 to login to DS")
			choice=input()
			break
		else:
			print("Username is not unique")
			print("Registration unsuccessful")
			print("Enter 1 to exit")
			print("Enter 2 to try again")
			x=input()
		if x=="1":
			s.sendall(bytes("2",'utf-8'))
			break;
		else:
			s.sendall(bytes("1",'utf-8'))
if choice=="2":
	s.sendall(bytes("3",'utf-8'))
	login="2"
	user=""
	passw=""
	while True:
		print("Enter your Username")
		user=input()
		print("Enter your password")
		passw=input()
		s.sendall(bytes(user,'utf-8'))
		s.sendall(bytes(passw,'utf-8'))
		x=s.recv(1024)
		x=x.decode('utf-8')
		ch="100"
		if x=="1":
			print("Login Successful")
			s.sendall(bytes("2",'utf-8'))
			login="1"
			break
		else :
			print("Login unsuccessful")
			print("Press 1 to exit")
			print("Press 2 to try again")
			ch=input()
		if ch=="1":
			s.sendall(bytes("2",'utf-8'))
			break
		else:
			s.sendall(bytes("1",'utf-8'))
	IDchecker="2"
	ID=""
	if login=="1":
		while True:
			print("Enter unique ID of File System")
			ID=input()
			s.sendall(bytes(ID,'utf-8'))
			x=s.recv(1024)
			x=x.decode('utf-8')
			if x=="1":
				print("ID found, initiating authentication")
				s.sendall(bytes("2",'utf-8'))
				IDchecker="1"
				break
			else:
				print("File System does not exist")
				print("Press 1 to exit")
				print("Press 2 to try again")
				ch=input()
			if ch=="1":
				s.sendall(bytes("2",'utf-8'))
				break
			else:
				s.sendall(bytes("1",'utf-8'))
	if IDchecker=="1":
		# step 1
		r=random.randint(1,100)
		RA1=str(r)
		A=user
		B=ID
		comp=RA1+"|"+A+"|"+B
		s.sendall(bytes(comp,'utf-8'))
		KAS=s.recv(1024)

		# step 2
		comp=s.recv(1024)
		comp=comp.decode('utf-8')
		RA12,B2,KAB,A2,KAB1,portServer=comp.split("|")
		fAS=Fernet(KAS)
		RA12=bytes(RA12,'utf-8')
		RA12=fAS.decrypt(RA12)
		RA12=RA12.decode('utf-8')
		B2=bytes(B2,'utf-8')
		B2=fAS.decrypt(B2)
		B2=B2.decode('utf-8')
		KAB=bytes(KAB,'utf-8')
		KAB=fAS.decrypt(KAB)
		fAB=Fernet(KAB)
		A2=bytes(A2,'utf-8')
		A2=fAS.decrypt(A2)
		A2=A2.decode('utf-8')
		KAB1=bytes(KAB1,'utf-8')
		KAB1=fAS.decrypt(KAB1)
		KAB1=KAB1.decode('utf-8')
		if RA12!=RA1 or B!=B2:
			print("Authentication Failed")
		else:
			s.close()
			s=socket.socket()
			portServer=int(portServer)
			s.connect(('127.0.0.1', portServer))
			r=random.randint(1,100)

			# step 3
			RA2=str(r)
			RA22=fAB.encrypt(bytes(RA2,'utf-8'))
			RA22=RA22.decode('utf-8')
			comp=RA22+"|"+A2+"|"+KAB1
			s.sendall(bytes(comp,'utf-8'))

			# step 4
			comp=s.recv(1024)
			comp=comp.decode('utf-8')
			RA22,RB1=comp.split("|")
			RA22=bytes(RA22,'utf-8')
			RA22=fAB.decrypt(RA22)
			RA22=RA22.decode('utf-8')
			RA22=int(RA22)
			RA22=RA22+1
			RA22=str(RA22)
			RB1=bytes(RB1,'utf-8')
			RB1=fAB.decrypt(RB1)
			RB1=RB1.decode('utf-8')
			RB1=int(RB1)
			if RA22!=RA2:
				RB1=0

			# step 5
			RB1=RB1-1
			RB1=str(RB1)
			RB1=bytes(RB1,'utf-8')
			RB1=fAB.encrypt(RB1)
			s.sendall(RB1)
			checker=s.recv(1024)
			checker=checker.decode('utf-8')
			if checker=="1":
				print("Authentication Complete")
				print("Connection established")
				auth="1"
			else:
				print("Connection failed")
	if auth=="1":
		while True:
			print("Enter pwd - Print current working directory")
			print("Enter cat - to display contents of file")
			print("Enter ls - list contents of folder")
			print("Enter cp - copy one file from one folder to another")
			print("Enter exit to terminate connection")
			choice=input()
			s.sendall(bytes(choice,'utf-8'))
			if choice=="exit":
				break
			elif choice=="pwd":
				curr=s.recv(1024)
				curr=curr.decode('utf-8')
				print(curr)
				print()
			elif choice=="ls":
				curr=s.recv(1024)
				curr=curr.decode('utf-8')
				comp=[]
				comp=curr.split("|")
				for cc in comp:
					print(cc)
				print()
			elif choice=="cat":
				print("Give file path")
				path=input()
				s.sendall(bytes(path,'utf-8'))
				res=s.recv(4096)
				res=res.decode('utf-8')
				print(res)
				print()
			elif choice=="cp":
				print("Name of file to copy from")
				path=input()
				print("Name of file to place the copy")
				path1=input()
				path=path+"|"+path1
				s.sendall(bytes(path,'utf-8'))
				res=s.recv(4096)
				res=res.decode('utf-8')
				print(res)
				print()

else :
	s.sendall(bytes("4",'utf-8'))
	
s.close()
