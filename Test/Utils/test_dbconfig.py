import os.path
import unittest
import configparser

from Project.Utils import dbconfig

class testDbConfig(unittest.TestCase):
    def setUp(self):
        self.testdbconfigpath = 'testdbconfig.ini'
        self.config = configparser.ConfigParser()
        self.createIniFile()
    def test_testsetup(self):
        self.assertTrue(os.path.exists(self.testdbconfigpath))
        self.assertEqual(self.config.get('KUDA_TEST','user'),'kuda_test')
        self.assertEqual(self.config.get('KUDA_TEST', 'pw'), 'test')
        self.assertEqual(self.config.get('KUDA_TEST', 'sid'), 'sw02')

    def test_dbconfig_init_with_wrong_path(self):
        wrongPath = 'wrongFile.ini'
        with self.assertRaises(dbconfig.DBCONFIGEXCEPTION) as err:
            config = dbconfig.dbconfig(wrongPath)
        self.assertEqual(err.exception.args[0], f'{wrongPath} not a valid path')

    def test_dbconfig_init(self):
        config = dbconfig.dbconfig(self.testdbconfigpath)
        self.assertIsInstance(config, dbconfig.dbconfig)
        self.assertEqual(config.config.get('KUDA_TEST', 'user'), 'kuda_test')
        self.assertEqual(config.config.get('KUDA_TEST', 'pw'), 'test')
        self.assertEqual(config.config.get('KUDA_TEST', 'sid'), 'sw02')

    def test_dbconfig_addDbConfig(self):
        config = dbconfig.dbconfig(self.testdbconfigpath)
        self.assertIsInstance(config, dbconfig.dbconfig)
        config.addDbConfig('KASSA_TEST', 'kassa_test', 'test', 'sw02', self.testdbconfigpath)
        self.assertIsInstance(config, dbconfig.dbconfig)
        self.assertEqual(config.config.get('KASSA_TEST', 'user'), 'kassa_test')
        self.assertEqual(config.config.get('KASSA_TEST', 'pw'),   'test')
        self.assertEqual(config.config.get('KASSA_TEST', 'sid'),  'sw02')

    def test_dbconfig_addDbConfig_with_wrong_path(self):
        config = dbconfig.dbconfig(self.testdbconfigpath)
        wrongPath = 'wrongpath.ini'
        self.assertIsInstance(config, dbconfig.dbconfig)
        with self.assertRaises(dbconfig.DBCONFIGEXCEPTION) as err:
            config.addDbConfig('KASSA_TEST', 'kassa_test', 'test', 'sw02', wrongPath)
        self.assertEqual(err.exception.args[0], f'{wrongPath} not a valid path')

    def test_dbconfig_getSectionsList(self):
        config = dbconfig.dbconfig(self.testdbconfigpath)
        self.assertIsInstance(config, dbconfig.dbconfig)
        keysList = config.getSectionsList()
        print(keysList)
        self.assertIsInstance(keysList, list)
        self.assertEqual('KUDA_TEST',keysList[0])

    def test_dbconfig_getSectionData(self):
        config = dbconfig.dbconfig(self.testdbconfigpath)
        self.assertIsInstance(config, dbconfig.dbconfig)
        dictList = config.getSectionData()
        print(dictList)

    def tearDown(self):
        self.deleteIniFile()

    def createIniFile(self):
        self.config.add_section('KUDA_TEST')
        self.config.set('KUDA_TEST', 'user', 'kuda_test')
        self.config.set('KUDA_TEST', 'pw',   'test')
        self.config.set('KUDA_TEST', 'sid',  'sw02')
        with open(self.testdbconfigpath, 'w') as fh:
            self.config.write(fh)
        fh.close()

    def deleteIniFile(self):
        if os.path.exists(self.testdbconfigpath):
            os.remove(self.testdbconfigpath)

if __name__ == '__main__':
    unittest.main()
