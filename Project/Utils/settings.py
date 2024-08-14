import configparser
import os

"""
TODO add method that creates basic config.ini file when file is empty (option check if it necessary to create file always)
"""
class mcsettings:
    """
    A class for managing settings using configparser.
    """

    def __init__(self, settingsPath: str = os.path.join(os.path.abspath(os.sep), 'config.ini')):
        """
        Initializes the mcsettings class.

        Args:
        settingsPath (str): The path to the settings file. Defaults to 'config.ini' in the root directory.

        Returns:
        None
        """
        self.configpath = settingsPath
        self.config = configparser.ConfigParser()
        self.config.read(self.configpath)

    def __storeSettings(self, store: bool):
        if store:
            with open(self.configpath, 'w') as fh:
                self.config.write(fh)
        else:
            None

    def getStringForSectionKey(self, section: str, option: str) -> str:
        """
        Retrieves a string value for a given section and key from the settings file.

        Args:
        section (str): The section name.
        option (str): The key within the section.

        Returns:
        str: The string value associated with the section and key.

        Raises:
        configparser.NoSectionError: If the specified section does not exist in the settings file.
        configparser.KeyError: If the specified key does not exist within the section.
        """
        return self.config.get(section, option)

    def createNewSection(self, section: str, store: bool = True):
        """
        Creates a new section in the settings file if it doesn't exist.

        Args:
        section_name (str): The name of the section to be created.

        Returns:
        None

        Raises:
        configparser.DuplicateSectionError - Raised when a section is attempted to be added with a name that is already in the configuration.
        """
        self.config.add_section(section)
        self.__storeSettings(store)


    def addEntryToSection(self, section: str, option: str, value: str, store: bool = True):
        """
        Adds an entry to the specified section in the settings configuration.

        Args:
        section (str): The name of the section where the entry will be added.
        option (str): The name of the option to be added.
        value (str): The value to be assigned to the option.
        store (bool, optional): Indicates whether the updated settings should be stored.
            Defaults to True.

        Returns:
        None

        Raises:
        configparser.NoSectionError - Raised when a specified section is not found in the configuration.
        configparser.DuplicateOptionError - Raised when an option is attempted to be added with a name that is already in the section.
        """
        self.config.set(section, option, value)
        self.__storeSettings(store)


"""
configparser Errors:

Error - This is the base class for all exceptions raised by configparser.
NoSectionError - Raised when a specified section is not found in the configuration.
DuplicateSectionError - Raised when a section is attempted to be added with a name that is already in the configuration.
NoOptionError - Raised when a specified option is not found in the specified section.
DuplicateOptionError - Raised when an option is attempted to be added with a name that is already in the section.
NoSectionError - Raised when attempting to retrieve an option or value from a non-existent section.
InterpolationError - This is the base class for all interpolation-related exceptions.
"""