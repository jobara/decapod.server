import decapod_utilities as utils
import uuid

IMPORT_DIR = "${book}/capturedImages/"
imagePrefix = "decapod-"

class ImageImport(object):
    
    resources = None
    importDir = None

    def __init__(self, resourceSource):
        self.resources = resourceSource
        self.importDir = self.resources.filePath(IMPORT_DIR)
                
        # Setup the import location.
        utils.mkdirIfNecessary(self.importDir)
    
    def generateImageName(self, prefix=imagePrefix, suffix="jpeg"):
        id = uuid.uuid4()
        return "{}{}.{}".format(prefix, id.hex, suffix)
    
    def mimeToSuffix(self, mimeType):
        splitStr = mimeType.split('/')
        return splitStr[-1]
    
    def writeFile(self, file, writePath):
        #Writes the file stream to disk at the path specified by writePath
        file.file.seek(0,0)
        fileData = file.file.read(8192)
        
        while fileData:
            saveFile = open(writePath, 'ab')
            saveFile.write(fileData)
            saveFile.close()
            fileData = file.file.read(8192)
        
        return writePath
    
    def save(self, file, name=None):
        # saves the file with the given name. 
        # if no name is provided it will call genearteImageName to create one
        fileType = self.mimeToSuffix(file.type)
        name = name if name else self.generateImageName(suffix=fileType)
        imagePath = self.importDir + name
        
        return self.writeFile(file, imagePath)