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
        """Print the board positions of all pieces on the board"""
        for i in self.fields.keys():
            #print(i)
            if self.fields[i]["piece"].player != 0:
                print("%s on %s" % (self.fields[i]["piece"].name,
                                    self.fields[i]["fieldName"])
                      )

    def playersPieces(self, id, type=""):
        """Return the board positions of all pieces of a specified player.
        When type is specified, one can restict output to s, f, or g fields"""
        pos = []
        for i in [j for j in self.fields.keys() if j.startswith(type)]:
            if self.fields[i]["piece"].player == id:
                pos.append(i)
        return pos

    def movePiece(self, fkey1, fkey2):
            self.fields[fkey2]["piece"], self.fields[fkey1]["piece"] = self.fields[fkey1]["piece"], self.fields[fkey2]["piece"]

    def kickBackToWhere(self, player):
        """Which of `player`'s starting (board) fields to kick back to"""
        if len(self.playersPieces(player, "f")) == 0: raise ValueError("Cannot kick out player with 0 active pieces.")
        else: return "s%d%d" % (player, len(self.playersPieces(player, "s")) +1)
        
        
    def startFromWhere(self, player):
        """From which of `player`'s starting (board) fields to move out"""
        if len(self.playersPieces(player, "s")) == 0: raise ValueError("Cannot start, all pieces active.")
        else: return "s%d%d" % (player, len(self.playersPieces(player, "s")))
    
    def isPlayerOnField(self, bf, playerId):
        return (self.fields[bf]["piece"].player == playerId)
    
    def isOtherPlayerOnField(self, bf, playerId):
        others = [1, 2, 3, 4]
        others.pop(playerId - 1) 
        return (self.fields[bf]["piece"].player in others)
    
    def iNotOnStart(self, playerId):
        return not self.isPlayerOnField(pf2bf(0, playerId), playerId)
    
    def kickOutFromPf(self, pf):
        bf = pf2bf(pf, self.currentPl())
        # add recording code here
        self.movePiece(bf,
                       self.kickBackToWhere(self.fields[bf]["piece"].player)
                       )
    def noGapsInGoal(self, pl):
        myGoalPoss = self.playersPieces(self.currentPl(), "g")
        if len(myGoalPoss) == 0: return True
        myGoalPlPoss = bfl2pfl(myGoalPoss, self.currentPl())
        if min(myGoalPlPoss) < 44 - len(myGoalPoss):
            return False
        else:
            #print("No gaps in goal. Having another roll!")
            return True

    def hasPlFinished(self, pl):

        return len(self.playersPieces(pl, "g")) == 4

    def finishProc(self, pl):
        self.winningOrder.append(pl)
        # add recording code here
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
            myGoalPoss = self.playersPieces(self.currentPl(), "g")
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
        
    def moveWhich(self, bfl, d):
        nonStartBFL = [i for i in bfl if not i.startswith("s")]
        nonStartPFL = bfl2pfl(nonStartBFL)
        targs = [i + d for i in nonStartPFL]
        
        # 0 if I on targ, 1 else
        iOnTarg = [(not self.isPlayerOnField(pf2bf(i), self.currentPl())) * 1  if i < 44 else True for i in targs]
        
        # 0 if not, 4 if yes, 0 if beyond goal
        otherOnTarg = [self.isOtherPlayerOnField(pf2bf(i), self.currentPl()) * 4  if i < 44 else 0 for i in targs]
        #otherOnTarg = [1 for _ in targs] # to turn off Schlagzwang
        
        onStartField = [(i == 0) * 8 for i in nonStartPFL] # 0 or 8

        onGoalField = [(not i.startswith("g")) * 2 for i in nonStartBFL] # 0 or 2

        priorities = [iOnTarg[i] * ((otherOnTarg[i] + onStartField[i] + onGoalField[i]) + 1) for i in range(len(targs))]

        mPr = max(priorities)
        if mPr == 0: #can't move
            return -1
        else:
            favsBFL = [nonStartBFL[i] for i in range(len(targs)) if priorities[i] == mPr]
            favsPFL = [nonStartPFL[i] for i in range(len(targs)) if priorities[i] == mPr]
            if len(favsBFL) == 1:
                return favsBFL[0]
            else:
                firstPF = max(favsPFL)
                firstBF = [favsBFL[i] for i in range(len(targs))if favsPFL[i] == firstPF][0]
                return firstBF


    def oneMove(self, attempt=1):
        if self.currentPl() in self.winningOrder:
            
            #printBoard(self)
            return
        
        roll = 1
        d = rollDie()
        if not self.np:
            sleep(0.01)
            clearScreen()  
        #print("###################")
        #d = 1
        #print("Rolled a %d" % d, end="")
            print("Turn %d - %s" % (self.turn, self.playerColours[self.currentPl()-1].upper()))
            print("Rolled a %d" % d)
        # my board pos
        myPositions = self.playersPieces(self.currentPl(), "f")
        allMyPoss = self.playersPieces(self.currentPl())
        
        mineOnBoard = len(myPositions)

        #my pl pos
        myPlPos = bfl2pfl(myPositions, self.currentPl())
        myPlPos.sort()

        if d == 6:
            #print("6!")
            if len(self.playersPieces(self.currentPl(), "s")) > 0: #there is a piece to move out
                #print("There's somebody waiting to go!")

                if self.iNotOnStart(self.currentPl()): # player not on own start
                    #print("I'm not on start.")
                    # if other player on start, kick out
                    if self.isOtherPlayerOnField(pf2bf(0, self.currentPl()), self.currentPl()):
                        #print("***There's somebody on my start, KICK!***")
                        self.kickOutFromPf(0)

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
        else: # if no 6 and there are some on the boar or gaps in the goal
            if self.iNotOnStart(self.currentPl()):
                self.movingProcedure(myPlPos, d, "std")
                #self.moveWhich(allMyPoss, d)
            else: # player self on own start
                self.movingProcedure(myPlPos[::-1], d, "std")
        #clearScreen()
        if not self.np:
            printBoard(self)
        if self.hasPlFinished(self.currentPl()): self.finishProc(self.currentPl())


        
