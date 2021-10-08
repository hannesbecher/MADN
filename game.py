from random import randint
from utils import *
from time import sleep
from plotting import * 

def rollDie():
    return randint(1,6)

class Piece:
    def __init__(self, playerId, playerPieceId, colour, bgcol="grey"):
        self.player = playerId
        self.ppid = playerPieceId
        self.name = "piece %d of player %d" % (playerPieceId, playerId)
        self.colour = colour
        self.bgcol = bgcol

def makeGhostPiece():
    """These are located on empty fields."""
    return Piece(0, 0, "white")


def initialisePlayerPieces(playerId, board):
    if playerId in [1, 2, 3, 4]:
        for i in [1, 2, 3, 4]:
            board.fields["s%s%d" % (playerId, i)]["piece"] = Piece(playerId, i, board.playerColours[playerId-1])
    else: raise ValueError("playerId has to be between 1 and 4.")


class Board():
    
    def __init__(self, nPl=4, noPrint=False):
        self.fields = {("f%02d" % i):{"nextField":("f%02d" % (i+1)),
                                      "fieldName":"board field %02d" % i,
                                      "piece":makeGhostPiece()
                                      } for i in range(40)}
        #self.fields["f40"]={"nextField":"f01", "piece":makeGhostPiece(), "fieldName":"field 40"}
    
        #starting fields
        for i in range(4):
            for j in range(4):
                self.fields["s%d%d" % (i+1,j+1)]={"piece":makeGhostPiece(), "fieldName":"starting field %d of player %d" % (j+1,i+1)}
       
        #goal fields
        for i in range(4):
            for j in range(4):
                self.fields["g%d%d" % (i+1,j)]={"piece":makeGhostPiece(), "fieldName":"goal field %d of player %d" % (j,i+1)}
        
        self.np = noPrint
        self.turn = 1
        self.plOrder = [1,2,3,4][:nPl]
        
        self.playerColours = ["red", "green", "cyan", "yellow"][:nPl]
        self.winningOrder = []
        
    def currentPl(self):
        return self.plOrder[0]
        
    def nextPl(self):
        self.plOrder = self.plOrder[1:] + [self.plOrder[0]]
        
    def state(self):
        """Print the positions of all pieces on the board"""
        for i in self.fields.keys():
            #print(i)
            if self.fields[i]["piece"].player != 0:
                print("%s on %s" % (self.fields[i]["piece"].name,
                                    self.fields[i]["fieldName"])
                      )
    def playersPiecesInGame(self, id):
        """Return the board positions (only f-ones) of all pieces of a specified player"""
        pos = []
        for i in [j for j in self.fields.keys() if j.startswith("f")]:
            if self.fields[i]["piece"].player == id:
                pos.append(i)
        return pos

    def playersPiecesInStart(self, id):
        """Return the s positions of all pieces of a specified player"""
        pos = []
        for i in [j for j in self.fields.keys() if j.startswith("s")]:
            if self.fields[i]["piece"].player == id:
                pos.append(i)
        return pos

    def playersPiecesInGoal(self, id):
        """Return the board ("g") positions of all pieces of a specified player"""
        pos = []
        for i in [j for j in self.fields.keys() if j.startswith("g")]:
            if self.fields[i]["piece"].player == id:
                pos.append(i)
        return pos

    def movePiece(self, fkey1, fkey2):
            self.fields[fkey2]["piece"], self.fields[fkey1]["piece"] = self.fields[fkey1]["piece"], self.fields[fkey2]["piece"]

    def kickBackToWhere(self, player):
        """Which of `player`'s starting (board) fields to kick back to"""
        if len(self.playersPiecesInGame(player)) == 0: raise ValueError("Cannot kick out player with 0 active pieces.")
        else: return "s%d%d" % (player, len(self.playersPiecesInStart(player)) +1)
        
        
    def startFromWhere(self, player):
        """From which of `player`'s starting (board) fields to move out"""
        if len(self.playersPiecesInStart(player)) == 0: raise ValueError("Cannot start, all pieces active.")
        else: return "s%d%d" % (player, len(self.playersPiecesInStart(player)))
    
    def isPlayerOnField(self, bf, playerId):
        return (self.fields[bf]["piece"].player == playerId)
    
    def isOtherPlayerOnField(self, fieldId, playerId):
        others = [1, 2, 3, 4]
        others.pop(playerId - 1) 
        return (self.fields[fieldId]["piece"].player in others)
    
    def iNotOnStart(self, playerId):
        return not self.isPlayerOnField(pf2bf(0, playerId), playerId)
    
    def kickOutFromPf(self, pf):
        bf = pf2bf(pf, self.currentPl())
        self.movePiece(bf,
                       self.kickBackToWhere(self.fields[bf]["piece"].player)
                       )
    def noGapsInGoal(self, pl):
        myGoalPoss = self.playersPiecesInGoal(self.currentPl())
        if len(myGoalPoss) == 0: return True
        myGoalPlPoss = bfl2pfl(myGoalPoss, self.currentPl())
        if min(myGoalPlPoss) < 44 - len(myGoalPoss):
            return False
        else:
            #print("No gaps in goal. Having another roll!")
            return True

    def hasPlFinished(self, pl):

        return len(self.playersPiecesInGoal(pl)) == 4

    def finishProc(self, pl):
        self.winningOrder.append(pl)
        if not self.np:
            #print("Player %d finishes with position %d" % (self.currentPl(), len(self.winningOrder)))
            print("Player %s finishes with position %d" % (self.playerColours[self.currentPl()-1].upper(), len(self.winningOrder)))
            sleep(1)

    def movingProcedure(self, startPfList, steps, situation="std"):
        
        if len(startPfList) == 0: # if no one movable in game
            if situation == "goal": # meaning we've done this already
                #print("All goalies tried w/o sucess. Passing.")
                return
            #any in goal to move?
            #print("None in game, check goal!")
            myGoalPoss = self.playersPiecesInGoal(self.currentPl())
            #print(myGoalPoss)
            if len(myGoalPoss) > 0:
                myGoalPlPoss = bfl2pfl(myGoalPoss, self.currentPl())
                self.movingProcedure(myGoalPlPoss, steps, "goal") 

            else: # if none in goal pass this turn
                #printBoard(self)
                return
        else:
            chosenOne = startPfList.pop() # this is a player field number
            #print("Chose to move from %s - pf %s" % (pf2bf(chosenOne, self.currentPl()), chosenOne))
            targ = chosenOne + steps
            if targ < 44:
                if self.isPlayerOnField(pf2bf(targ, self.currentPl()),
                                        self.currentPl()
                                        ):
                    #print("I'm on that field. Trying next piece...")
                    self.movingProcedure(startPfList, steps, situation) # trying remaining
                    #return #not needed?
                if self.isOtherPlayerOnField(pf2bf(targ, self.currentPl()), self.currentPl()):
                    #print("Kicking out...")
                    self.kickOutFromPf(targ)
                self.movePiece(pf2bf(chosenOne, self.currentPl()),
                               pf2bf(targ, self.currentPl())
                               )
                #printBoard(self)
                #return #not needed?
            else:
                #print("No fields left to go to. Trying next piece...")
                self.movingProcedure(startPfList, steps, situation) # trying remaining
                #return #not needed?
        


    def oneMove(self, attempt=1):
        if self.currentPl() in self.winningOrder:
            
            #printBoard(self)
            return
        
        roll = 1
        d = rollDie()
        if not self.np:
            sleep(0.02)
            clearScreen()  
        #print("###################")
        #d = 1
        #print("Rolled a %d" % d, end="")
            print("Turn %d - %s" % (self.turn, self.playerColours[self.currentPl()-1].upper()))
            print("Rolled a %d" % d)
        # my board pos
        myPositions = self.playersPiecesInGame(self.currentPl())
        mineOnBoard = len(myPositions)

        #my pl pos
        myPlPos = bfl2pfl(myPositions, self.currentPl())
        myPlPos.sort()

        if d == 6:
            #print("6!")
            if len(self.playersPiecesInStart(self.currentPl())) > 0: #there is a piece to move out
                #print("There's somebody waiting to go!")

                if self.iNotOnStart(self.currentPl()): # player not on own start
                    #print("I'm not on start.")
                    # if other player on start, kick out
                    if self.isOtherPlayerOnField(pf2bf(0, self.currentPl()), self.currentPl()):
                        #print("***There's somebody on my start, KICK!***")
                        
                        self.movePiece(pf2bf(0, self.currentPl()),
                                       self.kickBackToWhere(self.fields[pf2bf(0, self.currentPl())]["piece"].player)
                                       )
                    # move out piece
                    #print("Moving out!")
                    self.movePiece(self.startFromWhere(self.currentPl()),
                                   pf2bf(0, self.currentPl())
                                   )
                else:
                    #print("I'm on my start. Try to clear!")
                    # moving procedure with inverted order
                    self.movingProcedure(myPlPos[::-1], d, "std")
            else: # if none left to move out
                self.movingProcedure(myPlPos, d, "std")
            #print("Doing my 2nd move!")
            if not self.np:
                printBoard(self)        
            self.turn += 1 # count 2nd turn extra
            self.oneMove()
            return # important
        elif (mineOnBoard == 0) and (self.noGapsInGoal(self.currentPl())) and (attempt < 3):
            #print("""Can't move, attempt %d""" % (attempt + 1))
            
            if not self.np:
                printBoard(self)
            # these are not counted extra because there is no actual move happening
            # until a 6 is rolled
            self.oneMove(attempt=attempt+1) 
            return
        else: # if no 6
            if self.iNotOnStart(self.currentPl()):
                self.movingProcedure(myPlPos, d, "std")
            else: # player self on own start
                self.movingProcedure(myPlPos[::-1], d, "std")
        #clearScreen()
        if not self.np:
            printBoard(self)
        if self.hasPlFinished(self.currentPl()): self.finishProc(self.currentPl())

    # end oneMove            
        # if not, is 6
            # if not, re-roll...
        # if yes, is start empty?
            # if not, can manke empty?...
                #if not, move other
            # if yes, can first piece move?
#def initialPos(playerId, board):
        
