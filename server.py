import socket
import pickle
import numpy as np
import threading

def start_game(conn1,conn2):
    board = np.zeros((3,3))
    c1.send("GAME STARTED:".encode())
    c2.send("GAME STARTED:".encode())
        
    while True:
        end,player = is_game_over(board)
        if end:
            break
        
        conn1.send(pickle.dumps(board))

        action = conn1.recv(1024)

        action = pickle.loads(action)
        board = next_board(board,action,p=1)
        
        
        end,player = is_game_over(board)
        if end:
            break
        
        conn2.send(pickle.dumps(board))
        action = conn2.recv(1024)
        action = pickle.loads(action)
        board = next_board(board,action,p=-1)
    if player ==1:
        conn1.send(pickle.dumps("You win"))
        conn2.send(pickle.dumps("You lost"))
    elif player ==-1:
        conn1.send(pickle.dumps("You lost"))
        conn2.send(pickle.dumps("You win"))
    else:
        conn1.send(pickle.dumps("The match is a draw"))
        conn2.send(pickle.dumps("The match is a draw"))
    
    conn1.close()
    conn2.close()


def PrintBoard(state):
    mapping = {1: "X", 0: " ", -1: "O"}
    i = 0
    for row in state:
        print(" "+mapping.get(row[0])+" |"" "+mapping.get(row[1])+" |"" "+mapping.get(row[2]))
        i+=1
        if (i<3):  
            print(11*"-")

def next_board(board,move,p=1):
    row, column = (move-1)//3, (move-1)%3
    if board[row,column]==0:  
        board[row, column] = p
    return board

def is_game_over(board):
    for i in range(3):
        if np.sum(board[i])==3 or np.sum(board[:,i])==3:
            return True,1
        if np.sum(board[:,i])==-3 or np.sum(board[:,i])==-3:
            return True,-1
    if np.sum(np.diag(board))==3 or np.sum(np.diag(board[::-1]))==3:
        return True,1
    if np.sum(np.diag(board))==-3 or np.sum(np.diag(board[::-1]))==-3:
        return True,-1
    if np.sum(board==0)==0:
        return True,0
    return False,0

host_name = 'localhost'
hostip = socket.gethostbyname(host_name)
port = 65432

#hostip = '192.168.137.232'
#port = 65432



server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((hostip,port))

server_sock.listen()


threads=[]
i=0
while True:

    c1,add = server_sock.accept()
    c1.send("Searching for other player...".encode())
    
    c2,add = server_sock.accept()
    c2.send("Searching for other player...".encode())
    
    thread = threading.Thread(target=start_game,args=(c1,c2,))

    threads.append(thread)
    
    threads[-1].start()
    
    if  i==1:
        break
    i+=1

for t in threads:
    t.join()

server_sock.close()