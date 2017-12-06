import sgf
import re
import math

class JosekiOnBoard(object):
    def __init__(self):
        #create 2d array so that I don't have to duplicate code so much
        self.tlList = [] #top-left
        self.trList = [] #top-right
        self.blList = [] #bottom-left
        self.brList = [] #bottom-right
        self.nonJosekiList = [] #for stones not part of joseki

        #need to add passes if last colour is same as currently added colour
        #tlLastColourPlayed
        #trLastColourPlayed
        #blLastColourPlayed
        #brLastColourPlayed

        self.tlRegEx = r"[a-f][a-f]"
        self.trRegEx = r"[n-s][a-f]"
        self.blRegEx = r"[a-f][n-s]"
        self.brRegEx = r"[n-s][n-s]"

        self.emptyCorner = 4
        self.tlSettled = False
        self.trSettled = False
        self.blSettled = False
        self.brSettled = False

    def addMove(self, move):
        #need if for settled corners
        if self.emptyCorner:
            if len(self.tlList) == 0 and (re.match(self.tlRegEx, move)):
                self.tlList.append(move)
                self.emptyCorner -= 1
            elif (len(self.trList) == 0) and (re.match(self.trRegEx, move)):
                self.trList.append(move)
                self.emptyCorner -= 1
            elif (len(self.blList) == 0) and (re.match(self.blRegEx, move)):
                self.blList.append(move)
                self.emptyCorner -= 1
            elif (len(self.brList) == 0) and (re.match(self.brRegEx, move)):
                self.brList.append(move)
                self.emptyCorner -= 1
            else:
                pass
                #Need to consider what happens when a corner piece is approached before a stone is placed in all corners
                #Also when playing tengen and other moves not in 6-6 area (...scrap game because of little time?)
        else:
            #closestCorners = self.closestCorner(move)
            closestJos = self.closestJoseki(move)

            if closestJos == 0:
                self.tlList.append(move)
            elif closestJos == 1:
                self.trList.append(move)
            elif closestJos == 2:
                self.blList.append(move)
            elif closestJos == 3:
                self.brList.append(move)
            elif closestJos == 4:
                self.nonJosekiList.append(move)

    def chebyshevDis(self, currMove, previousMove):
        if len(currMove) != 2:
            return 100
        else:
            distance = max(abs((ord(currMove[0]) - ord(previousMove[0]))), abs((ord(currMove[1]) - ord(previousMove[1]))))
            return distance

    def closestCorner(self, move):
        distances = []      #list with distances from 4 corners in order of tl, tr, bl, br
        #todo corner could be empty!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Same as below
        distances.append(self.chebyshevDis(move, self.tlList[0]))
        distances.append(self.chebyshevDis(move, self.trList[0]))
        distances.append(self.chebyshevDis(move, self.blList[0]))
        distances.append(self.chebyshevDis(move, self.brList[0]))

        minDist = min(distances)
        indices = [index for index, val in enumerate(distances) if val == minDist]
        return indices

    def closestJoseki(self, move):
        distances = []  #list of minimum distances of each joseki array
        tempDist = []   #list of distances in one group, will be cleared and re-used each time

        #check if joseki are too close to each other to settle them!
        #check if closest joseki is too far away

        for prevMove in self.tlList:
            tempDist.append(self.chebyshevDis(move, prevMove))
        if len(tempDist):
            distances.append(min(tempDist))
            tempDist.clear()

        for prevMove in self.trList:
            tempDist.append(self.chebyshevDis(move, prevMove))
        if len(tempDist):
            distances.append(min(tempDist))
            tempDist.clear()

        for prevMove in self.blList:
            tempDist.append(self.chebyshevDis(move, prevMove))
        if len(tempDist):
            distances.append(min(tempDist))
            tempDist.clear()

        for prevMove in self.brList:
            tempDist.append(self.chebyshevDis(move, prevMove))
        if len(tempDist):
            distances.append(min(tempDist))
            tempDist.clear()

        for prevMove in self.nonJosekiList:
            tempDist.append(self.chebyshevDis(move, prevMove))
        if len(tempDist):
            distances.append(min(tempDist))

        if len(distances):
            minDist = min(distances)
            indices = [index for index, val in enumerate(distances) if val == minDist]

            if len(indices) > 1:    #if equally distant to multiple positions not part of joseki
                return 4
            else:

                return indices[0]
        else:
            return -1




with open("test2.sgf") as sgfFile:
    gameCollection = sgf.parse(sgfFile.read())

joseki = JosekiOnBoard()

game = gameCollection[0]
for node in game.rest:
    move = node.current_prop_value[0]
    colour = node.current_property

    joseki.addMove(move)

#game.nodes.append(sgf.Node(game, game.nodes[-1], game.parser))
#theParser = sgf.Parser().parse("(;B[or])")
#game.nodes.append(sgf.Node(game, game.nodes[-1], theParser))
#collection.parser.parse("(;B[or])")
#collection = sgf.parse("(;B[or])")

#with open("output.sgf", "w") as f:
#    collection.output(f)