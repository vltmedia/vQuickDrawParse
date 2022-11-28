import copy
import os, numpy, PIL, glob
from PIL import Image
import numpy as np

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def runBlackMasking(inputFolder, outputFile, showImage = True, clampRange = [0,255], invert= True, opacity = 3, useMinimum = False):
    # Access all PNG files in directory
    allfiles=os.listdir(inputFolder)
    imlist=[filename for filename in allfiles if  filename[-4:] in [".png",".PNG"]]
    print("inputFolder", inputFolder)
    v = 0
    # Assuming all images are the same size, get dimensions of first image
    w,h=Image.open(os.path.join(inputFolder, imlist[0])).size
    N=len(imlist)
    # Create a numpy array of floats to store the average (assume RGB images)
    compedImage=numpy.zeros((h,w,4),numpy.uint8)
    # Set 3 index in compedImage npArray to 255
    compedImage[:,:,3] = 255
    images = []
    opacityvalue =opacity
    # opacityvalue =255 *  (5 / (len(imlist) - 1))
    v = 0
    # Build up average pixel intensities, casting each image as an array of floats
    for indx ,im in enumerate( imlist):
        perc = indx / (len(imlist) - 1)
        # perc = 1 / (len(imlist) - 1)
        fullpath = os.path.join(inputFolder, im)
        imarr=Image.open(fullpath).convert('RGB')
        # invert Image
        inverted = imarr
        if invert:
            inverted = PIL.ImageOps.invert(imarr)
        # na = cv2.imread(fullpath)

        # Make a True/False mask of pixels whose BGR values sum to more than zero
        alpha = np.sum(inverted, axis=-1) > 0

        # Convert True/False to 0/255 and change type to "uint8" to match "na"
        alpha = np.uint8(alpha * opacityvalue)

        # Stack new alpha layer with existing image to go from BGR to BGRA, i.e. 3 channels to 4 channels
        currentImage = np.dstack((inverted, alpha))
        background = compedImage
        compedImage = np.array( Image.alpha_composite(Image.fromarray(background).convert('RGBA'), Image.fromarray(currentImage).convert('RGBA')))

        
        v = 0
    outputBaseSplit = os.path.splitext(os.path.basename(outputFile))
    outputDir = os.path.dirname(outputFile)
    # Generate, save and preview final image
    # averagedout=Image.fromarray(averagednp,mode="RGB")
    out=Image.fromarray(compedImage,mode="RGBA")
    # out2=Image.fromarray(avg_img,mode="RGB")
    
    out.save(f"{outputDir}/{outputBaseSplit[0]}_averagedOpacity.png")
    # averagedout.save(f"{outputDir}/{outputBaseSplit[0]}_averagedColor.png")
    # # Generate, save and preview final image
    # out2.save(outputFile)
    if showImage:
        out.show()
        # out2.show()
        # averagedout.show()
        pass


def runAveraging(inputFolder, outputFile, showImage = True, clampRange = [0,255], useMinimum = False):
    # Access all PNG files in directory
    allfiles=os.listdir(inputFolder)
    imlist=[filename for filename in allfiles if  filename[-4:] in [".png",".PNG"]]
    print("inputFolder", inputFolder)
    v = 0
    # Assuming all images are the same size, get dimensions of first image
    w,h=Image.open(os.path.join(inputFolder, imlist[0])).size
    N=len(imlist)

    # Create a numpy array of floats to store the average (assume RGB images)
    arr=numpy.zeros((h,w,3),numpy.uint8)
    images = []
    # Build up average pixel intensities, casting each image as an array of floats
    for im in imlist:
        fullpath = os.path.join(inputFolder, im)
        imarr=numpy.array(Image.open(fullpath).convert('RGB'))
        shapee = imarr.shape
        minval = np.min(imarr[np.nonzero(imarr)])
        maxval = np.max(imarr[np.nonzero(imarr)])
        v = 0
        # if imarr.shape[2] == 4 :
        #     imarr.reshape((3, 2))
        images.append(imarr)
            # v = 0images
        arr=arr+imarr/N

    # Round values in array and cast as 8-bit integer
    arr=numpy.array(numpy.round(arr),dtype=numpy.uint8)
    avg_img = np.mean(arr)
    averaged = []
    v = 0
    for item in arr:
        for point in item:
            for indx in range(3):
                point[indx] = translate(point[indx], clampRange[0], clampRange[1], 0, 255)
    # for indx, item in enumerate(images[0]):
    #     v = 0
    #     mean = np.mean( [drawing[indx] for drawing in images], axis=0)
    #     averaged.append(mean)
                
    if useMinimum:
        minval = np.min(arr[np.nonzero(arr)])
        maxval = np.max(arr[np.nonzero(arr)])
        v = 0
        for item in arr:
            for point in item:
                for indx in range(3):
                    point[indx] = translate(point[indx],  minval, maxval, 0, 255,)
    
    # averagednp = numpy.array(numpy.round(averaged),dtype=numpy.uint8)
    
    # newmax 
    v = 0
    outputBaseSplit = os.path.splitext(os.path.basename(outputFile))
    outputDir = os.path.dirname(outputFile)
    # Generate, save and preview final image
    # averagedout=Image.fromarray(averagednp,mode="RGB")
    out=Image.fromarray(arr,mode="RGB")
    # out2=Image.fromarray(avg_img,mode="RGB")
    
    out.save(f"{outputDir}/{outputBaseSplit[0]}_averagedBasic.png")
    # averagedout.save(f"{outputDir}/{outputBaseSplit[0]}_averagedColor.png")
    # # Generate, save and preview final image
    # out2.save(outputFile)
    if showImage:
        out.show()
        # out2.show()
        # averagedout.show()
        pass

def main():
    inputFolder = "F:/Projects/CodeDump/GoogleQuickDraw/bee"

    runBlackMasking(inputFolder, "F:/Projects/CodeDump/GoogleQuickDraw/bee_mask_average.png", opacity=2, invert=True,clampRange= [0,255], useMinimum=False)
    # runAveraging(inputFolder, "F:/Projects/CodeDump/GoogleQuickDraw/faces_average.png", clampRange= [0,255], useMinimum=False)

if __name__ == "__main__":
    main()