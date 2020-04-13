### Student: Joseph Greene
### Class:   CSC401
### Title:   Socket Project
### Date:    10/2/2019

## This is the Client Program for our Prisoner's Dilemma Game
# It attempts to connect to the server to play the game
# If two players have already connected, this program gets rejected
# If a spot is open, the game begins!



#Importing the socket library
import socket
#Importing the system library
import sys

#Creating a socket
#IPv4 and over TCP connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connecting to the host on port 3000
s.connect((sys.argv[1], int(sys.argv[2])))
#serversocket, address = s.accept();
#Recieves data in chunks of data of buffer size 1024
message = s.recv(1024)
isFull = b"full" in message
#The game is full
if isFull:
    #Print full message
    print(message.decode("utf-8"))
    #Close Socket
    s.close()
#The game has a spot avaliable
else:
    #Print game assignment message
    if b"1" in message:
        #Handles prisoner 1
        print(message.decode("utf-8"))
        print("Waiting for prisoner 2.")
    else:
        #Handles prisoner 2
        print(message.decode("utf-8"))
        print("Let's begin >:)")
    
    #Waiting for game to start
    message = s.recv(1024)
    
    
    #Prints the game instructions
    print(message.decode("utf-8"))
    #Start of Game
    isQuestioning = True
    while isQuestioning:
        response = str(raw_input())
        if response == "B" or response =="C":
            isQuestioning = False
        else:
            print("Please specify 'B' or 'C'")
    s.send(response)
    print("Please wait for your sentence")
    #Wait for sentence
    message = s.recv(1024)
    print(message.decode("utf-8"))
    
    #Close the socket after the sentence is recieved
    print("Interrogation over, disconnecting from jail server.")
    s.close();
    