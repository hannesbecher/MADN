from random import randint

from madn.utils import bf2pf, pf2bf, bfl2pfl
from time import sleep
from madn.plotting import clearScreen, printBoard


def rollDie():
    return randint(1, 6)


class Piece:
    """
    A class to represent pieces (including ghost pieces on empty fields)

    Keyword args:
    playerId -- an integer
    playerPieceId -- an integer
    colour -- string
    bgcol -- background colour?, a string (default: "grey")
    """
    def __init__(self, playerId, playerPieceId, colour, bgcol="grey"):
        self.player = playerId
        self.ppid = playerPieceId
        self.name = "piece %d of player %d" % (playerPieceId, playerId)
        self.colour = colour
        self.bgcol = bgcol


def makeGhostPiece():
    """Returns white a piece object eloning to no player. These are located on
    empty fields.
    """
    return Piece(0, 0, "white")


def initialisePlayerPieces(board, playerId):
    """
    Places a player's pieces in starting position by mutating `board`. This is
    run once for each player. Used in oneGame().
    """
    assert isinstance(playerId, int), "Argument `playerId` must be `int`."
    assert isinstance(board, Board), "Argument `board ` must be `Board`."
    if playerId in [1, 2, 3, 4]:
        for i in [1, 2, 3, 4]:
            board.fields["s%s%d" % (playerId, i)]["piece"] = Piece(
               playerId, i, board.playerColours[playerId-1])
    else:
        raise ValueError("playerId must be between 1 and 4.")


class Board():
    """
    The main class of the game.
    """
    def __init__(self, nPl=4, noPrint=False, tak=["k", "k", "k", "k"]):
        # set up fields
        # 40 ordinary fileds
        self.fields = {("f%02d" % i): {
            "nextField": ("f%02d" % (i+1)),
            "fieldName": "board field %02d" % i,
            "piece": makeGhostPiece()} for i in range(40)}
        # self.fields["f40"]={"nextField":"f01", "piece":makeGhostPiece(), "fieldName": "field 40"}

        # 16 starting fields
        for i in range(4):
            for j in range(4):
                self.fields["s%d%d" % (i+1, j+1)] = {
                    "piece": makeGhostPiece(),
                    "fieldName": "starting field %d of player %d" % (j+1, i+1)}
       
        # 16 goal fields
        for i in range(4):
            for j in range(4):
                self.fields["g%d%d" % (i+1,j)]={"piece":makeGhostPiece(), "fieldName":"goal field %d of player %d" % (j,i+1)}
        
        # whether or not to print board state on oneTurn() 
        self.np = noPrint
        
        
        self.tactics = tak
        self.turn = 0
        self.plOrder = [1,2,3,4][:nPl]
        
        # these colour must match vals in plotting.py
        self.playerColours = ["red", "green", "cyan", "yellow"][:nPl]
        #self.playerColours = ["reds", "green", "cyan", "yellow"][:nPl] # will fail
        
        # dict of interesting stuff
        self.events = {"finishingOrder":[], 
                       "finishingTurns":[], 
                       "kickingTurns":[], 
                       "kickingWho":[],
                       "whoField":[], # field were the kick happens in pf notation for who
                       "kickingWhom":[],
                       "whomField":[] # field were the kick happens in pf notation for whom
                       }
            

    def currentPl(self):
        """
        Returns the current player (int)
        """
        return self.plOrder[0]
        
    def nextPl(self):
        """
        Updates the player order (ready for the next turn).
        """
        self.plOrder = self.plOrder[1:] + [self.plOrder[0]]
        
    def printState(self):
        """
        Print the board positions of all pieces on the board as text.
        """
        for i in self.fields.keys():
            #print(i)
            if self.fields[i]["piece"].player != 0:
                print("%s on %s" % (self.fields[i]["piece"].name,
                                    self.fields[i]["fieldName"])
                      )

    def playersPieces(self, id, type=""):
        """
        Returns the board positions of all pieces of a specified player.
        When `type` is specified, one can restict output to s, f, or g
        fields.
        """
        pos = []
        for i in [j for j in self.fields.keys() if j.startswith(type)]:
            if self.fields[i]["piece"].player == id:
                pos.append(i)
        return pos

    def movePiece(self, frto):
        """
        Low-level moving method. It swaps the pieces on the two fields
        given in `frto`. This is not usually called directly. It does
        not check wether a move is valid.
        """
        assert isinstance(frto, tuple), "Argument `frto` must be a tuple of lenght==2."
        assert len(frto) == 2, "Argument `frto` must be a tuple of lenght==2."
        
        fkey1, fkey2 = frto
        self.fields[fkey2]["piece"], self.fields[fkey1]["piece"] = self.fields[fkey1]["piece"], self.fields[fkey2]["piece"]

    def kickBackToWhere(self, player):
        """
        Which of `player`'s starting (board) fields to kick back to
        """
        if len(self.playersPieces(player, "f")) == 0: raise ValueError("Cannot kick out player with 0 active pieces.")
        else: return "s%d%d" % (player, len(self.playersPieces(player, "s")) +1)
        
        
    def startFromWhere(self, player):
        """
        From which of `player`'s starting (board) fields to move out
        """
        if len(self.playersPieces(player, "s")) == 0: raise ValueError("Cannot start, all pieces active.")
        else: return "s%d%d" % (player, len(self.playersPieces(player, "s")))
    
    def isPlayerOnField(self, bf, playerId):
        """
        Returns (logical) whether player `playeId` has a piece on board
        field `bf`.
        """
        return (self.fields[bf]["piece"].player == playerId)
    
    def isOtherPlayerOnField(self, bf, playerId):
        """
        Returns (logical) whether any player except `playeId` has a
        piece on board field `bf`.
        """
        others = [1, 2, 3, 4]
        others.pop(playerId - 1) 
        return (self.fields[bf]["piece"].player in others)
    
    def iNotOnStart(self, playerId):
        """
        Returns `True` player `playerId` has no piece on their start
        field.
        """
        return not self.isPlayerOnField(pf2bf(0, playerId), playerId)

    def kickOutFromBf(self, bf):
        """
        Kicks out a piece from a specified board field and records
        relevant events. This is called by moveAndKick(), which deals
        with the kicking piece's move.
        """
        self.events["kickingTurns"].append(self.turn) 
        self.events["kickingWho"].append(self.currentPl())
        self.events["whoField"].append(bf2pf(bf, self.currentPl()))
        self.events["kickingWhom"].append(self.fields[bf]["piece"].player)
        self.events["whomField"].append(bf2pf(bf, self.fields[bf]["piece"].player))
        
        self.movePiece((bf,
                       self.kickBackToWhere(self.fields[bf]["piece"].player))
                       )

    def moveAndKick(self, frto):
        """
        Removes piece from target field and then moves focal piece.
        """
        if frto[0] != -1:
            if self.isOtherPlayerOnField(frto[1], self.currentPl()):
                self.kickOutFromBf(frto[1])
            self.movePiece(frto)

    def noGapsInGoal(self, pl):
        """
        Returns (logical) whether player `pl` has gaps between their
        pieces in goal.
        """
        myGoalPoss = self.playersPieces(self.currentPl(), "g")
        if len(myGoalPoss) == 0: return True
        myGoalPlPoss = bfl2pfl(myGoalPoss, self.currentPl())
        if min(myGoalPlPoss) < 44 - len(myGoalPoss):
            return False
        else:
            #print("No gaps in goal. Having another roll!")
            return True

    def hasPlFinished(self, pl):
        """
        Returns (logical) whether all of player `pl`'s pieces are in
        goal.
        """
        return len(self.playersPieces(pl, "g")) == 4

    def finishProc(self, pl):
        """
        Procedure that is run once a player finishes.
        """
        self.events["finishingOrder"].append(pl)
        self.events["finishingTurns"].append(self.turn)
        if not self.np:
            print("Player %s finishes with position %d" % (self.playerColours[self.currentPl()-1].upper(), len(self.events["finishingOrder"])))
            sleep(1)

        
    def moveWhich(self, bfl, d, tak="k"):
        """
        Takes a list of board fields where the current player's
        pieces are and the number rolled. Returns which board fields to
        move from and to.
        """
        nonStartBFL = [i for i in bfl if not i.startswith("s")]
        if len(nonStartBFL) == 0:
            return -1, -1
        nonStartPFL = bfl2pfl(nonStartBFL, self.currentPl())
        targs = [i + d for i in nonStartPFL]
        
        # 0 if I on targ, 1 else
        iOnTarg = [(not self.isPlayerOnField(pf2bf(i, self.currentPl()), self.currentPl())) * 1  if i < 44 else 0 for i in targs]
        #print(iOnTarg)
        # 0 if not, 4 if yes, 0 if beyond goal
        if tak == "k": # if tactic is to kick out
            otherOnTarg = [self.isOtherPlayerOnField(pf2bf(i, self.currentPl()), self.currentPl()) * 4  if i < 44 else 0 for i in targs]
        else:
            otherOnTarg = [1 for _ in targs] # to turn off Schlagzwang
        
        onStartField = [(i == 0) * 8 for i in nonStartPFL] # 0 or 8

        onGoalField = [(not i.startswith("g")) * 2 for i in nonStartBFL] # 0 or 2

        priorities = [iOnTarg[i] * ((otherOnTarg[i] + onStartField[i] + onGoalField[i]) + 1) for i in range(len(targs))]
        #print(priorities)
        mPr = max(priorities)
        if mPr == 0: #can't move
            return -1, -1
        else:
            favsBFL = [nonStartBFL[i] for i in range(len(targs)) if priorities[i] == mPr]
            favsPFL = [nonStartPFL[i] for i in range(len(targs)) if priorities[i] == mPr]
            if len(favsBFL) == 1:
                return favsBFL[0], pf2bf(favsPFL[0] + d, self.currentPl())
            else:
                firstPF = max(favsPFL)
                firstBF = [favsBFL[i] for i in range(len(favsBFL))if favsPFL[i] == firstPF][0]
                return firstBF, pf2bf(firstPF + d, self.currentPl())


    def oneMove(self, attempt=1):
        if self.currentPl() in self.events["finishingOrder"]:
            
            #printBoard(self)
            return
        if attempt == 1:
            self.turn += 1
        roll = 1
        d = rollDie()
        if not self.np:
            sleep(0.01)
            clearScreen()  
            #print("###################")

            print("Turn %d - %s" % (self.turn, self.playerColours[self.currentPl()-1].upper()))
            print("Rolled a %d" % d)
        # my board pos
        myPositions = self.playersPieces(self.currentPl(), "f")
        allMyPoss = self.playersPieces(self.currentPl())
        mineOnBoard = len(myPositions)

        if d == 6:
            #print("6!")
            if len(self.playersPieces(self.currentPl(), "s")) > 0: #there is a piece to move out
                #print("There's somebody waiting to go!")

                if self.iNotOnStart(self.currentPl()): # player not on own start
                    #print("I'm not on start.")
                    # if other player on start, kick out
                    if self.isOtherPlayerOnField(pf2bf(0, self.currentPl()), self.currentPl()):
                        #print("***There's somebody on my start, KICK!***")
                        self.kickOutFromBf(pf2bf(0, self.currentPl()))

                    # move out piece
                    #print("Moving out!")
                    self.movePiece((self.startFromWhere(self.currentPl()),
                                   pf2bf(0, self.currentPl()))
                                   )
                else:
                    #print("I'm on my start. Try to clear!")

                    self.moveAndKick(self.moveWhich(allMyPoss, d, self.tactics[self.currentPl()-1]))

            else: # if none left to move out

                self.moveAndKick(self.moveWhich(allMyPoss, d, self.tactics[self.currentPl()-1]))

            #print("Doing my 2nd move!")
            if not self.np:
                printBoard(self)        

            self.oneMove()
            return # important
        elif (mineOnBoard == 0) and (self.noGapsInGoal(self.currentPl())) and (attempt < 3):
            #print("""Can't move, attempt %d""" % (attempt + 1))
            
            if not self.np:
                printBoard(self)

            self.oneMove(attempt=attempt+1) 
            return
        else: # if no 6 and there are some on the board or gaps in the goal
            if self.iNotOnStart(self.currentPl()):

                self.moveAndKick(self.moveWhich(allMyPoss, d, self.tactics[self.currentPl()-1]))


            else: # player self on own start
                self.moveAndKick(self.moveWhich(allMyPoss, d, self.tactics[self.currentPl()-1]))

        if not self.np:
            printBoard(self)
        if self.hasPlFinished(self.currentPl()): self.finishProc(self.currentPl())
