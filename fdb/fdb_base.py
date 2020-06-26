import os
import operator
from jpfmanager.jpf import FileManager
from mexp.manager import find
from model_base import FDBModel

class FDBase(object):

    __fileWithPath = None
    __filteredObjectsListWithPath = {}
    __filteredObjectsList = []
    __partial_seach_is_used = False
    isInitialized = True
   
    def saveNew(self, name):
        __fileWithPath = os.path.join(FDBModel.path, name)
        if os.path.exists(__fileWithPath):
            raise Exception("The file you want to save exists, please delete it or change its name then save again.")        
        FileManager.save(self, __fileWithPath)
        FDBModel.manager.addElement(__fileWithPath, FDBase.getClassType(), False)

    def update(self):
        for oPath, obj in FDBase.__filteredObjectsListWithPath.items():
            if obj == self:
                FDBase.__fileWithPath = oPath
                break
        FileManager.save(self, FDBase.__fileWithPath)

    @staticmethod
    def delete(fileName):
        fdbObjectFromIndexer = next(o for o in FDBModel.manager.listObjects if o.full_path == os.path.join(FDBModel.path, fileName))
        #Clean FDBModel.manager.listObjects
        result = FileManager.delete(fdbObjectFromIndexer.full_path)
        if result:
            FDBModel.manager.removeElement(fdbObjectFromIndexer)
            o = FDBase.__filteredObjectsListWithPath[fdbObjectFromIndexer.full_path]
            if o in FDBase.__filteredObjectsList: FDBase.__filteredObjectsList.remove(o)
            del FDBase.__filteredObjectsListWithPath[fdbObjectFromIndexer.full_path]
            
        return result

    @staticmethod
    def deleteAll():
        fdbObjectsFromIndexer = filter(lambda objectF: objectF.object_type == FDBase.getClassType(), FDBModel.manager.listObjects)
        result = False
        listOffdbObjects = list(fdbObjectsFromIndexer)
        for lightItem in listOffdbObjects:
            result = FileManager.delete(lightItem.full_path)
            if result:
                FDBModel.manager.removeElement(lightItem)
                #fix
                o = FDBase.__filteredObjectsListWithPath[lightItem.full_path]
                if o in FDBase.__filteredObjectsList: FDBase.__filteredObjectsList.remove(o)
                del FDBase.__filteredObjectsListWithPath[lightItem.full_path]
                
            else:
                raise Exception("some objects have not been deleted.")

        return result

    @staticmethod
    def get(fileName):
        fdbObjectFromIndexer = None
        try:
            fdbObjectFromIndexer = next(o for o in FDBModel.manager.listObjects if o.full_path == os.path.join(FDBModel.path, fileName))
        except StopIteration:
            pass
        fdbObject = None
        if fdbObjectFromIndexer != None:
            if not fdbObjectFromIndexer.is_loaded:
                fdbObject = FileManager.get(fdbObjectFromIndexer.full_path)
                FDBase.__filteredObjectsListWithPath.update({fdbObjectFromIndexer.full_path:fdbObject})
                FDBase.__filteredObjectsList.append(fdbObject)
                FDBModel.manager.addElement(fdbObjectFromIndexer.full_path,  FDBase.getClassType(), True)
            else:
                try:
                    fdbObject = FDBase.__filteredObjectsListWithPath[fdbObjectFromIndexer.full_path]
                except StopIteration:
                    pass
            pass
        if fdbObject == False:
            return None
        return fdbObject

    @staticmethod
    def getAll():
        FDBase.getAllObjects()
        return FDBase.__filteredObjectsListWithPath

    @classmethod
    def getClassType(cls):
        return cls.__subclasses__()[0].__name__
    
    @staticmethod
    def getAllObjects():
        if not any(FDBase.__filteredObjectsListWithPath) or FDBase.__partial_seach_is_used:
            classType = FDBase.getClassType()
            fdbObjectsFromIndexer = list(filter(lambda objectF: objectF.object_type == cls.__name__, FDBModel.manager.listObjects))
            FDBase.__partial_seach_is_used = False
            if fdbObjectsFromIndexer != None and any(fdbObjectsFromIndexer):
                for lightItem in fdbObjectsFromIndexer:
                    fdbObject = FileManager.get(lightItem.full_path)
                    FDBase.__filteredObjectsListWithPath.update({lightItem.full_path:fdbObject})
                    FDBase.__filteredObjectsList.update(fdbObject)
                    FDBModel.manager.addElement(lightItem.full_path, FDBase.getClassType(), True)

    @staticmethod
    def count():
        return len([objectF for objectF in FDBModel.manager.listObjects if objectF.object_type == FDBase.getClassType()])

    @classmethod
    def exists(fileName):
        fileFullPath = os.path.join(FDBModel.path, fileName)
        return os.path.exists(fileFullPath)
    
    @staticmethod
    def find(**kwargs):
        i = 0
        resultMapping = None
        FDBase.getAllObjects()
        resultMapping = find(FDBase.__filteredObjectsList, **kwargs)
        return resultMapping