#The script to run when package is run non-interactively

from madn.top import oneGame
if __name__ == "__main__":

    oneGame(noPrint=False, nPl=4)
    #print(oneGame(noPrint=True, nPl=4, seed=12345))
    #oneGame(noPrint=True))
