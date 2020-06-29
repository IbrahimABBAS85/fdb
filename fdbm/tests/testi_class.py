
from fdb_base import FDBase

class Testi(FDBase):
    
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Car(FDBase):
    
    def __init__(self, brand, model, year, engine):
        self.brand = brand
        self.model = model
        self.year = year
        self.engine = engine

class Engine(FDBase):
    
    def __init__(self, type, size, origine):
        self.type = type
        self.size = size
        self.origine = origine