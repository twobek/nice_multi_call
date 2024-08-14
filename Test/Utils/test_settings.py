import os
import unittest
import configparser
from Project.Utils.settings import mcsettings

class test_settings(unittest.TestCase):

    def setUp(self):
        self.testSettingsPath = os.path.join(os.path.join(os.path.dirname(__file__), 'Ressources'), 'test_settings.ini')
        self.testConfig = configparser.ConfigParser()
        self.testSectionOne = 'testSection1'
        self.testSectionTwo = 'testSection2'
        self.__createBaseConfig()

    def tearDown(self):
        if os.path.exists(self.testSettingsPath):
            os.remove(self.testSettingsPath)

    def __createBaseConfig(self):
        self.testConfig.add_section(self.testSectionOne)
        self.testConfig.add_section(self.testSectionTwo)
        self.testConfig.set(self.testSectionOne,'testKey','testValue')
        self.testConfig.set(self.testSectionTwo, 'someKey', 'someValue')
        with open(self.testSettingsPath, 'w') as fh:
            self.testConfig.write(fh)

    def test_if_test_settings_file_exists(self):
        self.assertTrue(os.path.exists(self.testSettingsPath))

    def test_if_test_settings_file_contains_predefined_values(self):
        config = configparser.ConfigParser()
        config.read(self.testSettingsPath)
        self.assertTrue(config.has_section(self.testSectionOne))
        self.assertTrue(config.has_section(self.testSectionTwo))
        self.assertEqual('testValue', config.get(self.testSectionOne, 'testKey'))
        self.assertEqual('someValue', config.get(self.testSectionTwo, 'someKey'))

    def test_getStringForSectionKey_NoSectionError_is_raised_when_section_does_not_exist(self):
        config = mcsettings(self.testSettingsPath)
        with self.assertRaises(configparser.NoSectionError) as e:
            config.getStringForSectionKey('NotValid_section', 'someKey')

    def test_getStringForSectionKey_NoOptionError_is_raised_when_option_does_not_exist(self):
        config = mcsettings(self.testSettingsPath)
        with self.assertRaises(configparser.NoOptionError) as e:
            config.getStringForSectionKey(self.testSectionOne, 'wrongKey')

    def test_getStringForSectionKey_returns_valid_value(self):
        config = mcsettings(self.testSettingsPath)
        self.assertEqual('testValue', config.getStringForSectionKey(self.testSectionOne, 'testKey'))

    def test_createNewSection_DuplicateSectionError_is_raised_when_section_already_in_ini_file(self):
        config = mcsettings(self.testSettingsPath)
        with self.assertRaises(configparser.DuplicateSectionError) as e:
            config.createNewSection(self.testSectionOne)

    def test_createNewSection_creates_new_section_and_stores_it_on_disk(self):
        config = mcsettings(self.testSettingsPath)
        self.assertFalse(config.config.has_section('newSection'))
        config.createNewSection('newSection')
        new_config = mcsettings(self.testSettingsPath)
        self.assertTrue(new_config.config.has_section('newSection'))

    def test_addEntryToSection_creates_new_key_value_in_file_and_stores_on_disk(self):
        config = mcsettings(self.testSettingsPath)
        self.assertFalse(config.config.has_option(self.testSectionOne, 'newOption'))
        config.addEntryToSection(self.testSectionOne,'newOption', 'newValue')
        self.assertEqual(config.config.get(self.testSectionOne, 'newOption'), 'newValue')
        newConfig = mcsettings(self.testSettingsPath)
        self.assertEqual(newConfig.config.get(self.testSectionOne, 'newOption'), 'newValue')

    def test_addEntryToSection_raises_NoSectionError_when_section_does_not_exist(self):
        None
    def test_addEntryToSection_raises_DuplicateOptionError_Option_already_exists(self):
        config = mcsettings(self.testSettingsPath)
        with self.assertRaises(configparser.DuplicateOptionError) as e:
            config.addEntryToSection(self.testSectionOne, 'testKey', 'testValue')

    """
    TODO check why test_addEntryToSection_raises_DuplicateOptionError_Option_already_exists doesn't raise configparser.DuplicateOptionError
    TODO complete test_addEntryToSection_raises_NoSectionError_when_section_does_not_exist 
    TODO add testmethod that config.ini hast needed Entries for Program 
    """