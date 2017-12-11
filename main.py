import josekiFinder
import CreateOutput

outputCreater = CreateOutput.CreateOutputSgf()
#josekiFinder.findJoseki("test2.sgf", outputCreater)
#josekiFinder.findJoseki("testGame.sgf", outputCreater)
#josekiFinder.findJoseki("test3.sgf", outputCreater)
josekiFinder.findJoseki("test4.sgf", outputCreater)

output = outputCreater.getOutputString()
with open("output.sgf", "w") as f:
    f.write(output)
