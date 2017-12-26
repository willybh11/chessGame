'''
made by Leo Kastenberg and Will Hagele
'''
import turtle
import time
import random
from generationalLearn import *
from sys import platform

class Graphics:

    class Draw:

        def __init__(self, T):
            self.T = T

        def box(self):
            self.coords = self.T.pos()
            self.T.goto(self.coords[0] - 30, self.coords[1] - 24)
            self.T.seth(0)
            self.T.pd()
            self.T.begin_fill()
            for i in range(2):
                self.T.fd(60)
                self.T.rt(90)
                self.T.fd(11)
                self.T.rt(90)
            self.T.end_fill()
            self.T.pu()

        def king(self):
            self.box()
            self.T.goto(self.coords[0] + 13, self.coords[1] + 9)
            self.T.seth(90)
            self.T.pd()
            self.T.begin_fill()
            self.T.circle(13)
            self.T.goto(self.coords[0] - 2, self.coords[1] + 21)
            self.T.seth(360)
            for i in range(4):
                self.T.fd(4)
                self.T.lt(90)
                self.T.fd(7)
                self.T.rt(90)
                self.T.fd(7)
                self.T.lt(90)
            self.T.end_fill()

        def queen(self):
            self.box()
            self.T.goto(self.coords[0] + 13, self.coords[1] + 9)
            self.T.seth(90)
            self.T.pd()
            self.T.begin_fill()
            self.T.circle(13)
            self.T.end_fill()
            self.T.seth(360)
            for coords in [(self.coords[0] - 20, self.coords[1] + 24),
                           (self.coords[0] - 8, self.coords[1] + 29),
                           (self.coords[0] + 8, self.coords[1] + 29),
                           (self.coords[0] + 20, self.coords[1] + 24)]:
                self.T.pu()
                self.T.goto(coords)
                self.T.begin_fill()
                self.T.pd()
                self.T.circle(5)
                self.T.end_fill()

        def bishop(self):
            self.box()
            self.T.goto(self.coords[0], self.coords[1] + 35)
            self.T.pd()
            self.T.begin_fill()
            for heading in [250, 290, 70, 110]:
                self.T.seth(heading)
                self.T.fd(25)
            self.T.end_fill()

        def knight(self):
            self.box()
            self.T.goto(self.coords[0] + 2, self.coords[1] + 5)
            self.T.begin_fill()
            self.T.pd()
            self.T.circle(15, 180)
            self.T.end_fill()
            self.T.pu()
            self.T.goto(self.coords[0] - 2, self.coords[1] + 25)
            self.T.seth(180)
            self.T.begin_fill()
            self.T.circle(20, 180)
            self.T.end_fill()

        def pawn(self):
            self.box()
            self.T.seth(90)
            self.T.goto(self.coords[0] + 15, self.coords[1] + 20)
            self.T.begin_fill()
            self.T.pd()
            self.T.circle(15)
            self.T.end_fill()

        def rook(self):
            self.box()
            self.T.goto(self.coords[0] - 15, self.coords[1] + 17)
            self.T.begin_fill()
            self.T.pd()
            self.T.fd(30)
            self.T.lt(90)
            self.T.fd(15)
            for i in range(2):
                self.T.lt(90)
                self.T.fd(6)
                self.T.lt(90)
                self.T.fd(4)
                self.T.rt(90)
                self.T.fd(6)
                self.T.rt(90)
                self.T.fd(4)
            self.T.lt(90)
            self.T.fd(6)
            self.T.lt(90)
            self.T.fd(15)
            self.T.seth(270)
            self.T.circle(15, 180)
            self.T.end_fill()

    def turtleSetup(self):
        self.window = turtle.Screen()
        self.window.clear()
        self.window.setup(724, 724)
        self.window.bgpic("background.gif" if ("linux" in platform) else "gameFiles/background.gif")
        self.window.tracer(0, 0)
        self.T = turtle.Turtle()
        self.T.speed(10)
        self.T.ht()
        self.write = self.Draw(self.T)
        self.draw = {"P": self.write.pawn,
                     "R": self.write.rook,
                     "K": self.write.king,
                     "Q": self.write.queen,
                     "B": self.write.bishop,
                     "N": self.write.knight}

    def turtleUpdate(self,grid):
        self.T.clear()
        for row in range(8):
            for col in range(8):
                square = grid[col][row]
                coords = (row * 90 - 315,  col * 90 - 315)
                self.T.pu()
                self.T.goto(coords)
                color = "white" if "w" in square else "black"
                self.T.fillcolor(color)
                self.T.pencolor(color)
                try:
                    self.draw[square[0]]()
                except IndexError:
                    pass  # empty square
        turtle.update() #graaaphics

class Board:

    def __init__(self):

        self.pieceStartOrder = ["R","N","B","Q","K","B","N","R"]

        self.grid = self.makeGrid()

        self.letterConvert = {  "A":0,
                                "B":1,
                                "C":2,
                                "D":3,
                                "E":4,
                                "F":5,
                                "G":6,
                                "H":7}

        self.whiteCastleableSpots = [[0,0],[0,7]]
        self.blackCastleableSpots = [[7,0],[7,7]]

        self.gridCache = []

    def makeGrid(self):

        grid = [["" for i in range(8)] for i in range(8)] #makes an 8 by 8 grid

        for i in range(8):
            grid[1][i] = "Pw"   #makes the second row full of white pawns
            grid[6][i] = "Pb"   #makes the second row from the back full of black pawns

            grid[0][i] = self.pieceStartOrder[i]+"w"    #fills it up with the pieces in the correct order
            grid[7][i] = self.pieceStartOrder[i]+"b"    #same as above but the black pieces

        return grid

    def isCheck(self,whoseTurn):

        #row and column are the row and column of the piece that I am finding the possible moves of

        #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]

        threatenedTiles = self.tilesThreatened(whoseTurn)

        #these nested loops find where the king is. It might be better to save where the king is, but this function is no longer called very often
        for row in range(8):
            for column in range(8):
                if (self.grid[row][column]=="K"+whoseTurn):
                    if ([row,column] in threatenedTiles):
                        return True
                    else:
                        return False

        return True

    def isCheckmate(self,whoseTurn):

        if not self.isCheck(whoseTurn):
            return False

        posMoves = self.possibleColorMoves(whoseTurn,True)

        '''for move in posMoves:
            self.movePiece(move)
            if not self.isCheck(whoseTurn):     #if the move has fixed the situation
                self.undoMove()
                print "one possible move is",move
                print "\nCHECK\n"
                return False
            self.undoMove()
        '''
        if (len(posMoves)==0):
            return True
        else:
            #print "\nCHECK\n"
            return False

    def tilesThreatened(self,whoseTurn):
        posMoves = self.possibleColorMoves(("w" if whoseTurn == "b" else "b"),False)

        for i in range(len(posMoves)):    #the possible response moves. These tell me all of the threatened tiles exceot for the pawns
            move = posMoves[i][:]
            if move[1] == "P":
                pawnThreat = self.pawnThreatening(move[2],move[3])
                posMoves[i] = [move[0],move[1],move[2],move[3]]#,pawnThreat[0][0],pawnThreat[0][1]]
                posMoves[i].extend(pawnThreat[0])
                if len(pawnThreat) > 1:#if there is a second possible move for the pawns
                    posMoves.append([move[0],move[1],move[2],move[3],pawnThreat[1][0],pawnThreat[1][1]])

        #posMoves has now been transformed into a list of moves which are not all possible,
        #but do represent the threatened spaces

        threatenedTiles = []

        for move in posMoves:
            threaten = [move[4],move[5]]
            if not (threaten in threatenedTiles):
                threatenedTiles.append(threaten)

        return threatenedTiles

    def isStalemate(self,whoseTurn):
        if len(self.gridCache)<10:
            return False
        if (self.gridCache[-1]==self.gridCache[-5] and self.gridCache[-5]==self.gridCache[-9]):
            print "\n\nSTALEMATE!!\n\n"
            return True

        possMoves = self.possibleColorMoves(whoseTurn,True)
        for row in range(8):
            for col in range(8):
                if self.grid[row][col] == "K"+whoseTurn:
                    kingCoords = [row,col]
                    break
        if (not (kingCoords in self.tilesThreatened(whoseTurn))) and len(possMoves)==0:#if the king isn't threatened, but there are no possible moves, then it is stalemate
            return True

        return False

    def undoMove(self):

        self.grid = [i[:] for i in self.gridCache[-1]]

        self.gridCache.pop(-1)

    def pawnThreatening(self,row,column):
        color = self.grid[row][column][1]
        returnList = []
        if color == "w":
            try:
                if self.grid[row+1][column-1] == "just get IndexError":
                    pass
                returnList.append([row+1,column-1])
            except IndexError:
                pass

            try:
                if self.grid[row+1][column+1] == "this line tires to provoke an index error":
                    pass                            #If that happens, NOTHING happens.
                returnList.append([row+1,column+1])
            except IndexError:
                pass

        else:
            try:
                if self.grid[row-1][column-1] == "just get IndexError":
                    pass
                returnList.append([row-1,column-1])
            except IndexError:
                pass

            try:
                if self.grid[row-1][column+1] == "just get IndexError":
                    pass
                returnList.append([row-1,column+1])
            except IndexError:
                pass

        return returnList

    def possiblePieceMoves2(self,row,column):#all of the possible moves that a given piece can make
        pieceType = self.grid[row][column][0]
        pieceColor = self.grid[row][column][1]

        baseMove = [pieceColor,pieceType,row,column]

        foundMoves = []

        for rowTo in range(8):
            for columnTo in range(8):
                testingMove = baseMove[:]
                testingMove.append(rowTo)
                testingMove.append(columnTo)
                if self.isLegalMove(testingMove,False):
                    print testingMove,"was a duplicate"


        return foundMoves

    def possiblePieceMoves(self,row,col,safeMode):
        piece = self.grid[row][col]
        pieceType = piece[0]
        pieceColor = piece[1]
        if pieceType == "Q":
            moves = self.possibleRookMoves(pieceColor,row,col,safeMode)
            moves.extend(self.possibleBishopMoves(pieceColor,row,col,safeMode))
            #print row,col,"can go to",[[i[4],i[5]] for i in moves]
            return moves
        return {"R":self.possibleRookMoves(pieceColor,row,col,safeMode),
                "N":self.possibleKnightMoves(pieceColor,row,col,safeMode),
                "B":self.possibleBishopMoves(pieceColor,row,col,safeMode),
                "K":self.possibleKingMoves(pieceColor,row,col,safeMode),
                "P":self.possiblePawnMoves(pieceColor,row,col,safeMode)}[pieceType]

    def possiblePawnMoves(self,color,row,col,safeMode):
        returnList = []
        piece = self.grid[row][col]
        for a in range(row-2,row+3):
            for b in range(col-1,col+2):
                move = [piece[1],piece[0],row,col,a,b]
                if self.isLegalMove(move,safeMode):
                    returnList.append(move)
        return returnList

    def possibleBishopMoves(self,color,row,col,safeMode):

        returnList = []
        piece = self.grid[row][col]

        for i in range(1,row+1):#down and to the right
            move = [piece[1],piece[0],row,col,row-i,col+i]

            if move[4] > 7 or move[4] < 0 or move[5] > 7 or move[5] < 0:#this chunk is the code taken from the start of isLegalMove
                break
            pieceType = move[1]
            if safeMode:
                self.movePiece(move)
                if self.isCheck(move[0]):
                    self.undoMove()
                    continue
                self.undoMove()

            goTo = self.grid[move[4]][move[5]]
            if goTo =="":
                returnList.append(move[:])
            elif goTo[1]==("b" if move[0]=="w" else "w"):
                returnList.append(move[:])
                break#we can break in this case even though it is a legal move, because the following pieces will be blocked
            else:
                break

        for i in range(1,8-row):#up and to the right
            move = [piece[1],piece[0],row,col,row+i,col+i]

            if move[4] > 7 or move[4] < 0 or move[5] > 7 or move[5] < 0:#this chunk is the code taken from the start of isLegalMove
                break
            pieceType = move[1]
            if safeMode:
                self.movePiece(move)
                if self.isCheck(move[0]):
                    self.undoMove()
                    continue
                self.undoMove()

            goTo = self.grid[move[4]][move[5]]
            if goTo =="":
                returnList.append(move[:])
            elif goTo[1]==("b" if move[0]=="w" else "w"):
                returnList.append(move[:])
                break#we can break in this case even though it is a legal move, because the following pieces will be blocked
            else:
                break

        for i in range(1,row+1):#down and to the left
            move = [piece[1],piece[0],row,col,row-i,col-i]

            if move[4] > 7 or move[4] < 0 or move[5] > 7 or move[5] < 0:#this chunk is the code taken from the start of isLegalMove
                break
            pieceType = move[1]
            if safeMode:
                self.movePiece(move)
                if self.isCheck(move[0]):
                    self.undoMove()
                    continue
                self.undoMove()

            goTo = self.grid[move[4]][move[5]]
            if goTo =="":
                returnList.append(move[:])
            elif goTo[1]==("b" if move[0]=="w" else "w"):
                returnList.append(move[:])
                break#we can break in this case even though it is a legal move, because the following pieces will be blocked
            else:
                break

        for i in range(1,8-row):#up and to the left
            move = [piece[1],piece[0],row,col,row+i,col-i]

            if move[4] > 7 or move[4] < 0 or move[5] > 7 or move[5] < 0:#this chunk is the code taken from the start of isLegalMove
                break
            pieceType = move[1]
            if safeMode:
                self.movePiece(move)
                if self.isCheck(move[0]):
                    self.undoMove()
                    continue
                self.undoMove()

            goTo = self.grid[move[4]][move[5]]
            if goTo =="":
                returnList.append(move[:])
            elif goTo[1]==("b" if move[0]=="w" else "w"):
                returnList.append(move[:])
                break#we can break in this case even though it is a legal move, because the following pieces will be blocked
            else:
                break

        return returnList

    def possibleRookMoves(self,color,row,col,safeMode): #TODO: fix bug where rook skips over pieces/maybe jumps over the side of the board?
        returnList = []
        piece = self.grid[row][col]

        for i in range(row+1,8):#up
            move = [piece[1],piece[0],row,col,i,col]

            '''if move[4] > 7 or move[4] < 0 or move[5] > 7 or move[4] < 0:#this chunk is the code taken from the start of isLegalMove
                break
            pieceType = move[1]'''
            if safeMode:
                self.movePiece(move)
                if self.isCheck(move[0]):
                    self.undoMove()
                    continue
                self.undoMove()

            goTo = self.grid[move[4]][move[5]]
            if goTo =="":
                returnList.append(move[:])
            elif goTo[1]==("b" if move[0]=="w" else "w"):
                returnList.append(move[:])
                break#we can break in this case even though it is a legal move, because the following pieces will be blocked
            else:
                break

        for i in range(row)[::-1]:#down
            move = [piece[1],piece[0],row,col,i,col]

            '''if move[4] > 7 or move[4] < 0 or move[5] > 7 or move[4] < 0:#this chunk is the code taken from the start of isLegalMove
                break
            pieceType = move[1]'''
            if safeMode:
                self.movePiece(move)
                if self.isCheck(move[0]):
                    self.undoMove()
                    continue
                self.undoMove()

            goTo = self.grid[move[4]][move[5]]
            if goTo =="":
                returnList.append(move[:])
            elif goTo[1]==("b" if move[0]=="w" else "w"):
                returnList.append(move[:])
                break#we can break in this case even though it is a legal move, because the following pieces will be blocked
            else:
                break

        for i in range(col+1,8):#right
            move = [piece[1],piece[0],row,col,row,i]

            '''if move[4] > 7 or move[4] < 0 or move[5] > 7 or move[4] < 0:#this chunk is the code taken from the start of isLegalMove
                break
            pieceType = move[1]'''
            if safeMode:
                self.movePiece(move)
                if self.isCheck(move[0]):
                    self.undoMove()
                    continue
                self.undoMove()

            goTo = self.grid[move[4]][move[5]]
            if goTo =="":
                returnList.append(move[:])
            elif goTo[1]==("b" if move[0]=="w" else "w"):
                returnList.append(move[:])
                break#we can break in this case even though it is a legal move, because the following pieces will be blocked
            else:
                break

        for i in range(col)[::-1]:#left
            move = [piece[1],piece[0],row,col,row,i]

            '''if move[4] > 7 or move[4] < 0 or move[5] > 7 or move[4] < 0:#this chunk is the code taken from the start of isLegalMove
                break
            pieceType = move[1]'''
            if safeMode:
                self.movePiece(move)
                if self.isCheck(move[0]):
                    self.undoMove()
                    continue
                self.undoMove()

            goTo = self.grid[move[4]][move[5]]
            if goTo =="":
                returnList.append(move[:])
            elif goTo[1]==("b" if move[0]=="w" else "w"):
                returnList.append(move[:])
                break#we can break in this case even though it is a legal move, because the following pieces will be blocked
            else:
                break

        return returnList

    def possibleKnightMoves(self,color,row,col,safeMode):

        returnList = []
        piece = self.grid[row][col]

        move = [piece[1],piece[0],row,col,row+1,col+2]
        if self.isLegalMove(move,safeMode): returnList.append(move[:])

        move = [piece[1],piece[0],row,col,row-1,col+2]
        if self.isLegalMove(move,safeMode): returnList.append(move[:])

        move = [piece[1],piece[0],row,col,row+1,col-2]
        if self.isLegalMove(move,safeMode): returnList.append(move[:])

        move = [piece[1],piece[0],row,col,row-1,col-2]
        if self.isLegalMove(move,safeMode): returnList.append(move[:])

        move = [piece[1],piece[0],row,col,row+2,col+1]
        if self.isLegalMove(move,safeMode): returnList.append(move[:])

        move = [piece[1],piece[0],row,col,row+2,col-1]
        if self.isLegalMove(move,safeMode): returnList.append(move[:])

        move = [piece[1],piece[0],row,col,row-2,col+1]
        if self.isLegalMove(move,safeMode): returnList.append(move[:])

        move = [piece[1],piece[0],row,col,row-2,col-1]
        if self.isLegalMove(move,safeMode): returnList.append(move[:])

        return returnList

    def possibleKingMoves(self,color,row,col,safeMode):
        returnList = []
        piece = self.grid[row][col]

        for a in range(row-1,row+2):
            for b in range(col-1,col+2):
                move = [piece[1],piece[0],row,col,a,b]
                if self.isLegalMove(move,safeMode):
                    returnList.append(move)

        return returnList

    def possibleColorMoves(self,color,safeMode):#all of the possible moves that a player (specified by the color) can make

        foundMoves = []
        for row in range(8):
            for column in range(8):
                piece = self.grid[row][column]
                if len(piece) != 0:
                    if self.grid[row][column][1]==color:
                        pieceMoves = self.possiblePieceMoves(row,column,safeMode)
                        if len(pieceMoves)!=0:
                            foundMoves.extend(pieceMoves)

        return foundMoves

    def isLegalMove(self,move,safeMode): #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]
        if move[4] > 7 or move[4] < 0 or move[5] > 7 or move[5] < 0:
            return False
        pieceType = move[1]
        if safeMode:
            self.movePiece(move)
            if self.isCheck(move[0]):
                self.undoMove()
                return False
            self.undoMove()

        if not (pieceType+move[0] == self.grid[move[2]][move[3]]): #the piece has to be there
            return False

        if move[2]==move[4] and move[3]==move[5]: return False

        if pieceType == "P":
            return self.isLegalPawnMove(move)

        if pieceType == "N":
            return self.isLegalKnightMove(move)

        if pieceType == "R":
            return self.isLegalRookMove(move)

        if pieceType == "K":
            return self.isLegalKingMove(move)

        if pieceType == "B":
            return self.isLegalBishopMove(move)

        if pieceType == "Q":
            return (self.isLegalBishopMove(move) or self.isLegalRookMove(move))

    def isLegalKingMove(self,move): #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]
        if move[4]>7 or move[5]>7 or move[4]<0 or move[5]<0: return False
        deltaRow = abs(move[2]-move[4])
        deltaCol = abs(move[3]-move[5])
        movementCorrect = False
        movetoSafe = False
        if (deltaRow==1 and (deltaCol==0 or deltaCol==1)) or (deltaCol==1 and (deltaRow==0 or deltaRow==1)):
            movementCorrect = True
        try:
            if self.grid[move[4]][move[5]][1] == move[0]:
                movetoSafe = False
            else:
                movetoSafe = True
        except IndexError:
            movetoSafe = True

        return movetoSafe and movementCorrect

    def isLegalKnightMove(self,move): #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]
        if move[4]>7 or move[5]>7 or move[4]<0 or move[5]<0: return False
        deltaRow,deltaCol = abs(move[2]-move[4]),abs(move[3]-move[5])
        movementCorrect = False#they need to be false by default, if they should be true I will make them true
        gotoSafe = False
        if ((deltaRow==1 and deltaCol==2) or (deltaRow==2 and deltaCol==1)):
            movementCorrect = True

        try:
            if (move[0] == "w") and (self.grid[move[4]][move[5]][1] == "b"):
                gotoSafe = True
            elif (move[0] == "b") and (self.grid[move[4]][move[5]][1] == "w"):
                gotoSafe = True
        except IndexError:
            gotoSafe = True
        return (movementCorrect and gotoSafe)

    def isLegalBishopMove(self,move): #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]
        if move[4]>7 or move[5]>7 or move[4]<0 or move[5]<0: return False

        if move[2]-move[4] == 0:
            return False
        if not (abs(move[2]-move[4]) == abs(move[3]-move[5])):
            return False


        distance = abs(move[2]-move[4])

        rowDirection = distance/(move[4]-move[2])
        columnDirection = distance/(move[5]-move[3])

        for i in range(1,distance):
            if self.grid[move[2] + (i*rowDirection)][move[3] + (i*columnDirection)]!="":
                return False

        try:
            if self.grid[move[4]][move[5]][1] == move[0]:
                return False  #if there is a same-colored piece where you want to go
        except:
            pass

        return True

    def isLegalPawnMove(self,move): #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]
        if move[4]>7 or move[5]>7 or move[4]<0 or move[5]<0: return False

        if move[0]=="w":#moving as a white piece is opposite of moving as a black piece, so it will be programmed seperately
            isStartingSpot = move[2]==1 #a boolean for if it is in the starting possition
            if ((move[4]-move[2] == 1) or ((isStartingSpot and (move[4]-move[2] == 2)) and (self.grid[move[2]+1][move[3]] == ""))) and (move[3]==move[5]):#basically if it is moving forward by one, or by two if in the starting spot and staying in the same column
                if len(self.grid[move[4]][move[5]]) > 1:#if there is a piece there, because the pawn cannot take a piece by doing this type of move
                    return False
                return True

            elif (move[4]-move[2] == 1) and (abs(move[3]-move[5])==1):  #elf-is
                try:
                    if self.grid[move[4]][move[5]][1] == "b":#if it is going to an enemy piece
                        return True
                except:
                    pass

        elif move[0]=="b":
            isStartingSpot = move[2]==6 #a boolean for if it is in the starting possition
            if ((move[2]-move[4] == 1) or ((isStartingSpot and (move[2]-move[4] == 2)) and (self.grid[move[2]-1][move[3]] == ""))) and (move[3]==move[5]): #basically if it is moving forward by one, or by two if in the starting spot and staying in the same column
                if len(self.grid[move[4]][move[5]]) > 1:#if there is a piece there, because the pawn cannot take a piece by doing this type of move
                    return False
                return True
            elif (move[2]-move[4] == 1) and (abs(move[3]-move[5])==1):#this is beautiful because 1 is true, and I want to see if it is moving one to the side
                try:
                    if self.grid[move[4]][move[5]][1] == "w":#if it is going to an enemy piece
                        return True
                except:
                    pass
        return False

    def isLegalRookMove(self,move): #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]
        if move[4]>7 or move[5]>7 or move[4]<0 or move[5]<0: return False

        if not ((move[2]==move[4]) or (move[3]==move[5])): #makes sure that it is either the same row or column
            return False
        if move[2] == move[4]: #if we are doing a
            if move[5] > move[3]:
                for i in range (move[3]+1,move[5]):
                    if self.grid[move[2]][i] != "":    #if the path is blocked by another piece
                        return False
            else:
                for i in range (move[5]+1,move[3]):
                    if self.grid[move[2]][i] != "":    #if the path is blocked by another piece
                        return False
                    #alsd

        else:
            if move[2]>move[4]:
                for i in range(move[4]+1,move[2]):
                    if self.grid[i][move[3]] != "": return False
            else:
                for i in range(move[2]+1,move[4]):
                    if self.grid[i][move[3]] != "": return False

        try:
            if self.grid[move[4]][move[5]][1] == move[0]: return False  #if there is a same-colored piece where you want to go
        except:
            pass

        return True

    def movePiece(self,move): #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]

        #NOTE only call this function if you have already checked if the move is a legal move

        #first I am putting the code relevant to castling; NOTE: this function is not to be used for castling

        if move[1] == "R":
            if move[0] == "w":
                if [move[2],move[3]] in self.whiteCastleableSpots:
                    self.whiteCastleableSpots.remove([move[2],move[3]])
            elif [move[2],move[3]] in self.blackCastleableSpots:
                self.blackCastleableSpots.remove([move[2],move[3]])

        if move[1] == "K":
            if move[0] == "w":
                self.whiteCastleableSpots = []
            else:
                self.blackCastleableSpots = []

        self.gridCache.append([i[:] for i in self.grid])#because python takes over the control of pointers and such, this is the only way to make it not update with self.grid

        self.grid[move[2]][move[3]] = ""
        try:
            self.grid[move[4]][move[5]] = move[1]+move[0]
        except IndexError:
            print "I tried to do the move",move

        if (move[4] == (0 if move[0]=="b" else 7)) and move[1] == "P":
            self.grid[move[4]][move[5]] = "Q"+move[0]

    def isLegalCastle(self,color,move):#castles are in the format ["castle",withRookRow,withRookCol]

        #it is highly advised that you look at a chess board while reading this in order to understand it
        #I had to look at one the whole time I programmed it anyway

        if color == "w":
            if not ([move[1],move[2]] in self.whiteCastleableSpots):
                return False
        else:
            if not ([move[1],move[2]] in self.blackCastleableSpots):
                return False

        #now we know if the pieces have been moved

        row = (0 if color=="w" else 7)#the row that this will be happening on

        if move[2] == 0:#if it is the left rook
            for col in range(1,4):
                if not (self.grid[row][col] == ""):
                    print "in the way"
                    return False
        else:
            for col in range(5,7):
                if not (self.grid[row][col] == ""):
                    print "in the way"
                    return False

        return True

    def castleMove(self,move):#castles are in the format ["castle",withRookRow,withRookCol]

        #NOTE this function only gets called if it is already determined to be a legal move

        self.gridCache.append([i[:] for i in self.grid])#again, this is to get around python's stupid (not really stupid, still simpler than C) pointer stuff


        color = ("w" if move[1] == 0 else "b")

        kingCoords = [(2 if move[2] == 0 else 6),move[1]]
        rookCoords = [(3 if move[2] == 0 else 5),move[1]]

        self.grid[move[1]][kingCoords[0]] = "K"+color
        self.grid[move[1]][4] = ""
        self.grid[move[1]][rookCoords[0]] = "R"+color
        self.grid[move[1]][move[2]] = ""

    def takePlayerMove(self,colorsTurn):    # i changed this
        invalidMove = True
        while invalidMove: #because python doesn't have any heckin' do while loops
            print "it is "+colorsTurn+"'s turn\n"

            inputMove = raw_input("input move in the format:\n'column' row 'columnTo' rowTo\ne.g. A 2 A 4\n>>>").split() #currently in the format [row,column,rowTo,columnTo]

            try:
                row = int(inputMove[1]) - 1
                col = self.letterConvert[inputMove[0].upper()]
                rowto = int(inputMove[3]) - 1
                colto = self.letterConvert[inputMove[2].upper()]
                try:
                    piece = self.grid[row][col][0]
                except IndexError:
                    piece = "P"#if you accidentally typed the coords for an empty square then we just need to pick a placeholder string. It will be a bad move anyway

                rawMove = [ piece, row, col, rowto, colto ]

            except: # not enough inputs or castle

                if inputMove[0].lower() == "castle":#castles are in the format ["castle",withRookRow,withRookCol]
                    rawMove = ["castle", int(inputMove[2]) - 1, self.letterConvert[inputMove[1].upper()]]
                    #rawMove[1],rawMove[2] = int(rawMove[1]),int(rawMove[2])
                    if self.isLegalCastle(colorsTurn,rawMove):
                        self.castleMove(rawMove)
                        invalidMove = False
                    else:
                        print "that move was not a legal move, please check how you formated it (invalid castle)"
                else:
                    print "invalid num of inputs"

            move = [colorsTurn]
            move.extend(rawMove)
            if self.isLegalMove(move,True):
                self.movePiece(move)
                invalidMove = False
            else:
                print "that move was not a legal move, please check how you formated it (after castlecheck)"

    def printGrid(self):

        top = "   0  1  2  3  4  5  6  7"
        print top

        for i in range(8)[::-1]:
            row = self.grid[i]
            printRow = str(i)+" "
            for square in row:
                if len(square)>1:
                    printRow = printRow + square + " "
                else:
                    printRow = printRow + " - "
            print printRow

class Game:

    def __init__(self,tuningValues,testing):

        self.isLinux = ("linux" in platform) #if it is running on a linux platform then the user will be launching this directly without the executable


        self.lastTurnTime = 5
        self.futureTurns = 2
        self.board = Board()
        self.graphics = Graphics()
        self.graphics.turtleSetup()
        self.pieceValues = [int(tuningValues[i]) for i in range(6)]
        self.movementCoefficients = [int(tuningValues[i]) for i in range(6,12)]
        self.playGame = [self.zeroPlayer, self.singlePlayer, self.twoPlayer]

        self.graphics.turtleUpdate(self.board.grid)

        if testing:
            pass
        else:
           self.playGame[input("How many players? ")]()

    def twoPlayer(self):
        whoseTurn = "w"
        while not (self.board.isCheckmate(whoseTurn) or self.board.isStalemate(whoseTurn)):
            self.graphics.turtleUpdate(self.board.grid)
            self.board.printGrid()
            while 1:
                try:
                    self.board.takePlayerMove(whoseTurn)
                    break
                except:
                    print "format error: try again\n"

            whoseTurn = ("w" if whoseTurn == "b" else "b")


        self.board.printGrid()
        print ("checkmate" if self.board.isCheckmate(whoseTurn) else "stalemate")

    def singlePlayer(self):
        playerColor = raw_input("\nwhat color do you want to play as?\n>>>")
        compColor = ("b" if playerColor == "w" else "w")

        whoseTurn = "b"#start as black because it switches colors at the start of the loop

        while not (self.board.isCheckmate(whoseTurn) or self.board.isStalemate(whoseTurn)):
            whoseTurn = ("b" if whoseTurn == "w" else "w")
            self.graphics.turtleUpdate(self.board.grid)
            if whoseTurn == playerColor:
                self.board.printGrid()
                self.board.takePlayerMove(whoseTurn)
            else:
                self.board.movePiece(self.bestMove(compColor))

    def zeroPlayer(self):
        genSize = 3
        randomness = 50
        aValues = [400]
        aValues.extend([1000 for i in range(6)])#values of the pieces
        aValues.append(1000)#the pawn worth devisor
        aValues.extend([50 for i in range(5)])#values which are currently being thrown out, but may be of use later
        chessPlayerA = Species(lambda x:x**2,aValues,genSize,randomness)    #the lambda function never gets used because this training algorithm is only adversarial.
                                                                            #the lambda function would be used if we could train it without an adversarial algorithm
        bValues = aValues[:]
        chessPlayerB = Species(lambda x:x**2,bValues,genSize,randomness)
        generations = 10 #change this value for optimizing stuff
        thisGame = Competition(chessPlayerA,chessPlayerB,Game)

        #the following section of code was an after-thought. It will read from learnignResults.txt and take the tuning values reached from last time

        with open(("learningResults.txt" if self.isLinux else "gameFiles/learningResults.txt"),"r") as f:
            latest = f.read()
            if latest != "":#if we have values from previous attempts
                aGen,bGen = latest.split("--")
                aGen = aGen.split("\n-\n")
                bGen = bGen.split("\n-\n")
                for i in range(genSize):
                    aGen[i] = aGen[i].split()
                    for j in range(12):
                        aGen[i][j] = int(aGen[i][j])
                    bGen[i] = bGen[i].split()
                    for j in range(12):
                        bGen[i][j] = int(bGen[i][j])
                chessPlayerA.currentGeneration = aGen
                chessPlayerB.currentGeneration = bGen

        for generation in range(generations):
            print "\n\n==========WE ARE ENTERING GENERATION %d==========\n\n" %(generation)

            with open(("learningResults.txt" if self.isLinux else "gameFiles/learningResults.txt"),"w") as f:
                f.truncate()
                f.write(str(chessPlayerA)+"--"+str(chessPlayerB))

            scoresA = [0 for i in range(genSize)]
            scoresB = [0 for i in range(genSize)]
            for a in range(genSize):
                for b in range(genSize):
                    print "\n\nWE ARE ON GAME %d\n\n" % (3*a+b)
                    playerA = Game(chessPlayerA.currentGeneration[a],True)  #each player is an instance of the Game class with different sets of the values which we are throwing out.
                                                                            #yes, it is stupid that we have multiple instances of the Game class within the Game class, but Will insisted
                    playerB = Game(chessPlayerB.currentGeneration[b],True)
                    winner = thisGame.compete(playerA,playerB)#returns a 0 if A wins and a 1 if B wins -- now it can return a 2 if it is a stalemate
                    if winner < 2:
                        if winner:
                            scoresB[b] += 1
                            scoresA[a] -= 1
                        else:
                            scoresA[a] -= 1
                            scoresB[b] += 1
            aBest = chessPlayerA.currentGeneration[scoresA.index(max(scoresA))]
            bBest = chessPlayerB.currentGeneration[scoresB.index(max(scoresB))]

            chessPlayerA.breedGen(aBest)
            chessPlayerB.breedGen(bBest)
            with open(("learningResults.txt" if self.isLinux else "gameFiles/learningResults.txt"),"w") as f:
                f.truncate()
                f.write(str(chessPlayerA)+"\n--\n\n"+str(chessPlayerB))
        print "\nthe values for player A are:",chessPlayerA.currentGeneration
        print "\nthe values for player B are:",chessPlayerB.currentGeneration

    def evaluateMove(self,move,movesLeft,isComp):

        #all that is done in this function is call itself recursively and take the worst or best case depending on if it is the computer's turn or the player's turn
        compColor = (move[0] if isComp else ("b" if move[0]=="w" else "w"))
        if movesLeft > 0:
            goTo = self.board.grid[move[4]][move[5]]
            if goTo != "":  #just prevents an index error
                if goTo[0] == "K":#if the move would take the king
                    return ((1 if isComp else -1) * (100000/movesLeft))#this is just like checking for checkmates, but it is more efficient

            self.board.movePiece(move)

            '''
            if isComp:
                if self.board.isCheck(move[0]):
                    self.board.undoMove()
                    return -100000  # it just makes it go like: "stop doing that"'''
            color = ("b" if move[0] == "w" else "w")
            possMoves = self.board.possibleColorMoves(color,False)
            '''
            if isComp:
                if len(possMoves)==0:#this is the same, just faster, as calling isCheckmate
                    self.board.undoMove()
                    return 100000/movesLeft
            else:
                if len(possMoves)==0:
                    self.board.undoMove()
                    return -100000/movesLeft
            '''
            if not isComp:

                best = self.evaluateMove(possMoves[0],movesLeft-1,(not isComp))
                for nextMove in possMoves:
                    curEval = self.evaluateMove(nextMove,movesLeft-1,(not isComp))
                    if curEval > best: best = curEval
                self.board.undoMove()
                return best
            else:
                worst = self.evaluateMove(possMoves[0],movesLeft-1,(not isComp))
                for nextMove in possMoves:
                    curEval = self.evaluateMove(nextMove,movesLeft-1,(not isComp))
                    if curEval < worst:
                        worst = curEval
                self.board.undoMove()
                return worst
        else:#this is now if there are no more moves to look into the future
            self.board.movePiece(move)
            compColor = (move[0] if isComp else ("w" if move[0]=="b" else "b"))
            evaluation = self.evaluateBoard(compColor)
            self.board.undoMove()
            return evaluation

    def evaluateBoard(self,forColor):#evaluates the worth of the board for a given color
        '''
        if   self.board.isCheckmate(("w" if forColor=="b" else "b")):
            return  100000
        elif self.board.isCheckmate(forColor):
            return -100000'''

        value = 0
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if len(piece)==0:
                    continue
                elif piece[1] == forColor:
                    value += self.evaluatePieceValue(row,col)
                else:
                    value -= self.evaluatePieceValue(row,col)
        return value

    def evaluatePieceValue(self,row,col):
        piece = self.board.grid[row][col]

        distance = (row if piece[1]=="w" else (7-row))

        startVals = {
                        "P":self.pieceValues[0],
                        "Q":self.pieceValues[1],
                        "B":self.pieceValues[2],
                        "K":1000000,
                        "R":self.pieceValues[4],
                        "N":self.pieceValues[5]}
        '''
        distanceCoefficients = {"P":self.movementCoefficients[0],
                                "Q":self.movementCoefficients[1],
                                "B":self.movementCoefficients[2],
                                "K":self.movementCoefficients[3],
                                "R":self.movementCoefficients[4],
                                "N":self.movementCoefficients[5]}
        '''
        distanceCoefficients = {"P":self.pieceValues[1]/(self.movementCoefficients[0]/50),   #the worth of a queen devided by a number which is trained by the algorithm
                                                                                        #It has to then be devided by 10 because the randomness has to be the same for all values being trained
                                "Q":0,
                                "B":0,
                                "K":0,
                                "R":0,
                                "N":0}

        return (startVals[piece[0]]+(distanceCoefficients[piece[0]]*distance))

    def bestMove(self,color):#compTurn is boolean for if it is the computer's turn

        start = time.clock()
        possMoves = self.board.possibleColorMoves(color,True)
        if len(possMoves)==0:
            print "no possible moves"
            self.board.printGrid()
        best = [self.evaluateMove(possMoves[0],self.futureTurns,True),possMoves[0]]
        for move in possMoves:
            curEval = self.evaluateMove(move,self.futureTurns,True)
            if curEval > best[0]:
                best = [curEval,move]
            elif (abs(curEval - best[0]) < 5):
                if random.choice([1,0]):
                    best = [curEval,move]

        #the following chunk of code is for determining how far into the future it should look
        if time.clock()-start < 0.4:
            if self.lastTurnTime < 0.4:
                self.futureTurns += 1
                print "increasing futureTurns to",self.futureTurns
        if time.clock()-start > 10:
            if self.lastTurnTime > 10:
                self.futureTurns -= 1
                print "decreasing futureTurns to",self.futureTurns
        self.lastTurnTime = time.clock()-start

        print best[1]

        return best[1]

if __name__ == "__main__":
    #order is: Pawn, Queen, Bishop, King, Rook, Knight
    with open(("learningResults.txt" if ("linux" in platform) else "gameFiles/learningResults.txt"),"r") as f:
        firstLine = f.readline()
        if firstLine == "":
            game = Game([1,10,4,1000,5,3,300,0.1,0.3,-1,0.3,0.5],False)#creates a Game class with some generic values
        else:
            game = Game(firstLine.split(),False)#creates a Game class with the latest tuning Values
