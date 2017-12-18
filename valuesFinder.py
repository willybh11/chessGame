'''
made by Leo Kastenberg
'''
from generationalLearn import *
if __name__ == "__main__":
    genSize = 4
    randomness = 10
    aValues = [400]
    aValues.extend([1000 for i in range(6)])
    aValues.append(100)
    aValues.extend([50 for i in range(5)])
    chessPlayerA = Species(lambda x:x**2,aValues,genSize,randomness)
    bValues = aValues[:]
    chessPlayerB = Species(lambda x:x**2,bValues,genSize,randomness)
    generations = 10 #change this value for optimizing stuff
    thisGame = Competition(chessPlayerA,chessPlayerB,Game)
    for generation in range(generations):
        print "\n\n==========WE ARE ENTERING GENERATION %d==========\n\n" %(generation)

        scoresA = [0 for i in range(genSize)]
        scoresB = [0 for i in range(genSize)]
        for a in range(genSize):
            for b in range(genSize):
                playerA = Game(chessPlayerA.currentGeneration[a],True)
                playerB = Game(chessPlayerB.currentGeneration[b],True)
                winner = thisGame.compete(playerA,playerB)#returns a 0 if A wins and a 1 if B wins -- now it can return a 2 if it is a stalemate
                if winner < 2:
                    if winner:
                        scoresB[b] += 1
                        scoresA[a] -= 1
                    else:
                        scoresA[a] += 1
                        scoresB[b] += 1
        aBest = chessPlayerA.currentGeneration[scoresA.index(max(scoresA))]
        bBest = chessPlayerB.currentGeneration[scoresB.index(max(scoresB))]

        chessPlayerA.breedGen(aBest)
        chessPlayerB.breedGen(bBest)
        with open("learningResults.txt","w") as f: 
            f.truncate()
            f.write(str(chessPlayerA)+"\n"+str(chessPlayerB))
    print "\nthe values for player A are:",chessPlayerA.currentGeneration
    print "\nthe values for player B are:",chessPlayerB.currentGeneration
