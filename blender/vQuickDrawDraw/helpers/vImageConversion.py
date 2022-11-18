import cv2, os
import numpy as np
from PIL import Image
from PIL.ImageQt import ImageQt
from PySide2.QtGui import *

def ImportImagePIL(imagePath):
    # import an image using pillow
    return Image.open(imagePath)

def ImportImageCV2(imagePath):
    # import an image using opencv
    return cv2.imread(imagePath)

def PILToCV2Image(image):
    # convert a pillow image to an opencv image
    nimg = np.array(image)
    ocvim = cv2.cvtColor(nimg, cv2.COLOR_RGB2BGR)
    return ocvim

def CV2ImageToPIL(image):
    # convert an opencv image to a pillow image
    ocvim = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(ocvim)

def ImageToQPixmap(image):
    # Check if the image is a pillow image or an opencv image or string
    if isinstance(image, str):
        image = ImportImageCV2(image)
        return CV2ImageToQPixmap(image)
    if isinstance(image, Image.Image):
        return CV2ImageToQPixmap(PILToCV2Image(image))
    if isinstance(image, np.ndarray):
        return CV2ImageToQPixmap(image)
    return None

def SaveImageToFile(image, filepath):
    outimage = None
    # Check if the image is a pillow image or an opencv image or string
    if isinstance(image, str):
        outimage = ImportImageCV2(image)
    if isinstance(image, Image.Image):
        outimage =  PILToCV2Image(image)
    if isinstance(image, np.ndarray):
        outimage =  image
    # Save cv2 image to filepath
    print("Saving Image")
    cv2.imwrite(filepath, outimage)
    v = 0

def sanitizeImage(image):
    # Check if the image is a pillow image or an opencv image or string
    if isinstance(image, str):
        if os.path.exists(image):
            return ImportImageCV2(image)
        else:
            return None
    if isinstance(image, Image.Image):
        return CV2ImageToQPixmap(PILToCV2Image(image))
    if isinstance(image, np.ndarray):
        return CV2ImageToQPixmap(image)
    return None

def PILImageToQPixmap(image):
    # convert a pillow image to a qtpixmap
    qim = ImageQt(image)
    pix = QPixmap.fromImage(qim)
    return pix

def CV2ImageToQPixmap(image):
    qImg = QImage()
    v = 0
    if image.dtype == np.uint8:
        if len(image.shape) == 2:
            channels = 1
            height, width = image.shape
            bytesPerLine = channels * width
            qImg = QImage(
                image.data, width, height, bytesPerLine, QImage.Format_Indexed8
            )
            qImg.setColorTable([qRgb(i, i, i) for i in range(256)])
        elif len(image.shape) == 3:
            if image.shape[2] == 3:
                height, width, channels = image.shape
                bytesPerLine = channels * width
                qImg = QImage(
                    image.data, width, height, bytesPerLine, QImage.Format_BGR888
                )
            elif image.shape[2] == 4:
                height, width, channels = image.shape
                bytesPerLine = channels * width
                fmt = QImage.Format_ARGB32
                qImg = QImage(
                    image.data, width, height, bytesPerLine, QImage.Format_ARGB32
                )
    return qImg