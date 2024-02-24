


from madn.game import Board, initialisePlayerPieces
from time import sleep, time
import random


def oneGame(nPl=4, noPrint=True, tak=["k", "k", "k", "k"], seed=None):
    t0 = time()
    board = Board(nPl, noPrint, tak)
    
    if seed != None: random.seed(seed)
    
    [initialisePlayerPieces(board, i+1) for i in range(nPl)]
    
    # The game main loop
    while True:
        board.oneMove()
        board.nextPl()
        
        if len(board.events["finishingOrder"]) == nPl - 1:
            break
        #if board.turn == 20: break
    
    # Finishing off
    if noPrint == False:
        print("Game over.")
        print("%.3f s." % (time() - t0))
        print("Finishing order: " + " ".join([board.playerColours[i-1].upper() for i in board.events["finishingOrder"]]))
        print(f"Turn {board.turn}")
    
    return board.events
