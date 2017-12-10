import sgf

#something something Pre-fix Span tree?? To account for sub-trees in larger ones fitting into others?

class CreateOutputSgf(object):
    def __init__(self):
        self.josekiList = []    #contains joseki in form of other lists containing [move, childMoves[], frequency]

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

        #UGLY CODE !!!
        if xVal < middle and yVal > middle:     #bottom left - need to make 2 mirrors
            for move in range(len(moveList)):
                if moveList[move] != "tt":
                    xVal = ord(moveList[move][0]) - ord('a')
                    yVal = ord(moveList[move][1]) - ord('a')
                    moveList[move] = chr((18 - xVal) + ord('a')) + chr((18 - yVal) + ord('a'))
        elif xVal < middle:                     #top left - mirror horizontally
            for move in range(len(moveList)):
                if moveList[move] != "tt":
                    xVal = ord(moveList[move][0]) - ord('a')
                    y = moveList[move][1]
                    moveList[move] = chr((18 - xVal) + ord('a')) + y
        elif yVal > middle:                     #bottem right - mirror vertically
            for move in range(len(moveList)):
                if moveList[move] != "tt":
                    yVal = ord(moveList[move][1]) - ord('a')
                    x = moveList[move][0]
                    moveList[move] = x + chr((18 - yVal) + ord('a'))

    def getOutputString(self):
        output = "(;GM[1]FF[4]AP[JosekiFinder]SZ[19]CA[UTF-8]"                     #Customize!!!!
        output += self.createOutputString(self.josekiList, 'B')
        output += ')'
        return output

    #recursive pre-order depth-first traversal of my tree
    #returns the final string
    def createOutputString(self, tree, colour):
        output = ""
        if len(tree) == 0:
            output += ')'
            return output
        else:
            if colour == 'B':
                nextColour = 'W'
            else:
                nextColour = 'B'

            for subTree in tree:
                if len(tree) > 1:
                    output += '('
                output += ';'
                output += colour
                output += '['
                output += subTree[0]
                output += ']'
                output += self.createOutputString(subTree[1], nextColour)
                if len(subTree[1]) > 1:
                    output += ')'

            return output

