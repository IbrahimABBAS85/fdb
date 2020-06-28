import os

from pathlib import Path
from mexp.manager import find
from jpfmanager.jpf import FileManager
from structure.object_indexer import ObjectIndexer

class FDBManager(object):

    def __init__(self, path):      
        self.__listObjects = []
        self.__path = path
        self.indexFile = str((Path(path) / type(self).__name__).absolute()) + '.index'
        self.__filteredObjectsListWithPath = {}
        self.__filteredObjectsList = []

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
    
    def getAllObjects(self, classType):
        #if not any(self.__filteredObjectsListWithPath) or self.__partial_seach_is_used:
        #check reset  
        fdbObjectsFromIndexer = list(filter(lambda objectF: objectF.object_type == classType and objectF.is_loaded == False, self.listObjects))
        self.__partial_seach_is_used = False
        if fdbObjectsFromIndexer != None and any(fdbObjectsFromIndexer):
            for lightItem in fdbObjectsFromIndexer:
                fdbObject = FileManager.get(lightItem.full_path)
                self.__filteredObjectsListWithPath.update({lightItem.full_path:fdbObject})
                self.__filteredObjectsList.append(fdbObject)
                self.addElement(lightItem.full_path, classType, True)

    def find(self, type_of, **kwargs):
        i = 0
        resultMapping = None
        self.getAllObjects(type_of.__name__)
        listToFilter = list(filter(lambda o: type(o) == type_of, self.__filteredObjectsList))
        resultMapping = find(listToFilter, **kwargs)
        return resultMapping

    def getAll(self, type_of):
        self.getAllObjects(type_of.__name__)
        return self.__filteredObjectsListWithPath

    def count(self, type_of):
        return len([objectF for objectF in self.listObjects if objectF.object_type == type_of.__name__])

    def deleteAll(self, type_of):
        fdbObjectsFromIndexer = filter(lambda objectF: objectF.object_type == type_of.__name__, self.listObjects)
        result = False
        listOffdbObjects = list(fdbObjectsFromIndexer)
        for lightItem in listOffdbObjects:
            result = FileManager.delete(lightItem.full_path)
            if result:
                self.removeElement(lightItem)
                #fix
                o = self.__filteredObjectsListWithPath[lightItem.full_path]
                if o in self.__filteredObjectsList: self.__filteredObjectsList.remove(o)
                del self.__filteredObjectsListWithPath[lightItem.full_path]
                
            else:
                raise Exception("some objects have not been deleted.")

        return result
        
    def get(self, fileName):
        fdbObjectFromIndexer = None
        try:
            fdbObjectFromIndexer = next(o for o in self.listObjects if o.full_path == os.path.join(self.__path, fileName))
        except StopIteration:
            pass
        fdbObject = None
        if fdbObjectFromIndexer != None:
            if not fdbObjectFromIndexer.is_loaded:
                fdbObject = FileManager.get(fdbObjectFromIndexer.full_path)
                self.__filteredObjectsListWithPath.update({fdbObjectFromIndexer.full_path:fdbObject})
                self.__filteredObjectsList.append(fdbObject)
                self.addElement(fdbObjectFromIndexer.full_path, type(fdbObject).__name__, True)
            else:
                try:
                    fdbObject = self.__filteredObjectsListWithPath[fdbObjectFromIndexer.full_path]
                except StopIteration:
                    pass
            pass
        if fdbObject == False:
            return None
        return fdbObject
        
    def delete(self, target):
        #string or object
        fdbObjectFromIndexer = None
        if type(target) is str:
            fileWithPath = os.path.join(self.__path, target)
        else:
            fileWithPath = self.findObjectPath(target)
        fdbObjectFromIndexer = next(o for o in self.listObjects if o.full_path == fileWithPath)
        #Clean FDBModel.manager.listObjects
        result = FileManager.delete(fdbObjectFromIndexer.full_path)
        if result:
            self.removeElement(fdbObjectFromIndexer)
            o = self.__filteredObjectsListWithPath[fdbObjectFromIndexer.full_path]
            if o in self.__filteredObjectsList: self.__filteredObjectsList.remove(o)
            del self.__filteredObjectsListWithPath[fdbObjectFromIndexer.full_path]
            
        return result

    def findObjectPath(self, target):
        for oPath, obj in self.__filteredObjectsListWithPath.items():
            if obj == target:
                return oPath