import re
import sgf
import CreateOutput

class JosekiOnBoard(object):
    def __init__(self):
        self.josekiList = []    #this list contains the other lists so that I can access them in a loop

        self.tlList = ['aa'] #top-left
        self.trList = ['sa'] #top-right
        self.blList = ['as'] #bottom-left
        self.brList = ['ss'] #bottom-right
        self.nonJosekiList = [] #for stones not part of joseki

        self.josekiList.append(self.tlList)
        self.josekiList.append(self.trList)
        self.josekiList.append(self.blList)
        self.josekiList.append(self.brList)
        self.josekiList.append(self.nonJosekiList)

        #need to add passes if last colour is same as currently added colour
        self.lastColourPlayed = ['B', 'B', 'B', 'B']

        self.emptyCorners = [True, True, True, True]
        self.settledCorners = []
        self.numUnsettledCorners = 4

        self.tlSettled = False
        self.trSettled = False
        self.blSettled = False
        self.brSettled = False

        self.settledCorners.append(self.tlSettled)
        self.settledCorners.append(self.trSettled)
        self.settledCorners.append(self.blSettled)
        self.settledCorners.append(self.brSettled)

    def addMove(self, move, colour):
        #Also when playing tengen and other moves not in 6-6 area (...scrap game because of little time?)
        closestJosIndex = self.closestJoseki(move)
        currentList = self.josekiList[closestJosIndex]

        #if len(self.emptyCorners[closestJosIndex]) == 1 and re.match(self.initialRegEx, currentList[0]):
        if closestJosIndex < 4 and self.emptyCorners[closestJosIndex]:
            currentList[0] = move
            self.lastColourPlayed[closestJosIndex] = colour
            self.emptyCorners[closestJosIndex] = False
        else:
            ko = 0
            if len(currentList):
                ko = currentList.count(move)

            if closestJosIndex < 4:  #0-3 are corners, 4 is non-joseki
                if self.lastColourPlayed[closestJosIndex] == colour:
                    currentList.append('tt')
                
                self.lastColourPlayed[closestJosIndex] = colour            
            #if ko joseki is done
            if ko and closestJosIndex < 4:
                self.settledCorners[closestJosIndex] = True
            else:
                currentList.append(move)
                

    def chebyshevDis(self, currMove, previousMove):
        if len(currMove) != 2:
            return 100
        else:
            distance = max(abs((ord(currMove[0]) - ord(previousMove[0]))), abs((ord(currMove[1]) - ord(previousMove[1]))))
            return distance

    def closestJoseki(self, move):
        distances = []  #list of minimum distances of each joseki array
        tempDist = []   #list of distances in one group, will be cleared and re-used each time
        MAX_JOSEKI_LEN = 20
        MAX_NON_JOSEKI_LEN = 50

        for jList in self.josekiList:
            for prevMove in jList:
                tempDist.append(self.chebyshevDis(move, prevMove))
            if len(tempDist):
                distances.append(min(tempDist))
                tempDist.clear()

        if len(distances):
            minDist = min(distances)
            closestJosekiFound = [index for index, val in enumerate(distances) if val == minDist]   #list of the index of closest joseki
            #allClosedJoseki = [i for i, val in enumerate(distances) if val < 3]    #number of joseki within distance of 2 or less

            if closestJosekiFound[0] < 4:
                cornerSettled = self.settledCorners[closestJosekiFound[0]]
            else:
                cornerSettled = False

            #if equally distant to multiple positions not part of joseki
            if len(closestJosekiFound) > 1 or cornerSettled:
                return 4
            #elif len(allClosedJoseki) > 1:
            #    for corner in allClosedJoseki:
            #        if corner != 4:
            #            self.settledCorners[corner] = True
            #    return 4
            else:
                closestJosekiLen = len(self.josekiList[closestJosekiFound[0]])

                if (minDist > 5 or 
                    closestJosekiLen >= 10 and minDist > 2 or
                    closestJosekiLen >= 4 and minDist > 3 or
                    closestJosekiLen >= MAX_JOSEKI_LEN):
                    
                    if closestJosekiLen >= MAX_JOSEKI_LEN:  #this should only be entered once per corner
                        if closestJosekiFound[0] < 4:
                            self.settledCorners[closestJosekiFound[0]] = True
                            self.numUnsettledCorners -= 1
                        else:   #number of non joseki stones are greater than Max
                            if closestJosekiLen >= MAX_NON_JOSEKI_LEN:
                                self.numUnsettledCorners = 0
                    return 4
                else:
                    return closestJosekiFound[0]
        else:
            return -1   #error, all distances are empty

def findJoseki(inFile, outputCreater):
    movesPlayed = 0
    joseki = JosekiOnBoard()

    with open(inFile) as sgfFile:
        gameCollection = sgf.parse(sgfFile.read())

    game = gameCollection[0]

    for node in game.rest:  #first node is header info
        move = node.current_prop_value[0]
        colour = node.current_property

        joseki.addMove(move, colour)
        movesPlayed += 1
        if joseki.numUnsettledCorners <= 0:
            break

    for jList in joseki.josekiList[:-1]:
        outputCreater.addJoseki(jList)

    #print('Total moves played in %s: %d' % (inFile, movesPlayed))
