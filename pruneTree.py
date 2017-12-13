import pickle
import CreateOutput

#josekiList = pickle.load(open("AllGames.p", "rb"))
josekiList = pickle.load(open("2000s.p", "rb"))
#josekiList = pickle.load(open("1900s.p", "rb"))
#josekiList = pickle.load(open("1800s.p", "rb"))
#josekiList = pickle.load(open("1700s.p", "rb"))

removedBySupport = 0

def pruneTree(josekiList):
    numJoseki = 0
    minSup = 0
    counter = len(josekiList) - 1

    while counter >= 0:
        numJoseki += josekiList[counter][2]
        if josekiList[counter][0] == 'sa' or josekiList[counter][0] == 'sb' or josekiList[counter][0] == 'rb' \
        or josekiList[counter][0] == 'rc' or josekiList[counter][0] == 'rd' or josekiList[counter][0] == 're' \
        or josekiList[counter][0] == 'tt':
            josekiList.remove(josekiList[counter])
        counter -= 1
    
    minSup = numJoseki / (4000)
    if minSup < 1:
        minSup = 1
    elif minSup > 10:   #try to keep rare but standard sequences
        minSup = 10

    removeInfrequentSeq(josekiList, minSup)

#travers tree and remove branches smaller with support < minSup
def removeInfrequentSeq(tree, minSup):
    global removedBySupport
    counter = len(tree) - 1

    while counter >= 0:
        if tree[counter][2] < minSup:
            tree.remove(tree[counter])
            removedBySupport += 1
        else:
            removeInfrequentSeq(tree[counter][1], minSup)
        counter -= 1

def sortTree(tree):
    for subtree in tree:
        if len(subtree) and len(subtree[1]):
            sortTree(subtree[1])
    tree.sort(key=lambda x: (x[2]), reverse=True)

pruneTree(josekiList)
print('Removed by Support: %d' % removedBySupport)
sortTree(josekiList)

pickle.dump(josekiList, open("2000s_pruned.p", "wb"))
outputCreater = CreateOutput.CreateOutputSgf()
output = outputCreater.getCustomOutputString(josekiList)
with open("2000s_pruned.sgf", "w") as f:
        f.write(output)