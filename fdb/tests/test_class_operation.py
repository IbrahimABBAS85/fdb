import unittest
import pytest

from pathlib import Path

from model_base import FDBModel
from tests.testi_class import Testi

class Test_Class_Operation(unittest.TestCase):

    def test_save_class_object(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        testp = Testi(5, 'toto')
        testp.saveNew('testi.toto')
        testiObj = Testi.get('testi.toto')
        self.assertIsNotNone(testiObj)
        self.assertEqual(type(testiObj), Testi)
        resultDelete = Testi.delete('testi.toto')
        self.assertEqual(resultDelete, True)
        self.assertEqual(len(FDBModel.manager.listObjects), 0)

    def test_save_class_object_no_path(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        testp = Testi(5, 'toto')
        testp.saveNew()

        testp = Testi(10, 'fofo')
        testp.saveNew()

        testiObj = Testi.find(name='toto')[0]
        self.assertIsNotNone(testiObj)
        self.assertEqual(type(testiObj), Testi)
        resultDelete = Testi.delete(testiObj)
        self.assertEqual(resultDelete, True)
        self.assertEqual(len(FDBModel.manager.listObjects), 1)

        testiObj = Testi.find(name='fofo')[0]
        self.assertIsNotNone(testiObj)
        self.assertEqual(type(testiObj), Testi)
        resultDelete = Testi.delete(testiObj)
        self.assertEqual(resultDelete, True)
        self.assertEqual(len(FDBModel.manager.listObjects), 0)

    def test_save_two_class_object(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        testp = Testi(5, 'toto')
        testp.saveNew('testi.toto')
        testp = Testi(5, 'lolo')
        testp.saveNew('testi2.toto')
        testiObjToto = Testi.get('testi.toto')
        testiObjLolo = Testi.get('testi2.toto')
        self.assertIsNotNone(testiObjToto)
        self.assertEqual(type(testiObjToto), Testi)
        resultDeleteToto = Testi.delete('testi.toto')
        self.assertEqual(resultDeleteToto, True)
        self.assertIsNotNone(testiObjLolo)
        self.assertEqual(type(testiObjLolo), Testi)
        resultDeleteLolo = Testi.delete('testi2.toto')
        self.assertEqual(resultDeleteLolo, True)
        self.assertEqual(len(FDBModel.manager.listObjects), 0)

    def test_get_objects(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.path = pathi
        allObjects = Testi.getAll()
        self.assertIsNotNone(allObjects)

    def test_delete_object(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        testp = Testi(5, 'toto')
        testp.saveNew('testi1.toto')
        testiObj = Testi.get('testi1.toto')
        self.assertIsNotNone(testiObj)
        self.assertEqual(type(testiObj), Testi)
        isDeleted = Testi.delete('testi1.toto')
        self.assertEqual(isDeleted, True)
        testiObj = Testi.get('testi1.toto')
        self.assertIsNone(None)
        
    def test_delete_all_objects(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        testp = Testi(5, 'toto')
        testp.saveNew('testi1.toto')
        testiObj = Testi.get('testi1.toto')
        self.assertIsNotNone(testiObj)
        testp = Testi(5, 'toto')
        testp.saveNew('testi2.toto')
        testiObj = Testi.get('testi2.toto')
        self.assertIsNotNone(testiObj)
        isDeleted = Testi.deleteAll()
        self.assertEqual(isDeleted, True)
        testiObj = Testi.get('testi1.toto')
        self.assertIsNone(None)
        testiObj = Testi.get('testi2.toto')
        self.assertIsNone(None)

    def test_count_all_objects(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        testp = Testi(5, 'toto')
        testp.saveNew('testi1.toto')
        testiObj = Testi.get('testi1.toto')
        self.assertIsNotNone(testiObj)
        testp = Testi(5, 'toto')
        testp.saveNew('testi2.toto')
        testiObj = Testi.get('testi2.toto')
        self.assertIsNotNone(testiObj)
        count = Testi.count()
        self.assertEqual(count, 2)
        isDeleted = Testi.deleteAll()
        self.assertEqual(isDeleted, True)
        testiObj = Testi.get('testi1.toto')
        self.assertIsNone(None)
        testiObj = Testi.get('testi2.toto')
        self.assertIsNone(None)

    def test_update_object(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        testp = Testi(5, 'toto')
        testp.saveNew('testi1.toto')
        testiObj = Testi.get('testi1.toto')
        self.assertIsNotNone(testiObj)
        self.assertEqual(testiObj.name, 'toto')
        testiObj.name = 'titi'
        testiObj.update()
        testiObj = Testi.get('testi1.toto')
        self.assertIsNotNone(testiObj)
        self.assertEqual(testiObj.name, 'titi')        
        isDeleted = Testi.deleteAll()
        self.assertEqual(isDeleted, True)
        testiObj = Testi.get('testi1.toto')
        self.assertIsNone(None)

    def test_find_object_one_argument(self):
        pathi = str((Path(__file__).parent).absolute())
        FDBModel.initialize(pathi)
        testp = Testi(5, 'toto')        
        testp.saveNew('testi1.toto')

        testiObj = Testi.get('testi1.toto')
        self.assertIsNotNone(testiObj)
        
        tobject = Testi.find(name='toto')
        self.assertIsNotNone(tobject)
        self.assertEqual(tobject[0].name, 'toto')
        isDeleted = Testi.deleteAll()
        self.assertEqual(isDeleted, True)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_Class_Operation('test_save_class_object'))
    suite.addTest(Test_Class_Operation('test_save_class_object_no_path'))
    suite.addTest(Test_Class_Operation('test_save_two_class_object'))
    suite.addTest(Test_Class_Operation('test_get_objects'))
    suite.addTest(Test_Class_Operation('test_delete_object'))
    suite.addTest(Test_Class_Operation('test_delete_all_objects'))
    suite.addTest(Test_Class_Operation('test_count_all_objects'))
    suite.addTest(Test_Class_Operation('test_update_object'))
    suite.addTest(Test_Class_Operation('test_find_object_one_argument'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())