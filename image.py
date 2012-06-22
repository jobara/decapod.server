import os
import decapod_utilities as utils
import imghdr
import zipfile

BOOK_DIR = "${library}/book/images/"
IMG_DIR = BOOK_DIR + "img/"
TEMP_DIR = IMG_DIR + "temp/"

class ConversionError(Exception): pass
class ImageError(Exception): pass
class OutputPathError(Exception): pass

def convert(imagePath, format, outputDir=None):
    '''
    Converts the image at imagePath into the specified image format
    Can optionaly specify the directory where to save the new file, will default to the same directory as the original file.
    If the format is invalid, it will convert it to jpeg
    Returns the path to the new image file.
    
    Exceptions:
    ImageError: if the file at imagePath isn't a supported image format
    ConversionError: an error occurs during the conversion process
    '''
    if utils.isImage(imagePath):
        ext = format if format[0] == "." else "." + format
        origDir, fileName = os.path.split(imagePath)
        name = os.path.splitext(fileName)[0]
        writeDir = outputDir if outputDir != None else origDir
        
        writePath = os.path.join(writeDir, name + ext)
        utils.invokeCommandSync(["convert", imagePath, writePath], ConversionError, "Error converting {0} to '{1}' format".format(imagePath, format))
        return writePath
    else:
        raise ImageError("{0} is not a valid image file".format(imagePath))

def batchConvert(imagePaths, format, outputDir=None):
    '''
    Converts the image at imagePath into the specified image format
    Can optionaly specify the directory where the converted images will be saved, will default to putting them back into their original directories.
    If the path provided is not an image, it will be ignored.
    If the format is invalid, it will convert it to jpeg
    Returns a list of the paths to the new image files
    
    Exceptions:
    ConversionError: an error occurs during the conversion process
    '''
    convertedImages = []
    for imagePath in imagePaths:
        if utils.isImage(imagePath):
            convertedImage = convert(imagePath, format, outputDir)
            convertedImages.append(convertedImage)
    return convertedImages

def archiveConvert(imagePaths, format, archivePath, tempDir=None):
    '''
    Converts the images in the list of imagePaths to tiff format.
    Must specify the output path, including the file name, for the zip file to be saved.
    If the image path provided is not an image, it will be ignored.
    Can optionally specify a temp derictory for use during conversion, 
    it will default to creating a temp directory in the current working directory.
    Note that in all cases, the temp directory will be removed after completion.
    Returns a path to the zip file containing the converted images.
    If no valid images were provided, None is returned
    
    Exceptions:
    ConversionError: an error occurs during the conversion process
    OutputPathError: the output path is malformed (e.g. path to a directory)
    '''
    result = archivePath
    currentDir = os.getcwd()
    temp = tempDir if tempDir != None else os.path.join(os.getcwd(), "temp")
    utils.makeDirs(tempDir)
    converted = batchConvert(imagePaths, format, temp)
    os.chdir(tempDir) # Need to change to the tempDir where the images are so that the zip file won't contain any directory structure
    if len(converted) > 0:
        try:
            zip = zipfile.ZipFile(archivePath, mode="a")
        except IOError:
            raise OutputPathError("{0} is not a valid path".format(archivePath))
        for imagePath in converted:
            imageFile = os.path.split(imagePath)[1] # extacts the filename from the path
            zip.write(imageFile)
        zip.close()
    else:
        # Return None when there are no valid image paths
        result = None
    
    os.chdir(currentDir)
    utils.rmTree(tempDir)
    return result