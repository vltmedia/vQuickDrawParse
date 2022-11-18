import os, numpy, PIL, glob
from PIL import Image

def runAveraging(inputFolder, outputFile, showImage = True):
    # Access all PNG files in directory
    allfiles=os.listdir(inputFolder)
    imlist=[filename for filename in allfiles if  filename[-4:] in [".png",".PNG"]]
    print("inputFolder", inputFolder)
    v = 0
    # Assuming all images are the same size, get dimensions of first image
    w,h=Image.open(os.path.join(inputFolder, imlist[0])).size
    N=len(imlist)

    # Create a numpy array of floats to store the average (assume RGB images)
    arr=numpy.zeros((h,w,3),numpy.float)

    # Build up average pixel intensities, casting each image as an array of floats
    for im in imlist:
        fullpath = os.path.join(inputFolder, im)
        imarr=numpy.array(Image.open(fullpath).convert('RGB'),dtype=numpy.float)
        shapee = imarr.shape
        v = 0
        # if imarr.shape[2] == 4 :
        #     imarr.reshape((3, 2))

            # v = 0
        arr=arr+imarr/N

    # Round values in array and cast as 8-bit integer
    arr=numpy.array(numpy.round(arr),dtype=numpy.uint8)

    # Generate, save and preview final image
    out=Image.fromarray(arr,mode="RGB")
    out.save(outputFile)
    if showImage:
        out.show()

# def main():
#     inputFolder = "F:/Projects/CodeDump/GoogleQuickDraw/baseBallBat"

#     runAveraging(inputFolder, "F:/Projects/CodeDump/GoogleQuickDraw/baseballbat.png")

# if __name__ == "__main__":
#     main()