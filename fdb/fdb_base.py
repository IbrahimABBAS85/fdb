import os
from jpfmanager.jpf import FileManager

class FDBase(object):

    def __init__(self, path):
        self.__path = path
        print('base')

    def save(self, name):
        print(self.path)
        FileManager.save(self, os.path.join( self.path, name))

    def update(self):
        print(self.path)

    @classmethod
    def delete(self, obj):
        print(self.path)

    @classmethod
    def deleteAll(self):
        print(self.path)

    @classmethod
    def get(self, id):
        return None

    @classmethod
    def getAll(self, id):
        return None

    @classmethod
    def count(self, id):
        return None
    
    @classmethod
    def exists(self, id):
        return None
    
    @classmethod
    def find(self, **kwargs):
        for key, value in kwargs.items(): 
            print ("%s == %s" %(key, value))
        #fom keys to lambda...