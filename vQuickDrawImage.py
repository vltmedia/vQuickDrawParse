# Parse, access, and ,draw an image from a .ndjson QuickDraw file provided by Google
# Author:  Justin Jaro
# Date:    2022-11-18
# LIcense: MIT

import os, json

from helpers.DictClass import DictClass
from averaging import runAveraging

class vQuickDrawImage:
    def __init__(self, filePath, maxLoad = 500):
        self.maxLoad = maxLoad
        self.filePath = filePath
        self.baseName = os.path.basename(os.path.splitext(filePath)[0])
        if os.path.exists(filePath):
            self.parseImage()
        
    def parseImage( self):
        # open the file and read the json data to a variable
        outArray = []
        with open(self.filePath, 'r') as f:
            lines = f.readlines()
            # only keep a certain number of lines based on self.maxLoad
            newLines = lines[-self.maxLoad:]
            lines = newLines
            for line in lines:
                js = json.loads(line)
                drawings = []
                lines = []
                for drawing in js['drawing']:
                    drawX = drawing[0]
                    drawY = drawing[1]
                    for index,item in enumerate(drawX):
                        drawings.append({"x": item, "y": drawY[index]})
                        if index != 0:
                            lines.append({"start": {"x": drawX[index-1], "y": drawY[index-1]}, "end": {"x": item, "y": drawY[index]}})
                js['drawing'] = drawings
                js['lines'] = lines
                v = 0
                outArray.append(DictClass(js))
        self.data = DictClass({"images":outArray})
    
    def getBasicEdges(self, points):
        return  [ [i,i+1] for i in range( len(points)-1) ]
    
    def getDrawing(self, drawingIndex):
        if 0 <= drawingIndex < len(self.data.images):
            return self.data.images[drawingIndex]
        return False
        
    def getDrawingPoints(self, drawingIndex):
        drawing = self.getDrawing(drawingIndex)
        if drawing:
            return drawing.drawing
        return False
    
    def getBlenderMeshData(self,itemName, drawingIndex):
        try:
            import bpy
            mesh = bpy.data.meshes.new(itemName)
            verts, edges = self.getMeshData(drawingIndex)
            mesh.from_pydata(verts, edges = edges, faces=[])
            mesh.update()
        except:
            return "Blender Not Found"
    
    def getMeshData(self, drawingIndex):
        verts = self.getVertices(drawingIndex)
        edges = self.getBasicEdges(verts)
        return [verts, edges]
    
    def getDrawingPoint(self, drawingIndex, pointIndex):
        drawing = self.getDrawing(drawingIndex)
        if drawing:
            points = self.getDrawingPoints(drawingIndex)
            if points:
                return points[pointIndex]
            
    def getLinesAsNumpy(self, drawingIndex, addZ = False):
        drawing = self.getDrawing(drawingIndex)
        if drawing:
            lines = []
            for line in drawing.lines:
                if addZ == False:
                    lines.append([(line['start']['x'], line['start']['y']), (line['end']['x'], line['end']['y'])])
                else:
                    lines.append([(line['start']['x'], line['start']['y'], 0), (line['end']['x'], line['end']['y'], 0)])
            return lines
            # return np.array(lines)
        return False
    
    def getVertices(self, drawingIndex):
        drawing = self.getDrawing(drawingIndex)
        if drawing:
            points = self.getDrawingPoints(drawingIndex)
            lines = []
            for point in points:
                lines.append((point['x'], point['y'], 0))
                    
            return lines
            # return np.array(lines)
        return False
    
    def getLinesAsEdges(self, drawingIndex, addZ = False):
        drawing = self.getDrawing(drawingIndex)
        if drawing:
            lines = []
            for line in drawing.lines:
                if addZ == False:
                    lines.append([[line['start']['x'], line['start']['y']], [line['end']['x'], line['end']['y']]])
                else:
                    lines.append([[line['start']['x'], line['start']['y'], 0], [line['end']['x'], line['end']['y'], 0]])
                    
            return lines
            # return np.array(lines)
        return False
    
    def saveImages(self, directory, maxCount = 10, width=256, height=256, thickness = 5):
        if os.path.exists(directory) == False:
            os.mkdir(directory)
        for indx in range(maxCount):
            savePath = f"{directory}/{self.baseName}_{str(indx).zfill(4)}.png"
            print(f"Drawing Image: {int((indx / maxCount) * 100)}%",savePath )
            img = self.drawImage(indx, width , height, thickness = thickness)
            img.save(savePath)
    
    def drawImage(self, drawingIndex, width=256, height=256, thickness = 5):
        lines = self.getLinesAsNumpy(drawingIndex)
        v = 0
        from PIL import Image, ImageDraw
        
        # creating new Image object
        img = Image.new("RGB", (width, height), color="white")
        
        # create line image
        img1 = ImageDraw.Draw(img) 
        for line in lines:
            img1.line(line, fill ="black", width = thickness)
        return img
    def drawBlenderCurves(self,maxCount = 10, name = "Item"):
        
        import bpy
        new_collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(new_collection)
        for i in range(maxCount):
            itemName = f"{name}_{str(i).zfill(4)}"
            verts, edges = self.getMeshData(i)
            
            mesh = bpy.data.meshes.new(itemName)
            mesh.from_pydata(verts, edges = edges, faces=[])
            mesh.update()


            new_object = bpy.data.objects.new(itemName, mesh)
            # make collection
            #new_collection = bpy.data.collections.new('new_collection')
            
            
            
        # add object to scene collection
            new_collection.objects.link(new_object)
    
    
    def value(self):
        return self.data
        
    @staticmethod
    def getInfo():
        return "vQuickDrawImage: A class for loading Quick Draw images from a .ndjson from Google's Quick Draw dataset"
    
if __name__ == '__main__':
    
    # User Set This
    inputFolder = f"C:/Users/ethic/Desktop/Classes_Fall2022/ComputationalDesign/finalProject/vQuickDrawParse"
    items = ["bee"]
    maxLoad = 500
    saveCount = 500
    
    # User Don't Touch
    for item in items:
        outputFolder = f"{inputFolder}/{item}"
        vQuickDraw_ = vQuickDrawImage(f"{item}.ndjson", maxLoad = maxLoad)
        edges = vQuickDraw_.getLinesAsEdges(0, addZ = True)
        v = 0
        # vQuickDraw_.saveImages(f"{inputFolder}/{item}", saveCount, thickness = 5)
        # runAveraging(inputFolder =outputFolder, outputFile = f"{inputFolder}/{item}_Average.png",showImage=False)
    # value = vQuickDraw_.value()
    # drawing = vQuickDraw_.getDrawing(0)
    v = 0
    # drawingPs = vQuickDraw_.getDrawingPoints(0)
    # lines = vQuickDraw_.getLinesAsNumpy(0)
    v = 0