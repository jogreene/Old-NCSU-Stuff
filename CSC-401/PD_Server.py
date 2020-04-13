### Student: Joseph Greene
### Class:   CSC401
### Title:   Socket Project
### Date:    10/2/2019

## This is the Server Program for our Prisoner's Dilemma Game
# It continously waits for clients to connect
# Once two clients have connected the game, the program creates a thread for the game to begin
# If another client attempts to connect while a game is being played, that client is rejected
# Once the game is finished, clients will be accepted again


#Importing the socket library
import socket
#Importing the thread library
import thread
#Importing the system library
import sys

#Global variable to keep track of if a game is going on
inGame = False

#The function that plays the game.
#Takes in the sockets of the two prisoner clients as parameters
def playGame(socket1, socket2):
    global inGame

    #Prompt for choice
    socket1.send("Enter Cooperate(C) or Betray(B):")
    socket2.send("Enter Cooperate(C) or Betray(B):")
    print("Game has begun.")
    #Recieve the responses
    response1 = socket1.recv(1024);
    response2 = socket2.recv(1024);
    choice1 = 0
    choice2 = 0
    time1 = 0
    time2 = 0
    #Parses the first choice
    if b"B" in response1:
        #Code will Betray if B is found in the response
        choice1 = "B"
    else:
        #Code will Cooperate by default if betray is not specified
        choice1 = "C"
    #Parses the second choice
    if b"B" in response2:
        choice2 = "B"
    else:
        #Code will Cooperate by default if betray is not specified
        choice2 = "C"
    
    #If both betray, each get two years    
    if choice1 == "B" and choice2 == "B":
        time1 = 2
        time2 = 2
    #If both cooperate, each get one year
    elif choice1 == "C" and choice2 == "C":
        time1 = 1
        time2 = 1
    #If prisoner 1 betrays prisoner 2, prisoner 2 gets three years and prisoner 1 goes free
    elif choice1 == "B" and choice2 == "C":
        time1 = 0
        time2 = 3
        #If prisoner 2 betrays prisoner 1, prisoner 1 gets three years and prisoner 2 goes free
    elif choice1 == "C" and choice2 == "B":
        time1 = 3
        time2 = 0
            
    #Send the prisoners their sentence
    socket1.send("You are sentenced to %d year(s)." % (time1))
    socket2.send("You are sentenced to %d year(s)." % (time2))
    
    #Report results to the server
    print("Prisoner 1 recieved a sentenced of %d year(s)" % (time1))
    print("Prisoner 2 recieved a sentenced of %d year(s)" % (time2))
    print("Waiting on more players to begin the next game!")
    #Exit the thread
    inGame = False;
    thread.exit()


#Creating a socket
#IPv4 and over TCP connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Ports must be in the range of 3000 - 5000 to work on the VCL
port = sys.argv[1]
hostName = socket.gethostname()
ip = socket.gethostbyname(hostName)
s.bind((ip, int(port)))
#Puts the socket into listening mode with a queue of 5
s.listen(5)
print("The interrogation server is up and ready to go!")

playerNum = 0
clientSocket1 = 0
clientSocket2 = 0

#Infinite loop of the server running games
while True:
    #This starts the game when two players are ready
    if playerNum == 2 and not inGame:
        print("We got two!")
        #clientSocket1.send(bytes("Enter Cooperate(C) or Betray(B):", "utf-8"))
        #clientSocket2.send(bytes("Enter Cooperate(C) or Betray(B):", "utf-8"))
        inGame = True
        playerNum = 0
        thread.start_new_thread(playGame, (clientSocket1, clientSocket2)) 
    
    #Accepts a new client
    clientsocket, address = s.accept();
    print("A new prisoner from %r is trying to enter the game!" % (address[0]))
    
    #Queues up a player for a game
    if playerNum < 2 and not inGame:
        playerNum += 1
        #Tells the client they are in the game
        clientsocket.send("You are Prisoner %d, goodluck..." % playerNum)
        print("Prisoner was assigned the role of Prisoner %d." % playerNum)
        #Assigns the player their socket
        if playerNum == 1:
            clientSocket1 = clientsocket
        elif playerNum == 2:
            clientSocket2 = clientsocket
    else:
        #A game is already going on so the player is rejected
        print("Server is too busy and the new prisoner was rejected.")
        clientsocket.send("Server is full, come back later.")
    
