import os

from pathlib import Path
from mexp.manager import find
from jpfmanager.jpf import FileManager
from structure.object_indexer import ObjectIndexer

class FDBManager(object):

    def __init__(self, path):      
        self.__listObjects = []        
        self.indexFile = str((Path(path) / type(self).__name__).absolute()) + '.index'        

    @property
    def listObjects(self):
        if len(self.__listObjects) == 0:
            self.getFiles()
        return self.__listObjects

    def addElement(self, fileWithPath, classType, isLoaded):
        existedO = find(self.__listObjects, full_path = fileWithPath)
        if any(existedO):
            self.removeElement(existedO[0])
        self.__listObjects.append(ObjectIndexer(fileWithPath, classType, isLoaded))
        self.save()

    def save(self):
        FileManager.save(self.__listObjects, self.indexFile)

    def removeElement(self, element):
        if any(self.__listObjects):
            self.__listObjects.remove(element)
            self.save()
            
    def removeElements(self, elementsList):
        if any(self.__listObjects):
            for element in elementsList:
                self.__listObjects.remove(elementsList)
            self.save()

    def getFiles(self):
        #get file update date....then make a get if date different from last modified date
        #if self.__listObjects != None:
        #    return self.__listObjects
        if os.path.exists(self.indexFile):
            fileIndex = FileManager.get(self.indexFile)
            if fileIndex != None and fileIndex != False:
                self.__listObjects = fileIndex