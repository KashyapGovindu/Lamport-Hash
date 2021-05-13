import socket
from _thread import *
import sys
import threading
import sql_db
import lamport

CHAR_ENC = 'utf-8'
PORT = 8234 #Server listening to port 8234
CONNECTIONS = 0
BUFFERSIZE = 1024
print_lock = threading.Lock()

#Object for each user
class User:
    def __init__(self, username,n):
        self.username = username
        self.n_value = n

    def addPassword(self, password):
        self.password = password #Password - Its a hashed password

def serverThread(client):
    receive = client.recv(BUFFERSIZE)
    receive = receive.decode().rstrip()
    # print(receive)
    clientRecord = None
    con = None
    if receive == "INITIATE":
        username = client.recv(BUFFERSIZE)
        username = username.decode().rstrip()
        print("Received Username " + username)
        n = client.recv(BUFFERSIZE)
        n = n.decode().rstrip()
        print("Received n value " + n)
        clientRecord = User(username,n)
        print("Client Record created")
        password = client.recv(BUFFERSIZE)
        password = password.decode().rstrip()
        # print(type(password))       ####
        print("Received password " + password)

        clientRecord.addPassword(password)
        con = sql_db.sql_connection()
        sql_db.credentialsTable(con)
        sql_db.insertRecord(con,clientRecord)
        print("Initialized client record successful!")
        sql_db.selectClient(con,clientRecord)       ####
    assert clientRecord != None, "Client Record doesnt exist"

    while True:
        receive = client.recv(BUFFERSIZE)
        receive = receive.decode().rstrip()
        if receive == "AUTHENTICATE":

            #Send value of n and wait for client value of x= hash^n-1(pass)
            data = clientRecord.n_value
            client.send(data.ljust(BUFFERSIZE).encode())

            data = client.recv(BUFFERSIZE) #x= hash^n-1(pass)
            data = data.decode().rstrip()
            print("Hash value Received: " + data)
            #Verify with stored value of hashed password
            if lamport.verifySignature(data,clientRecord.password):
                client.send("YES".ljust(BUFFERSIZE).encode())
                print("Authentication of A is successful")
                #Update the entry from <n,hash^n(pass)> to <n-1,hash^n-1(pass)> >
                clientRecord.n_value = str(int(clientRecord.n_value) - 1)
                x = int(clientRecord.n_value)
                if x < 2:
                    print("Entered here x<2")
                    client.send("REFRESH".ljust(BUFFERSIZE).encode()) #Request for n value again
                    n = client.recv(BUFFERSIZE)
                    n = n.decode().rstrip()
                    # print(n)
                    clientRecord.n_value = n
                    hashp = client.recv(BUFFERSIZE)
                    hashp = hashp.decode().rstrip()
                    # print(hashp)
                    clientRecord.password = hashp
                    sql_db.updateClientEntry(con,clientRecord)
                    sql_db.selectClient(con,clientRecord)       ####
                    print("Refreshed client record with new N value,Salt and Password")
                else:
                    clientRecord.password = data
                    sql_db.updateClientEntry(con,clientRecord)
                    sql_db.selectClient(con,clientRecord)       ####
                
            else:
                client.send("NO".ljust(BUFFERSIZE).encode())
                print("Authentication of A failed")
                break
    print("BYE")
    client.send("BYE".ljust(BUFFERSIZE).encode())
    con.close()
    sys.exit()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(),PORT))
    print("Socket binded to port ",PORT)
    s.listen(10)
    print("Socket listening on port ",PORT,"...")
    while True:
        client, addr = s.accept()
        print('Connection from ',addr, " is established")
        start_new_thread(serverThread, (client,))


if __name__ == '__main__':
    main()