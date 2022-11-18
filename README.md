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

# Blender Addon
![Image](.\blender\vQuickDrawDraw\media\vQuickDraw_DrawPanel.jpg)

## Description
Draw the drawings in an ```.ndjson``` to a max count as Blender Curves.
## Installation
The Blender addon is provided in the blender directory of this codebase, just zip it up, or the Releases area of this Github Repo.

Go to this link for a tutorial on how to install a Blender addon [LINK](https://github.com/rlguy/Blender-FLIP-Fluids/wiki/Addon-Installation-and-Uninstallation).
