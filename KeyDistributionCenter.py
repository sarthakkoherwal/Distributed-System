# first of all import the socket library 
import socket            
from cryptography.fernet import Fernet 

FS={}
FSports={}
DS={}
DSpass={}

# next create a socket object 
s = socket.socket()      
print ("Socket successfully created")
KAB=b'saf'

# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 12345                

s.bind(('', port))       
print ("socket binded to %s" %(port)) 

# put the socket into listening mode 
s.listen(10)  
print ("socket is listening" )        
while True: 
    # Establish connection with client. 
    c, addr = s.accept()     
    print ('Got connection from', addr )
    x=c.recv(1024)
    x=x.decode('utf-8')
    if x=="1":
        xx=c.recv(1024)
        xx=xx.decode('utf-8')
        if xx=="1":
            key=Fernet.generate_key()
            while True:
                ID=c.recv(1024)
                if ID in FS:
                    c.sendall(bytes("2",'utf-8'))
                else:
                    FS[ID]=key
                    FSports[ID]=addr[1]
                    key=key.decode('utf-8')
                    c.sendall(bytes("1",'utf-8'))
                    c.sendall(bytes(str(addr[1])+"|"+key,'utf-8'))
                chec=c.recv(1024)
                chec=chec.decode('utf-8')
                if chec=="2":
                    break
        else:
            ID=c.recv(1024)
            if ID in FS:
                c.sendall(bytes("1",'utf-8'))
                FSports[ID]=addr[1]
                key=FS[ID]
                key=key.decode('utf-8')
                c.sendall(bytes(str(addr[1])+"|"+key,'utf-8'))
            else:
                c.sendall(bytes("2",'utf-8'))
    if x=="2":
        regist="2"
        key=Fernet.generate_key()
        while True:
            user=c.recv(1024)
            passw=c.recv(1024)
            if user in DS:
                c.sendall(bytes("2",'utf-8'))
            else:
                DS[user]=key
                DSpass[user]=passw
                c.sendall(bytes("1",'utf-8'))
                regist="1"
            chec=c.recv(1024)
            if regist=="1":
                x=c.recv(1024)
                x=x.decode('utf-8')
            chec=chec.decode('utf-8')
            if chec=="2":
                break

    if x=="3":
        login="2"
        while True:
            user=c.recv(1024)
            passw=c.recv(1024)
            if user in DS and DSpass[user]==passw:
                c.sendall(bytes("1",'utf-8'))
                login="1"
            else:
                c.sendall(bytes("2",'utf-8'))
            chec=c.recv(1024)
            chec=chec.decode('utf-8')
            if chec=="2":
                break
        IDchecker="2"
        if login=="1":
            while True:
                ID=c.recv(1024)
                if ID in FS:
                    c.sendall(bytes("1",'utf-8'))
                    IDchecker="1"
                else:
                    c.sendall(bytes("2",'utf-8'))
                chec=c.recv(1024)
                chec=chec.decode('utf-8')
                if chec=="2":
                    break
        if IDchecker=="1":

            # step 1
            comp=c.recv(1024)
            comp=comp.decode('utf-8')
            RA1,A,B=comp.split("|")
            RA1=bytes(RA1,'utf-8')
            A=bytes(A,'utf-8')
            B=bytes(B,'utf-8')
            portFS=FSports[B]
            portFS=str(portFS)
            KAS=DS[A]
            KBS=FS[B]
            KAB=Fernet.generate_key()
            c.sendall(KAS)

            # step 2
            fAS=Fernet(KAS)
            fBS=Fernet(KBS)
            A=fBS.encrypt(A)
            KAB1=fBS.encrypt(KAB)
            RA1=fAS.encrypt(RA1)
            B=fAS.encrypt(B)
            KAB2=fAS.encrypt(KAB)
            A=fAS.encrypt(A)
            KAB1=fAS.encrypt(KAB1)
            RA1=RA1.decode('utf-8')
            B=B.decode('utf-8')
            KAB2=KAB2.decode('utf-8')
            A=A.decode('utf-8')
            KAB1=KAB1.decode('utf-8')
            comp=RA1+"|"+B+"|"+KAB2+"|"+A+"|"+KAB1+"|"+portFS
            c.sendall(bytes(comp,'utf-8'))
    # sendall a thank you message to the client. 

    # Close the connection with the client 
    c.close()


