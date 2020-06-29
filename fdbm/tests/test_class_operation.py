import unittest
import pytest

from pathlib import Path

from model_base import FDBModel
from tests.testi_class import Testi, Car, Engine

class Test_Class_Operation(unittest.TestCase):

    def test_save_class_object(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        testp = Testi(5, 'toto')
        testp.saveNew('testi.toto')
        testiObj = FDBModel.manager.get('testi.toto')
        self.assertIsNotNone(testiObj)
        self.assertEqual(type(testiObj), Testi)
        resultDelete = FDBModel.manager.delete('testi.toto')
        self.assertEqual(resultDelete, True)
        self.assertEqual(len(FDBModel.manager.listObjects), 0)

    def test_save_class_object_no_path(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        testp = Testi(5, 'toto')
        testp.saveNew()

        testp = Testi(10, 'fofo')
        testp.saveNew()

        testiObj = FDBModel.manager.find(type_of = Testi, name='toto')[0]
        self.assertIsNotNone(testiObj)
        self.assertEqual(type(testiObj), Testi)
        resultDelete = FDBModel.manager.delete(testiObj)
        self.assertEqual(resultDelete, True)
        self.assertEqual(len(FDBModel.manager.listObjects), 1)

        testiObj = FDBModel.manager.find(type_of = Testi, name='fofo')[0]
        self.assertIsNotNone(testiObj)
        self.assertEqual(type(testiObj), Testi)
        resultDelete = FDBModel.manager.delete(testiObj)
        self.assertEqual(resultDelete, True)
        self.assertEqual(len(FDBModel.manager.listObjects), 0)

    def test_update_class_object_no_path(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        testp = Testi(5, 'toto')
        testp.saveNew()

        testp = Testi(10, 'fofo')
        testp.saveNew()

        testiObj = FDBModel.manager.find(type_of = Testi,name='toto')[0]
        self.assertIsNotNone(testiObj)
        self.assertEqual(type(testiObj), Testi)
        resultDelete = FDBModel.manager.delete(testiObj)
        self.assertEqual(resultDelete, True)
        self.assertEqual(len(FDBModel.manager.listObjects), 1)

        testiObj = FDBModel.manager.find(type_of = Testi,name='fofo')[0]
        self.assertIsNotNone(testiObj)
        self.assertEqual(type(testiObj), Testi)
        self.assertIsNotNone(testiObj)
        self.assertEqual(testiObj.name, 'fofo')
        testiObj.name = 'titi'
        testiObj.update()

        testiObj = FDBModel.manager.find(type_of = Testi,name='titi')[0]
        self.assertIsNotNone(testiObj)
        self.assertEqual(len(FDBModel.manager.listObjects), 1)

        resultDelete = FDBModel.manager.delete(testiObj)
        self.assertEqual(resultDelete, True)
        self.assertEqual(len(FDBModel.manager.listObjects), 0)

    def test_save_two_class_object(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        testp = Testi(5, 'toto')
        testp.saveNew('testi.toto')
        testp = Testi(5, 'lolo')
        testp.saveNew('testi2.toto')
        testiObjToto = FDBModel.manager.get('testi.toto')
        testiObjLolo = FDBModel.manager.get('testi2.toto')
        self.assertIsNotNone(testiObjToto)
        self.assertEqual(type(testiObjToto), Testi)
        resultDeleteToto = FDBModel.manager.delete('testi.toto')
        self.assertEqual(resultDeleteToto, True)
        self.assertIsNotNone(testiObjLolo)
        self.assertEqual(type(testiObjLolo), Testi)
        resultDeleteLolo = FDBModel.manager.delete('testi2.toto')
        self.assertEqual(resultDeleteLolo, True)
        self.assertEqual(len(FDBModel.manager.listObjects), 0)

    def test_get_objects(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.path = pathi
        allObjects = FDBModel.manager.getAll(type_of=Testi)
        self.assertIsNotNone(allObjects)

    def test_delete_object(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        testp = Testi(5, 'toto')
        testp.saveNew('testi1.toto')
        testiObj = FDBModel.manager.get('testi1.toto')
        self.assertIsNotNone(testiObj)
        self.assertEqual(type(testiObj), Testi)
        isDeleted = FDBModel.manager.delete('testi1.toto')
        self.assertEqual(isDeleted, True)
        testiObj = FDBModel.manager.get('testi1.toto')
        self.assertIsNone(None)
        
    def test_delete_all_objects(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        testp = Testi(5, 'toto')
        testp.saveNew('testi1.toto')
        testiObj = FDBModel.manager.get('testi1.toto')
        self.assertIsNotNone(testiObj)
        testp = Testi(5, 'toto')
        testp.saveNew('testi2.toto')
        testiObj = FDBModel.manager.get('testi2.toto')
        self.assertIsNotNone(testiObj)
        isDeleted = FDBModel.manager.deleteAll(type_of=Testi)
        self.assertEqual(isDeleted, True)
        testiObj = FDBModel.manager.get('testi1.toto')
        self.assertIsNone(None)
        testiObj = FDBModel.manager.get('testi2.toto')
        self.assertIsNone(None)

    def test_count_all_objects(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        testp = Testi(5, 'toto')
        testp.saveNew('testi1.toto')
        testiObj = FDBModel.manager.get('testi1.toto')
        self.assertIsNotNone(testiObj)
        testp = Testi(5, 'toto')
        testp.saveNew('testi2.toto')
        testiObj = FDBModel.manager.get('testi2.toto')
        self.assertIsNotNone(testiObj)
        count = FDBModel.manager.count(type_of=Testi)
        self.assertEqual(count, 2)
        isDeleted = FDBModel.manager.deleteAll(type_of=Testi)
        self.assertEqual(isDeleted, True)
        testiObj = FDBModel.manager.get('testi1.toto')
        self.assertIsNone(None)
        testiObj = FDBModel.manager.get('testi2.toto')
        self.assertIsNone(None)

    def test_update_object(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        testp = Testi(5, 'toto')
        testp.saveNew('testi1.toto')
        testiObj = FDBModel.manager.get('testi1.toto')
        self.assertIsNotNone(testiObj)
        self.assertEqual(testiObj.name, 'toto')
        testiObj.name = 'titi'
        testiObj.update()
        testiObj = FDBModel.manager.get('testi1.toto')
        self.assertIsNotNone(testiObj)
        self.assertEqual(testiObj.name, 'titi')        
        isDeleted = FDBModel.manager.deleteAll(type_of=Testi)
        self.assertEqual(isDeleted, True)
        testiObj = FDBModel.manager.get('testi1.toto')
        self.assertIsNone(None)

    def test_find_object_one_argument(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        testp = Testi(5, 'toto')        
        testp.saveNew('testi1.toto')

        testiObj = FDBModel.manager.get('testi1.toto')
        self.assertIsNotNone(testiObj)
        
        tobject = FDBModel.manager.find(type_of = Testi,name='toto')
        self.assertIsNotNone(tobject)
        self.assertEqual(tobject[0].name, 'toto')
        isDeleted = FDBModel.manager.deleteAll(type_of=Testi)
        self.assertEqual(isDeleted, True)

    def test_save_class_object_with_sub_object(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        myEngine = Engine('Essence', 1.8, 'France')
        myCar = Car('Peugeot', '504GL', 1970, myEngine)
        myCar.saveNew()
        myCarObj = FDBModel.manager.find(type_of =Car, brand='Peugeot')
        self.assertIsNotNone(myCarObj)
        self.assertEqual(myCarObj[0].model, '504GL')
        self.assertEqual(myCarObj[0].engine.size, 1.8)
        isDeleted = FDBModel.manager.deleteAll(type_of=Car)
        self.assertEqual(isDeleted, True)

    def test_save_class_object_with_sub_object_with_path(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        myEngine = Engine('Essence', 1.8, 'France')
        myCar = Car('Peugeot', '504GL', 1970, myEngine)
        myCar.saveNew('peugeot.pgt')
        myCarObj = FDBModel.manager.get('peugeot.pgt')
        self.assertIsNotNone(myCarObj)
        self.assertEqual(myCarObj.model, '504GL')
        self.assertEqual(myCarObj.engine.size, 1.8)
        isDeleted = FDBModel.manager.deleteAll(type_of=Car)
        self.assertEqual(isDeleted, True)

    def test_edit_class_object_with_sub_object(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        myEngine = Engine('Essence', 1.8, 'France')
        myCar = Car('Peugeot', '504GL', 1970, myEngine)
        myCar.saveNew()
        myCarObj = FDBModel.manager.find(type_of =Car, brand='Peugeot')
        self.assertIsNotNone(myCarObj)
        self.assertEqual(myCarObj[0].model, '504GL')
        self.assertEqual(myCarObj[0].engine.size, 1.8)
        myCarObj[0].model = '305'
        myCarObj[0].engine.size = 1.6
        myCarObj[0].update()

        myCarObj = FDBModel.manager.find(type_of =Car, brand='Peugeot')
        self.assertIsNotNone(myCarObj)
        self.assertEqual(myCarObj[0].model, '305')
        self.assertEqual(myCarObj[0].engine.size, 1.6)

        isDeleted = FDBModel.manager.deleteAll(type_of=Car)
        self.assertEqual(isDeleted, True)

    def test_delete_class_object_with_sub_object(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        myEngine = Engine('Essence', 1.8, 'France')
        myCar = Car('Peugeot', '504GL', 1970, myEngine)
        myCar.saveNew()
        myCarObj = FDBModel.manager.find(type_of=Car, brand='Peugeot')
        #myCarObj = Car.find(brand='Peugeot')
        self.assertIsNotNone(myCarObj)

        isDeleted = FDBModel.manager.deleteAll(type_of=Car)
        self.assertEqual(isDeleted, True)

    def test_delete_two_different_class_objects(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)

        myEngine = Engine('Essence', 1.8, 'France')
        myEngine.saveNew()
        myCar = Car('Peugeot', '504GL', 1970, myEngine)
        myCar.saveNew()
        
        myCarObj = FDBModel.manager.find(type_of=Car, brand='Peugeot')        
        self.assertIsNotNone(myCarObj)        
        self.assertEqual(len(FDBModel.manager.listObjects), 2)
        myEngineObj = FDBModel.manager.find(type_of=Engine, size=1.8)
        self.assertIsNotNone(myEngineObj)
        
        isDeleted = FDBModel.manager.deleteAll(type_of=Car)
        self.assertEqual(isDeleted, True)
        self.assertEqual(len(FDBModel.manager.listObjects), 1)

        isDeleted = FDBModel.manager.deleteAll(type_of=Engine)
        self.assertEqual(isDeleted, True)
        self.assertEqual(len(FDBModel.manager.listObjects), 0)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_Class_Operation('test_save_class_object'))
    suite.addTest(Test_Class_Operation('test_save_class_object_no_path'))
    suite.addTest(Test_Class_Operation('test_update_class_object_no_path'))
    suite.addTest(Test_Class_Operation('test_save_two_class_object'))
    suite.addTest(Test_Class_Operation('test_get_objects'))
    suite.addTest(Test_Class_Operation('test_delete_object'))
    suite.addTest(Test_Class_Operation('test_delete_all_objects'))
    suite.addTest(Test_Class_Operation('test_count_all_objects'))
    suite.addTest(Test_Class_Operation('test_update_object'))
    suite.addTest(Test_Class_Operation('test_find_object_one_argument'))
    suite.addTest(Test_Class_Operation('test_save_class_object_with_sub_object'))
    suite.addTest(Test_Class_Operation('test_save_class_object_with_sub_object_with_path'))
    suite.addTest(Test_Class_Operation('test_edit_class_object_with_sub_object'))
    suite.addTest(Test_Class_Operation('test_delete_class_object_with_sub_object'))
    suite.addTest(Test_Class_Operation('test_delete_two_different_class_objects'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())