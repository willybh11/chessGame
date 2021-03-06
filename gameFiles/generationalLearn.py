'''
made by Leo Kastenberg
'''
import random
from chessGame import *
class Species:

    def __init__(self,evaluate,values,genSize,randomness):
        self.evaluate = evaluate

        self.values = values    #this will be a list of whatever values are relevant to the current problem being solved. The list will be the max values (minimum is assumed 0)
                                #NOTE: remember that these values can only be integers, so don't make the range too small; use units accordingly (i.e. 1200 mL, not 1.2 L)

        self.genSize = genSize

        self.randomness = randomness

        self.currentGeneration = [[random.randint(0,values[i]) for i in range(len(values))] for ctzn in range(genSize)]

        #print "the first generation is",self.currentGeneration

        #each citizen of a generation will simply be a list of values, just like real life

        #self.currentGeneration = [[random.randint(0,values[i]) for i in range(len(values))] for j in range(genSize)] #just establishes a first generation

    def evolve(self,generations):
        bestTwo = [[self.evaluate(self.currentGeneration[0]),self.currentGeneration[0]],[self.evaluate(self.currentGeneration[1]),self.currentGeneration[1]]]
        evalutedGeneration = []
        for generation in range(generations):
            for citizen in self.currentGeneration:
                curEval = self.evaluate(citizen)
                evaluatedCitizen = [curEval,citizen]
                if curEval > bestTwo[0][0]:
                    bestTwo[1] = bestTwo[0]
                    bestTwo[0] = evaluatedCitizen
                elif curEval > bestTwo[1][0]:
                    bestTwo[1] = evaluatedCitizen
                evalutedGeneration.append(evaluatedCitizen)
            self.currentGeneration = [self.breed(citizen,random.choice(bestTwo)) for citizen in self.currentGeneration[:]]

    def breed(self,aParent,bParent):
        print "breading",aParent,"with",bParent
        return [((aParent[i]+bParent[i])/2 + random.randint(-self.randomness,self.randomness)) for i in range(len(aParent))] #averages the two parents and then adds randomness

    def breedGen(self,best):
        for i in range(self.genSize):
            self.currentGeneration[i] = self.breed(self.currentGeneration[i],best)

    def __str__(self):
        best = [self.evaluate(self.currentGeneration[0]),self.currentGeneration[0]]
        for i in self.currentGeneration:
            if self.evaluate(i)>best[0]:
                best = [self.evaluate(i),i]
        return str(best[1])

    def __str__(self):
        string = ""
        for i in self.currentGeneration:
            citizen = ""
            for j in i:
                citizen+=str(j)+" "
            string+= citizen+"\n-\n"
        return string

class Competition:

    def __init__(self,speciesA,speciesB,game):
        self.speciesA = speciesA
        self.speciesB = speciesB
        self.Game = game

    def compete(self,playerA,playerB):
        playerA.graphics.turtleUpdate(playerA.board.grid) #palyer A is not defined
        whoseTurn = "w"
        playerA.board.printGrid()
        while not (playerA.board.isCheckmate(whoseTurn) or playerA.board.isStalemate(whoseTurn)):

            move = (playerA if whoseTurn=="w" else playerB).bestMove(whoseTurn) #playerA is always white.
                                                                                #This code will determine whose turn it is in terms of instances of the class and figure out their best move

            #now we have to update the boards twice because we need to keep both players up-to-date on the current board

            playerA.board.movePiece(move,True)
            playerA.graphics.turtleUpdate(playerA.board.grid)
            playerB.board.movePiece(move,True)
            playerB.graphics.turtleUpdate(playerB.board.grid)
            print str(playerA.board)
            whoseTurn = ("w" if whoseTurn=="b" else "b")
            if playerA.board.isCheck(whoseTurn): print "\nCHECK\n"

        playerA.graphics.turtleSetup()
        print ("checkmate" if playerA.board.isCheckmate(whoseTurn) else "stalemate")

        if playerA.board.isStalemate(whoseTurn):
            return 2
        else:#otherwise it would have ended with a checkmate. Now we return the corresponding code for the player who won, which will be the player whose turn it is not
            return (0 if whoseTurn == "w" else 1)

if __name__ == "__main__":
    #just some test code
    '''comp = Competition(Species(False,[10,100,40,10000,50,30,3,1,3,-10,3,5],10,2),Species(False,[10,100,40,10000,50,30,3,1,3,-10,3,5],10,2),Game)
    comp.compete(Game([1,10,4,1000,5,3,0.3,0.1,0.3,-1,0.3,0.5],1),Game([1,10,4,1000,5,3,0.3,0.1,0.3,-1,0.3,0.5],1))'''
    print "you shouldn;t be running this file"
