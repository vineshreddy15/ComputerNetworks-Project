import socket
import pickle
import numpy as np

def PrintBoard(state):
    mapping = {1: "X", 0: " ", -1: "O"}
    i = 0
    for row in state:
        print(" "+mapping.get(row[0])+" |"" "+mapping.get(row[1])+" |"" "+mapping.get(row[2]))
        i+=1
        if (i<3):  
            print(11*"-")



host_name = 'localhost'
HOST = socket.gethostbyname(host_name) 
PORT = 65432       

#HOST = '192.168.137.232'
#PORT = 65432


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    msg = s.recv(1024).decode()
    print(msg)
    msg = s.recv(1024).decode()
    print(msg)

    while True:
        board = s.recv(1024)
        board = pickle.loads(board)
        if type(board)==str:
            print(board)
            break
        print("other player:")
        PrintBoard(board)
        action = int(input("enter the action:"))
        s.send(pickle.dumps(action))

         
