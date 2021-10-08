#The game


from game import *
from utils import *
from plotting import * 
from time import sleep, time

if __name__ == "__main__":

    t0 = time()
    nPl = 4 # number of players
    
    #noPrint = True
    noPrint = False
    board = Board(nPl, noPrint)
    [initialisePlayerPieces(i+1, board) for i in range(nPl)]
    

    while True:
        board.turn += 1
        board.oneMove()
        board.nextPl()
        
        if len(board.winningOrder) == nPl - 1:
            print("Finishing order: " + " ".join([board.playerColours[i-1].upper() for i in board.winningOrder]))
            print(f"Turn {board.turn}")
            #printBoard(board)
            break
        #if turn == 40: break

print("Game over.")
print(time() - t0)