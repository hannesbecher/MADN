#The game


from game import *
from utils import *
from plotting import * 
from time import sleep, time

if __name__ == "__main__":

    t0 = time()
    nPl = 4
    
    #np = True
    np = False
    board = Board(nPl, np)
    [setUpPlayer(board, i+1, board.playerColours[i]) for i in range(nPl)]

    
    #board.movePiece("s14", "f00")
    #board.movePiece("s24", "f20")
    #board.movePiece("s34", "f10")
    #board.movePiece("s44", "f30")
    #printBoard(board)
    while True:
        board.turn += 1
        board.oneMove()
        board.nextPl()
        
        if len(board.winningOrder) == nPl - 1:
            print(board.winningOrder)
            break
        #if turn == 40: break

print("Game over.")
print(time() - t0)