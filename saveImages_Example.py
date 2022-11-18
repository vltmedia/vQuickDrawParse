from vQuickDrawImage import vQuickDrawImage
from averaging import runAveraging


def runProcess(inputFolder, items, maxLoad, saveCount):
    # User Don't Touch
    for item in items:
        outputFolder = f"{inputFolder}/{item}"
        vQuickDraw_ = vQuickDrawImage(f"{item}.ndjson", maxLoad = maxLoad)
        vQuickDraw_.saveImages(f"{inputFolder}/{item}", saveCount, thickness = 5)
        runAveraging(inputFolder =outputFolder, outputFile = f"{inputFolder}/{item}_Average.png",showImage=False)





# User Set This
inputFolder = f"C:/Users/ethic/Desktop/Classes_Fall2022/ComputationalDesign/finalProject/vQuickDrawParse"
items = ["bush"]
maxLoad = 500
saveCount = 500

# Run Process here
runProcess(inputFolder, items, maxLoad, saveCount)