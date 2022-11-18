# Description
Parse, access, and ,draw an image from a .ndjson QuickDraw file provided by Google. Finally save out the images in the dataset easier.

# Requirements
- PIL
- Python 3.7 +

# Usage:
``` python
items = ["TheMonaLisa", "bee", "bicycle"]
maxLoad = 500
saveCount = 500
for item in items:
    outputFolder = f"F:/Projects/CodeDump/GoogleQuickDraw/{item}"
    inputFolder = f"F:/Projects/CodeDump/GoogleQuickDraw"
    
    vQuickDraw_ = vQuickDrawImage(f"{item}.ndjson", maxLoad = maxLoad)
    vQuickDraw_.saveImages(f"F:/Projects/CodeDump/GoogleQuickDraw/{item}", saveCount, thickness = 5)
    
    runAveraging(inputFolder =outputFolder, outputFile = f"{inputFolder}/{item}_Average.png",showImage=False)
# value = vQuickDraw_.value()
# drawing = vQuickDraw_.getDrawing(0)
v = 0
# drawingPs = vQuickDraw_.getDrawingPoints(0)
# lines = vQuickDraw_.getLinesAsNumpy(0)
```