from pathlib import Path

from model_base import FDBModel
from fdb_base import FDBase

class testi(FDBase):
    def __init__(self):        
        print('Ok')

if __name__ == '__main__':
    pathi = str((Path(__file__).parent).absolute())
    modulos = FDBModel(pathi)
    testp = testi()
    modulos.addClasse(testp)
    testp.save('testi')