import sgf

#something something Pre-fix Span tree?? To account for sub-trees in larger ones fitting into others?

class CreateOutputSgf(object):
    def __init__(self):
        self.josekiList = []    #contains joseki in form of other lists containing [move, childMoves[], frequency]
        self.numVariations = 0  #total number of variations
        self.numMoves = 0       #total number of moves in list

    def addJoseki(self, moveList):
        self.correctSymmetry(moveList)
        currentTree = self.josekiList   #list of current moves aka all 1st, 2nd, etc
        deepestBranchFound = False

        if len(self.josekiList) == 0:
            for move in moveList:
                currentTree.append([move, [], 1])
                currentTree = currentTree[0][1]
        else:
            for move in moveList:
                if not deepestBranchFound:
                    tree = [node[0] for node in currentTree]
                if not deepestBranchFound and move in tree:
                    currentTree[tree.index(move)][2] += 1
                    currentTree = currentTree[tree.index(move)][1]    #currentTree = child list
                else:   
                    #add as deeply as possible
                    currentTree.append([move, [], 1])
                    currentTree = currentTree[-1][1]
                    deepestBranchFound = True

            
    #mirror everything to top right
    def correctSymmetry(self, moveList):
        x = moveList[0][0]
        y = moveList[0][1]
        xVal = ord(x) - ord('a')
        yVal = ord(y) - ord('a')
        middle = 9  #middle of board 19x19 board starting count from 0
        badSymmetry = True
        checkedSym  = False
        symmetricPt = [ 'aa','bb','cc','dd','ee','ff','gg','hh','ii','jj','kk','ll','mm','nn','oo','pp','qq','rr','ss',
                        'as','br','cq','dp','eo','fn','gm','hl','ik','ki','lh','mg','nf','oe','pd','qc','rb','sa','tt'] #BAD PRACTICE

        #UGLY CODE !!!
        if xVal < middle and yVal > middle:     #bottom left - need to make 2 mirrors
            for i in range(len(moveList)):
                move = moveList[i]
                if not checkedSym and move not in symmetricPt:
                    badSymmetry = self.inTriangle(move, 2)
                    checkedSym = True
                if move != "tt":
                    if not badSymmetry:
                        xVal = ord(move[0]) - ord('a')
                        yVal = ord(move[1]) - ord('a')
                        moveList[i] = chr((18 - xVal) + ord('a')) + chr((18 - yVal) + ord('a'))
                    else:
                        moveList[i] = move[1] + move [0]
        elif xVal < middle:                     #top left - mirror horizontally
            for i in range(len(moveList)):
                move = moveList[i]
                if not checkedSym and move not in symmetricPt:
                    badSymmetry = self.inTriangle(move, 0)
                    checkedSym = True
                if move != "tt":
                    if badSymmetry:
                        move = move[1] + move[0]
                    xVal = ord(move[0]) - ord('a')
                    y = move[1]
                    moveList[i] = chr((18 - xVal) + ord('a')) + y
        elif yVal > middle:                     #bottem right - mirror vertically
            for i in range(len(moveList)):
                move = moveList[i]
                if not checkedSym and move not in symmetricPt:
                    badSymmetry = self.inTriangle(move, 3)
                    checkedSym = True
                if move != "tt":
                    if badSymmetry:
                        move = move[1] + move[0]
                    yVal = ord(move[1]) - ord('a')
                    x = move[0]
                    moveList[i] = x + chr((18 - yVal) + ord('a'))
        else:                                   #top left
            for i in range(len(moveList)):
                move = moveList[i]
                if not checkedSym and move not in symmetricPt:
                    badSymmetry = self.inTriangle(move, 1)
                    checkedSym = True
                if move != "tt":
                    if checkedSym:
                        if not badSymmetry:
                            break
                        else:
                            moveList[i] = move[1] + move[0]
                            yVal = ord(move[0]) - ord('a')
                            xVal = ord(move[1]) - ord('a')
                            moveList[i] = chr((18 - xVal) + ord('a')) + chr((18 - yVal) + ord('a'))          

    #determine if move is in correct "triangle" within corner
    #uses barycentric coordinates
    def inTriangle(self, move, cornerIndex):
        xVal = ord(move[0]) - ord('a')
        yVal = ord(move[1]) - ord('a')
        coordinateSet = [[1, 0, 9, 8, 9, 0],
                         [9, 0, 9, 8, 17, 0],
                         [1, 18, 9, 18, 9, 10],
                         [9, 18, 17, 18, 9, 10]]
        p0x = coordinateSet[cornerIndex][0]
        p0y = coordinateSet[cornerIndex][1]
        p1x = coordinateSet[cornerIndex][2]
        p1y = coordinateSet[cornerIndex][3]
        p2x = coordinateSet[cornerIndex][4]
        p2y = coordinateSet[cornerIndex][5]
        
        area = 0.5 *(-p1y*p2x + p0y*(-p1x + p2x) + p0x*(p1y - p2y) + p1x*p2y)
        sign = 1
        if area < 0:
            sign = -1
        s = (p0y*p2x - p0x*p2y + (p2y - p0y)*xVal + (p0x - p2x)*yVal) * sign
        t = (p0x*p1y - p0y*p1x + (p0y - p1y)*xVal + (p1x - p0x)*yVal) * sign

        if s >= 0 and t >= 0 and (s+t) <= 2 * abs(area):
            return True
        else:
            return False

    def getOutputString(self):
        output = "(;GM[1]FF[4]AP[JosekiFinder]SZ[19]CA[UTF-8]"
        moveString = self.createOutputString(self.josekiList, 'B')
        output += 'C[Total Variations: ' + str(self.numVariations - 1)
        output += '\nTotal Moves: ' + str(self.numMoves) + ']'
        output += moveString
        output += ')'
        return output

    def getCustomOutputString(self, customList):
        output = "(;GM[1]FF[4]AP[JosekiFinder]SZ[19]CA[UTF-8]"
        moveString = self.createOutputString(customList, 'B')
        output += 'C[Total Variations: ' + str(self.numVariations - 1)
        output += '\nTotal Moves: ' + str(self.numMoves) + ']'
        output += moveString
        output += ')'
        return output

    #recursive pre-order depth-first traversal of my tree
    #returns the final string
    def createOutputString(self, tree, colour):
        output = ""
        if len(tree) == 0:
            output += ')'
            self.numVariations += 1
            return output
        else:
            if colour == 'B':
                nextColour = 'W'
            else:
                nextColour = 'B'

            for subTree in tree:
                self.numMoves += 1
                if len(tree) > 1:
                    output += '('
                output += ';'
                output += colour
                output += '['
                output += subTree[0]
                output += ']'
                output += 'C[Support: '     #add comment with frequency of move
                output += str(subTree[2])
                output += ']'
                output += self.createOutputString(subTree[1], nextColour)
                if len(subTree[1]) > 1:
                    output += ')'
                    self.numVariations += 1

            return output

