import glob, os
import time
import pickle
import josekiFinder
import CreateOutput

gameDirectories = ['D:/GoGoD/Database/Games',
                    'D:/GoGoD/Database/Games/2000s',
                    'D:/GoGoD/Database/Games/1900s',
                    'D:/GoGoD/Database/Games/1800s',
                    'D:/GoGoD/Database/1700-99']
listNames = ['AllGames',
             '2000s',
             '1900s',
             '1800s',
             '1700s']

def run(directory, name):
    outputCreater = CreateOutput.CreateOutputSgf()
    outputDir = 'D:\GoGoD\Database\Dictionary Results'
    pickleName = name + '.p'
    outputName = name + '_output.sgf'
    
    os.chdir(directory)
    
    startTime = time.time()
    files = glob.glob("**/*.sgf", recursive=True)

    if outputName in files:
        files.remove(outputName)

    numFiles = len(files)
    i = 1
    for file in files:
        josekiFinder.findJoseki(file, outputCreater)
        i += 1
        if i % 10 == 0:
            print('%s: %0.2f%%' % (name, ((i/numFiles)*100)))
    print("--- %s seconds ---" % (time.time() - startTime))

    output = outputCreater.getOutputString()
    os.chdir(outputDir)
    pickle.dump(outputCreater.josekiList, open(pickleName, "wb"))   #dump josekiList so I don't have to rerun
    with open(outputName, "w") as f:
        f.write(output)

failures = []
if len(gameDirectories) == len(listNames):
    for i in range(len(gameDirectories)):
        try:
            run(gameDirectories[i], listNames[i])
        except Exception as e:
            failures.append(listNames[i])

    if len(failures):
        for failure in failures:
            print("Failed to finish: %s" % failure)
    else:
        print("All runs successful")
else:
    print("Lenght of directories and names do not match")
