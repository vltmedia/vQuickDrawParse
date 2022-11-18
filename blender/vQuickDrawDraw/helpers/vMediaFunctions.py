import copy
import glob
import re
import cv2, os
import numpy as np
from PIL import Image
import pickle

class vVideoInfo:
    # set init values by kwargs
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.currentItemIndex = 0
        self.items = []
        try:
            if kwargs['items'] is not None:
                self.items = kwargs['items']
        except:
            pass
        
    def __str__(self):
        return str(self.__dict__)
    def update(self, **kwargs):
        self.__dict__.update(kwargs)
        
    # Copy values from another vVideoInfo object
    def copySource(self, other):
        self.__dict__.update(other.__dict__)
    
    # Save the video info to a .vVidInfo file using pickle
    def saveToFile(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
            
    # Load the video info from a .vVidInfo file using pickle
    def loadFromFile(self, filepath):
        with open(filepath, 'rb') as f:
            return pickle.load(f)
        
    def getNewFPSFrameCount(self, oldFPS, newFPS):
        return float(newFPS) / float(oldFPS)
        
    def getCurrentItem(self):
        return self.items[self.currentItemIndex]
    
    def getNextItem(self):
        if self.currentItemIndex < len(self.items):
            self.currentItemIndex += 1
            return self.items[self.currentItemIndex]
        else:
            return self.items[self.currentItemIndex]
        
    def getPreviousItem(self):
        if self.currentItemIndex > 0:
            self.currentItemIndex -= 1
            return self.items[self.currentItemIndex]
        else:
            return self.items[self.currentItemIndex]

def getVideoInfo(path):
    if os.path.exists(path):
        cap = cv2.VideoCapture(path)
        file_stats = os.stat(path)
        ty = "MB"
        sizee = file_stats.st_size / (1024 * 1024)
        if sizee / 1024 > 1:
            ty = "GB"
            sizee = sizee / 1024
        # size to GB from MB
        mediaSize = sizee
        vInfo = vVideoInfo(size=mediaSize, fps=cap.get(cv2.CAP_PROP_FPS), width=cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                        height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT), totalFrames=copy.deepcopy(cap.get(7)),
                        sizeText=f'{mediaSize:.2f} {ty}'
                        )
        v = 0
        # close the cap object
        cap.release()
        return vInfo
def getImageInfo(path):
    if os.path.exists(path):
        cap = cv2.imread(path)
        file_stats = os.stat(path)
        ty = "MB"
        sizee = file_stats.st_size / (1024 * 1024)
        if sizee / 1024 > 1:
            ty = "GB"
            sizee = sizee / 1024
        # size to GB from MB
        mediaSize = sizee
        vInfo = getSequenceInfo(path)
        vInfo.update(size=cap.shape, width=cap.shape[1],
                        height=cap.shape[0], channels=cap.shape[2],
                        sizeText=f'{mediaSize:.2f} {ty}'
                        )
        # close the cap object
        del cap
        return vInfo
    
def parseGProImageSequence(path):
    mo = re.findall('\d+', path)
    groupNumber = mo[-1][:3]
    fileNumber = mo[-1][-4:]
    zcount = len(fileNumber)
    zcountperc = "%0" + str(zcount) + "d"
    globPattern = path.replace(fileNumber, '*')
    
    files = glob.glob(f"{path.replace(fileNumber, '*')}")
    sequenceCount = len(files)
    v = 0
    vVideoInfo_ = vVideoInfo(groupNumber=int(groupNumber), fileNumber=int(fileNumber),
                            zeroPaddingCount = zcount, zeroPaddingCountPercent = zcountperc,
                            sequenceCount=sequenceCount, sequenceType="gopro",
                            firstFile = files[0], lastFile = files[-1],
                            globPattern=f"{path.replace(fileNumber, '*')}",
                            firstNumber = int(getNumberSequencesFromPath(files[0])[-1]), lastNumber = int(getNumberSequencesFromPath(files[-1])[-1]),
                            sequenceFilePattern=f"{path.replace(fileNumber, zcountperc)}",
                            items = files,
                            fileExtension=os.path.splitext(path)[1].replace(".", "").lower())
    return vVideoInfo_
        
def getNumberSequencesFromPath(path):
    basename = os.path.basename(path)
    mo = re.findall('\d+', basename)
    return mo
    
def getSequenceInfo(path, sequenceType = "image"):
    basename = os.path.basename(path)
    # parse the basename splitting it by the zero padding
    # and get the number of digits
    # and the file extension
    # and the file name
    vVideoInfo_ = None
    filepath = path
    mo = getNumberSequencesFromPath(path)
    if basename[0] == "G" and len(mo[0]) == 7:
        sequenceType = "gopro"
    if sequenceType.lower() == "gopro":
        vVideoInfo_ = parseGProImageSequence(filepath)
    else:
        zcount = len(mo[-1])
        zcountperc = "%0" + str(zcount) + "d"
        files = glob.glob(f"{path.replace(mo[-1], '*')}")
        globPattern = path.replace(mo[-1], '*')
        sequenceCount = len(files)
        v = 0
        
        vVideoInfo_ = vVideoInfo(groupNumber=int(0), fileNumber=int(mo[-1]),
                                zeroPaddingCount = zcount, zeroPaddingCountPercent = zcountperc,
                                globPattern=f"{path.replace(mo[-1], '*')}",
                                sequenceFilePattern=f"{path.replace(mo[-1], zcountperc)}",
                                sequenceCount=sequenceCount, sequenceType=sequenceType,
                                firstFile = files[0], lastFile = files[-1],
                                firstNumber = int(getNumberSequencesFromPath(files[0])[-1]), lastNumber = int(getNumberSequencesFromPath(files[-1])[-1]),
                                items = files,
                                fileExtension=os.path.splitext(path)[1].replace(".", "").lower())
    return vVideoInfo_
    

def getMediaInfo(path):
    ospath = os.path.splitext(path)[1].replace(".", "").lower()
    vids = ["mp4", "avi", "mov", "mkv", "webm", "flv", "wmv", "mpg", "mpeg", "m4v", "3gp", "3g2"]
    images = ["jpg", "jpeg", "png", "bmp", "gif", "tiff", "tif", "exr"]
    if ospath in vids:
        return getVideoInfo(path)
    elif ospath in images:
        return getImageInfo(path)

def getFileCountBasedOnFilePattern(pattern):
    return len(glob.glob(pattern.replace("%0d", "*").replace("%01d", "*").replace("%02d", "*").replace("%03d", "*").replace("%04d", "*").replace("%05d", "*").replace("%06d", "*")))


if __name__ == '__main__':
    path = "E:/Temp/Mocap/SourceVids/out2/fram4636e_0001.png"
    path = "P:/datasets/Ethica/3dTimeplapse/CardA/G0021345.JPG"
    seqInfo = getSequenceInfo(path, "image")
    # seqInfo = getSequenceInfo(path, "gopro")
    v = 0