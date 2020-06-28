import os
import operator
from jpfmanager.jpf import FileManager
from mexp.manager import find
from model_base import FDBModel

class FDBase(object):

    def __init__(self):
        self.__fileWithPath = None
        self.isInitialized = True
   
    def saveNew(self, name = None):
        if name == None:
            name =  type(self).__name__ + '_' + str(FDBModel.manager.count(type(self)))
        self.__fileWithPath = os.path.join(FDBModel.path, name)
        if os.path.exists(self.__fileWithPath):
            raise Exception("The file you want to save exists, please delete it or change its name then save again.")        
        FileManager.save(self, self.__fileWithPath)
        FDBModel.manager.addElement(self.__fileWithPath, type(self).__name__, False)

    def update(self):
        FileManager.save(self, FDBModel.manager.findObjectPath(self))