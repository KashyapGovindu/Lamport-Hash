import socket,sys
import lamport

CHAR_ENC = 'utf-8'
PORT = 8234 #Server listening to port 8234
BUFFERSIZE = 1024

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(),PORT))
    print("Connection to server successful")

    # name = input("Enter name: ")
    # n_val = input("Enter value of integer n: ")
    # password = input("Enter password: ")
    # salt = input("Enter salt: ") 

    name = "Alice"
    n_val = "5"
    password = "adminroot"
    salt = "abcdefghij"

    #Compute hash^n(pass|salt)
    hashpass = lamport.genHashwithSalt(password,salt,int(n_val))
    print(type(hashpass))
    print(hashpass)

    #INITIALIZE
    s.send("INITIATE".ljust(BUFFERSIZE).encode())
    s.send(name.ljust(BUFFERSIZE).encode())
    s.send(n_val.ljust(BUFFERSIZE).encode())
    s.send(hashpass.ljust(BUFFERSIZE).encode())
    s.send(salt.ljust(BUFFERSIZE).encode())
    print("Initiation Successful!")

    #AUTHENTICATE
    while True:
        print("Choose among following options:")
        x=int(input("1. Authenticate\n2. Exit\n"))
        if x==1:
            #Send AUTHENTICATE REQUEST AND 
            s.send("AUTHENTICATE".ljust(BUFFERSIZE).encode())
            data_n = s.recv(BUFFERSIZE)
            data_n= data_n.decode().rstrip() # n value sent by Server
            print("n value received: "+ data_n)

            data = s.recv(BUFFERSIZE)
            data= data.decode().rstrip() # salt value sent by Server
            print("Salt value received: "+ data)

            # compute x = hash^n-1(pass|salt) from received n,salt
            password = input("Enter password: ")
            enc = lamport.genHashwithSalt(password,data,int(data_n) - 1)
            print("encoded password: "+enc)
            s.send(enc.ljust(BUFFERSIZE).encode())
            data = s.recv(BUFFERSIZE)
            data = data.decode().rstrip()
            if data == "YES":
                print("Authentication is successful")

                #For Refreshing the session in case of n<=2
                print(type(data_n),data_n)
                if data_n == "2":
                    data = s.recv(BUFFERSIZE)
                    data = data.decode().rstrip()
                    if data == "REFRESH":
                        print("Session is about to expire....Refreshing the session")
                        n_val = input("Enter value of integer n: ")
                        password = input("Enter password: ")
                        salt = input("Enter salt: ")
                        #Compute hash^n(pass)
                        hashpass = lamport.genHashwithSalt(password,salt,int(n_val))
                        print(type(hashpass))
                        print(hashpass)
                        s.send(n_val.ljust(BUFFERSIZE).encode())
                        s.send(hashpass.ljust(BUFFERSIZE).encode())
                        s.send(salt.ljust(BUFFERSIZE).encode())
            else:
                print("Authentication failed")
        elif x==2:
            s.close()
            sys.exit()

if __name__ == '__main__':
    main()





    