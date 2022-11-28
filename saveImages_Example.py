from vQuickDrawImage import vQuickDrawImage
from averaging import runAveraging, runBlackMasking


def runProcess(inputFolder, items, maxLoad, saveCount, thickness):
    # User Don't Touch
    for item in items:
        outputFolder = f"{inputFolder}/{item}"
        vQuickDraw_ = vQuickDrawImage(f"{item}.ndjson", maxLoad = maxLoad)
        vQuickDraw_.saveImages(f"{inputFolder}/{item}", saveCount, thickness = thickness)
        runAveraging(inputFolder =outputFolder, outputFile = f"{inputFolder}/{item}_Average.png",showImage=False)




def runOpacityLayeringProcess(inputFolder, items, maxLoad, saveCount, thickness, opacity = 2, invert = False):
    # User Don't Touch
    for item in items:
        inputPath = f"{inputFolder}/{item}"
        vQuickDraw_ = vQuickDrawImage(f"{inputPath}.ndjson", maxLoad = maxLoad)
        vQuickDraw_.saveImages(f"{inputFolder}/{item}", saveCount, thickness = thickness)
        runBlackMasking(inputPath, f"{inputFolder}/{item}_OpacityLayered.png", opacity=opacity, invert=invert,clampRange= [0,255], useMinimum=False)





# User Set This
inputFolder = f"C:/Users/ethic/Desktop/Classes_Fall2022/ComputationalDesign/finalProject/vQuickDrawParse"
items = ["bee"]
maxLoad = 50
saveCount = 50
thickness = 1

# # Run Process here
# runProcess(inputFolder, items, maxLoad, saveCount, thickness)

opacity = 1
invert = True
# Run Opacity Layering Process here
runOpacityLayeringProcess(inputFolder, items, maxLoad, saveCount, thickness, opacity, invert)