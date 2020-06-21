import os

from jpfmanager.jpf import FileManager

from model_base import FDBModel

class FDBase(object):
    def __init__(self):
        self.__fileWithPath = None

    def saveNew(self, name):        
        self.__fileWithPath = os.path.join(FDBModel.path, name)
        if os.path.exists(self.__fileWithPath):
            raise Exception("The file you want to save exists, please delete it or change its name then save again.")
        FDBModel.manager.addElement(self.__fileWithPath, type(self))
        FileManager.save(self, self.__fileWithPath)

    def update(self):
        FileManager.save(self, self.__fileWithPath)

    @classmethod
    def delete(self, fileName):
        fdbObjectFromIndexer = next(o for o in FDBModel.manager.listObjects if o.full_path == os.path.join(FDBModel.path, fileName))
        #Clean FDBModel.manager.listObjects
        result = FileManager.delete(fdbObjectFromIndexer.full_path)        
        if result:
            FDBModel.manager.removeElement(fdbObjectFromIndexer)
        return result

    @classmethod
    def deleteAll(self):
        fdbObjectsFromIndexer = filter(lambda objectF: objectF.object_type == self, FDBModel.manager.listObjects)
        result = False
        for lightItem in list(fdbObjectsFromIndexer):
            result = FileManager.delete(lightItem.full_path)
            if result:
                FDBModel.manager.removeElement(lightItem)
            else:
                raise Exception("some objects have not been deleted.")

        return result

    @classmethod
    def get(self, fileName):
        fdbObjectFromIndexer = None
        try:
            fdbObjectFromIndexer = next(o for o in FDBModel.manager.listObjects if o.full_path == os.path.join(FDBModel.path, fileName))
        except StopIteration:
            pass
        fdbObject = None
        if fdbObjectFromIndexer != None:
            fdbObject = FileManager.get(fdbObjectFromIndexer.full_path)
        if fdbObject == False:
            return None
        return fdbObject

    @classmethod
    def getAll(self):
        filteredObjectsList = []
        fdbObjectsFromIndexer = list(filter(lambda objectF: objectF.object_type == self, FDBModel.manager.listObjects))

        if fdbObjectsFromIndexer != None and any(fdbObjectsFromIndexer):
            for lightItem in fdbObjectsFromIndexer:
                filteredObjectsList.append(FileManager.get(lightItem.full_path))
            
        return filteredObjectsList 

    @classmethod
    def count(self):
        return len([objectF for objectF in FDBModel.manager.listObjects if objectF.object_type == self])
    
    @classmethod
    def exists(self, fileName):
        fileFullPath = os.path.join(FDBModel.path, fileName)
        return os.path.exists(fileFullPath)
    
    @classmethod
    def find(self, **kwargs):
        for key, value in kwargs.items(): 
            print ("%s == %s" %(key, value))
        #fom keys to lambda...