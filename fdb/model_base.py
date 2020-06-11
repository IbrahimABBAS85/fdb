class FDBModel(object):
    def __init__(self, path):
        self.__path = path      
    
    def addClasse(self, fdbclass):
        fdbclass.path = self.__path

    def addClasses(self, fdbclassList):
        for fdbClass in fdbclassList:
            fdbClass.path = self.__path    