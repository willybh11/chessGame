'''
made by Leo Kastenberg
'''
from generationalLearn import *
if __name__ == "__main__":
    genSize = 10
    randomness = 10
    aValues = [1000 for i in range(6)]
    aValues.extend([100 for i in range(6)])
    chessPlayerA = Species(lambda x:x**2,aValues,genSize,randomness)
    bValues = [1000 for i in range(6)]
    bValues.append(100)
    bValues.extend([1 for i in range(5)])
    chessPlayerB = Species(lambda x:x**2,bValues,genSize,randomness)
    generations = 1 #change this value for optimizing stuff
    thisGame = Competition(chessPlayerA,chessPlayerB,Game)
    for generation in range(generations):
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
    print "\nthe values for player A are:",chessPlayerA.currentGeneration
    print "\nthe values for player B are:",chessPlayerB.currentGeneration
