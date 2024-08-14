import os
import unittest
from dataclasses import asdict
from unittest.mock import mock_open, patch
from Project.Utils.dbList import dbList, DBLISTUTILSEXCEPTION, DBLISTKEYEXISTS, DBLISTKEYNOTEXISTS, dbObject

class TestDbList(unittest.TestCase):

    def setUp(self):
        """
        Method to set up necessary resources for each test case.

        This method initializes instance variables such as testRessourcesPath, test_dblist_file, base_db_list, and dblist_instance for use in the test cases.
        """
        self.testRessourcesPath = os.path.join(os.path.dirname(__file__), 'Ressources')
        self.test_dblist_file = os.path.join(self.testRessourcesPath,'test_dblist.json')
        self.base_db_list = {"dev": {}, "test": {}, "prod_a": {}, "prod_s": {}, "prod": {}}
        self.dblist_instance = dbList(self.test_dblist_file)

    def tearDown(self):
        """
        Method to clean up resources after each test case.

        This method removes the test_dblist_file if it exists after the test case has been executed.
        """
        if os.path.exists(self.test_dblist_file):
            os.remove(self.test_dblist_file)

    def test_read_dblist_existing_file(self):
        """
        Test case to verify the reading of the dbList from an existing file.

        This test case uses mocking to simulate the reading of a test dbList file and compares the result with the expected dbList content.
        """
        with patch("builtins.open", mock_open(read_data='{"dev": {"1": "data1"}}')):
            expected_dblist = {"dev": {"1": "data1"}}
            result = self.dblist_instance.readDbList(self.test_dblist_file)
            self.assertEqual(result, expected_dblist)

    def test_create_base_dblist_json(self):
        """
        Test case to verify the creation of the base dbList JSON file.

        This test case verifies that the base dbList JSON is created correctly and matches the expected base_db_list.
        """
        expected_base_dblist = self.base_db_list.copy()
        result = self.dblist_instance._dbList__createBaseDBListJson(self.test_dblist_file)
        self.assertEqual(result, expected_base_dblist)

    def test_get_prod_list(self):
        """
        Test case to verify the retrieval of the production list.

        This test case checks the correctness of the production list returned by the getProdList method.
        """
        expected_prod_list = ["dev", "test", "prod_a", "prod_s", "prod"]
        result = self.dblist_instance.getProdList()
        self.assertEqual(result, expected_prod_list)

    def test_get_keys_for_instance_list_existing_instance(self):
        """
        Test case to verify the retrieval of keys for an existing database instance.

        This test case checks if the keys returned for an existing database instance match the expected keys.
        """
        instance = "dev"
        expected_keys = []
        result = self.dblist_instance.getKeysForInstanceList(instance)
        self.assertEqual(result, expected_keys)

    def test_get_keys_for_instance_list_non_existing_instance(self):
        """
        Test case to verify the handling of a non-existing database instance.

        This test case verifies that an exception (DBLISTUTILSEXCEPTION) is raised when attempting to retrieve keys for a non-existing database instance.
        """
        non_existing_instance = "missing_instance"
        with self.assertRaises(DBLISTUTILSEXCEPTION):
            self.dblist_instance.getKeysForInstanceList(non_existing_instance)

    def test_addDbTypeToInstance_with_wronge_instance(self):
        """
        Test case to verify the behavior when adding a database type to a wrong instance.

        This test case checks that a DBLISTUTILSEXCEPTION is raised when attempting to add a database type to an incorrect instance.
        """
        with self.assertRaises(DBLISTUTILSEXCEPTION):
            self.dblist_instance.addDbTypeToInstance('hugo', 'kassa_test')

    def test_addDbTypeToInstance_with_correct_instance_correct_dbType(self):
        """
        Test case to verify the addition of a database type to a correct instance.

        This test case adds a database type 'intc_dev' to the 'dev' instance and compares the resulting dbListDict with the expected dictionary.
        """
        expected_dict = self.base_db_list.copy()
        expected_dict['dev']['intc_dev'] = {}
        self.dblist_instance.addDbTypeToInstance('dev', 'intc_dev')
        self.assertEqual(expected_dict,self.dblist_instance.dbListDict)

    def test_addDbTypeToInstance_with_already_existing_db_type(self):
        """
        Test case to verify behavior when adding an already existing database type to a database instance.

        Steps:
        1. Create a copy of the base_db_list for comparison.
        2. Add the 'intc_dev' database type to the 'dev' instance in the expected_dict.
        3. Add 'intc_dev' database type to the 'dev' instance in the dbListDict.
        4. Verify that adding 'intc_dev' again to the 'dev' instance raises a DBLISTKEYEXISTS exception.

        Args:
        - self: The test case instance.
        """
        expected_dict = self.base_db_list.copy()
        expected_dict['dev']['intc_dev'] = {}
        self.dblist_instance.addDbTypeToInstance('dev', 'intc_dev')
        self.assertEqual(expected_dict, self.dblist_instance.dbListDict)
        with self.assertRaises(DBLISTKEYEXISTS):
            self.dblist_instance.addDbTypeToInstance('dev', 'intc_dev')

    def test_addDbToDbType_with_wrong_instance(self):
        """
        Test case to verify behavior when adding a database object to a wrong instance.

        This test case attempts to add a database object to a non-existing instance 'wrongInstance'
        and verifies that it raises a DBLISTUTILSEXCEPTION.
        """
        dbObj = dbObject('kassa_dev', 'test', 'SW02')
        self.assertIsInstance(dbObj,dbObject)
        with self.assertRaises(DBLISTUTILSEXCEPTION):
            self.dblist_instance.addDbToDbType('wrongInstance', 'kassa_dev', dbObj)

    def test_addDbToDbType_with_already_existing_db_type(self):
        """
            Test case to verify behavior when adding a database object to a database type that already exists in the dbListDict.

            Steps:
            1. Create a copy of the base_db_list for comparison.
            2. Create a dbObject instance for testing.
            3. Verify that the dbObject is an instance of the dbObject class.
            4. Add the new dbObject to the expected_dict for comparison.
            5. Set the dbListDict in dblist_instance to the expected_dict.
            6. Verify that adding a dbObject to an already existing db_type raises a DBLISTKEYEXISTS exception.

            Args:
            - self: The test case instance.
        """
        expected_dict = self.base_db_list.copy()
        dbObj = dbObject('intc_dev', 'test', 'SW18')
        self.assertIsInstance(dbObj, dbObject)
        expected_dict['dev']['intc_dev'] = asdict(dbObj)
        self.dblist_instance.dbListDict = expected_dict
        with self.assertRaises(DBLISTKEYEXISTS):
            self.dblist_instance.addDbToDbType('dev', 'intc_dev', dbObj)

    def test_addDbToDbType_with_dbObj_is_wrong_class(self):
        """
        Test case to verify behavior when adding a database object of the wrong class to a database type.

        This test case creates a dbObject instance of the wrong class and verifies that it raises an Exception.
        """
        expected_dict = self.base_db_list.copy()
        dbObj = dbObject('intc_dev', 'intc_dev', 'test', 'SW18')
        self.assertIsInstance(dbObj, dbObject)
        expected_dict['dev']['intc_dev'] = asdict(dbObj)
        self.dblist_instance.dbListDict = expected_dict
        with self.assertRaises(Exception):
            self.dblist_instance.addDbToDbType('dev', dbObj)

    def test_addDbToDbType_with_valid_parameters(self):
        expected_dict = self.base_db_list.copy()
        dbObj = dbObject('intc_dev', 'test', 'SW18')
        self.assertIsInstance(dbObj, dbObject)
        expected_dict['dev']['intc_dev'] = asdict(dbObj)
        self.dblist_instance.addDbToDbType('dev', 'intc_dev', dbObj)
        self.assertEqual(expected_dict, self.dblist_instance.dbListDict)

    # Add more test methods to cover other functionalities

if __name__ == '__main__':
    unittest.main()