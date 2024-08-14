import os
import json
from dataclasses import dataclass, asdict
from typing import Optional

dbConfigPath = os.path.dirname(__file__)

class DBLISTUTILSEXCEPTION(Exception):
    """
    Custom exception class for handling exceptions specific to dbList utilities.
    """
    pass


class DBLISTKEYEXISTS(DBLISTUTILSEXCEPTION):
    """
    Custom exception Class which is raised when db list key allready exists
    """
    pass

class DBLISTKEYNOTEXISTS(DBLISTUTILSEXCEPTION):
    """
    Custom Exception Class which is raised when a dbList-key does not exist
    """
    pass

@dataclass
class dbObject:
    user: str
    pw: str
    sid: str
    reSelected: Optional[bool] = None

class dbList:
    """
    The dbList class provides utilities for interacting with a database list stored in a JSON file.

    Attributes:
    - configPath (str): The path to the configuration file ('dblist.json' by default).
    - dbListDict (dict): A dictionary containing the database list read from the configuration file.

    Methods:
    - __init__(self, configPath: str = os.path.join(dbConfigPath, 'dblist.json')) -> dict:
      Initializes the dbList object and reads the database list from the specified JSON file.

    - readDbList(self, path: str) -> dict:
      Reads the database list from the specified file path and returns it as a dictionary.

    - __createBaseDBListJson(self, path: str) -> dict:
      Creates the base database list if the file does not exist and returns the base database list dictionary.

    - __createJsonFile(self, path: str, dbDict: dict):
      Creates a JSON file with the specified database dictionary at the given path.

    - __checkKeysForInstance(self, instance: str) -> bool:
      Checks if a given instance key exists in the database list dictionary.

    - getProdList(self) -> list:
      Returns a list of database instance keys from the database list dictionary.

    - getKeysForInstanceList(self, instance: str) -> list:
      Returns a list of database entry keys for a given instance from the database list dictionary.

    - addDbTypeToInstance(self, instance: str, dbType: str):
      Adds a database type entry to a database instance in the database list dictionary.

    - addDbToDbType(self, instance: str, dbObj: dbObject ):
      Adds a database entry to a specified database type in the database list dictionary.

    Usage:
    - Instantiate the dbList object to access the database list utilities.
    - Use the provided methods to retrieve database lists or perform related operations.

    Example:
    ```
    db = dbList()
    prod_list = db.getProdList()
    print(prod_list)
    ```
    """
    def __init__(self, configPath: str = os.path.join(dbConfigPath, 'dblist.json')):
        """
        Initializes the dbList object and reads the database list from the specified JSON file.

        Args:
        - configPath (str): The path to the configuration file ('dblist.json' by default).
        """
        self.configPath = configPath
        self.dbListDict = self.readDbList(self.configPath)

    def __createBaseDBListJson(self, path: str) -> dict:
        """
        Creates the base database list if the file does not exist and returns the base database list dictionary.

        Args:
        - path (str): The file path for the database list JSON file.

        Returns:
        - dict: The base database list dictionary.
        """
        baseDbList = {"dev": {}, "test": {}, "prod_a": {}, "prod_s": {}, "prod": {}}
        self.__createJsonFile(path, baseDbList)
        return baseDbList

    def __createJsonFile(self, path: str, dbDict: dict):
        """
        Creates a JSON file with the specified database dictionary at the given path.

        Args:
        - path (str): The file path for the JSON file.
        - dbDict (dict): The database dictionary to be written to the file.

        Raises:
        - DBLISTUTILSEXCEPTION: If an error occurs during file creation.
        """
        try:
            with open(path, 'w') as fh:
                json.dump(dbDict, fh)
        except Exception as e:
            raise DBLISTUTILSEXCEPTION(e)

    def __checkIfKeysForInstanceExists(self, instance: str) -> bool:
        """
        Checks if a given instance key exists in the database list dictionary.

        Args:
        - instance (str): The instance key to be checked.

        Returns:
        - bool: True if the instance key exists.

        Raises:
        - DBLISTKEYNOTEXISTS: when the key does not exist in the db-ListJson
        """
        if instance not in self.dbListDict:
            raise DBLISTKEYNOTEXISTS(f"key {instance} not in dbList-Json")
        else:
            return True

    def __checkIfKeysForInstanceNotExists(self, instance: str) -> bool:
        """
        Checks if a given instance key does not exist in the database list dictionary.

        Args:
        - instance (str): The instance key to be checked.

        Returns:
        - bool: True if the instance key does not exist.

        Raises:
        - DBLISTKEYEXISTS: when the key does not exist in the db-ListJson
        """
        if instance in self.dbListDict:
            raise DBLISTKEYEXISTS(f"key {instance} already exists in dbList-Json")
        else:
            return True

    def __checkDbTypeForInstanceExists(self, instance: str, dbType: str ) -> bool:
        """
        Checks if a given dbType key exists for give instance in the database list dictionary.

        Args:
        - instance (str): The instance key inside the database.
        - dbType (str): The dbType to be checked

        Returns:
        - bool: True if the dbType key does exist inside the instance Json-object.

        Raises:
        - DBLISTKEYNOTEXISTS: when the key does not exist in the db-ListJson
        """
        if dbType in self.dbListDict[instance]:
            return True
        else:
            raise DBLISTKEYNOTEXISTS(f"dbType key {dbType} already exists for instance {instance}!")

    def __checkDbTypeForInstanceNotExists(self, instance: str, dbType: str ) -> bool:
        """
        Checks if a given dbType key does not exist for give instance in the database list dictionary.

        Args:
        - instance (str): The instance key inside the database.
        - dbType (str): The dbType to be checked

        Returns:
        - bool: True if the dbType key does not exist inside the instance Json-object.

        Raises:
        - DBLISTKEYEXISTS: when the key does not exist in the db-ListJson
        """
        if dbType not in self.dbListDict[instance]:
            return True
        else:
            raise DBLISTKEYEXISTS(f"dbType key {dbType} already exists for instance {instance}!")

    def readDbList(self, path: str = os.path.join(dbConfigPath, 'dblist.json')) -> dict:
        """
        Reads the database list from the specified file path and returns it as a dictionary.

        Args:
        - path (str): The file path to the database list JSON file.

        Returns:
        - dict: The database list dictionary read from the specified file path.

        Raises:
        - DBLISTUTILSEXCEPTION: If an error occurs during file reading or base database list creation.
        """
        if os.path.exists(path):
            try:
                with open(path, 'r') as fh:
                    json_data = fh.read()
            except Exception as e:
                raise DBLISTUTILSEXCEPTION(e)
            return json.loads(json_data)
        else:
            try:
                return self.__createBaseDBListJson(path)
            except:
                raise

    def getProdList(self) -> list:
        """
        Returns a list of database instance keys from the database list dictionary.

        Returns:
        - list: A list of database instance keys.
        """
        return list(self.dbListDict.keys())

    def getKeysForInstanceList(self, instance: str) -> list:
        """
        Returns a list of database entry keys for a given instance from the database list dictionary.

        Args:
        - instance (str): The database instance key.

        Returns:
        - list: A list of database entry keys for the specified instance.
        """
        if self.__checkIfKeysForInstanceExists(instance):
            return list(self.dbListDict[instance].keys())

    def getKeysForDbType(self, instance: str, dbType: str) -> list:
        if self.__checkIfKeysForInstanceExists(instance):
            if self.__checkDbTypeForInstanceExists(instance, dbType):
                return list(self.dbListDict[instance][dbType].keys())

    def getDbTypeDict(self, instance: str, dbType: str) -> dict:
        if self.__checkIfKeysForInstanceExists(instance):
            if self.__checkDbTypeForInstanceExists(instance, dbType):
                return self.dbListDict[instance][dbType]

    def addInstance(self, instance: str):
        if self.__checkIfKeysForInstanceNotExists(instance):
            self.dbListDict[instance] = {}

    def addDbTypeToInstance(self, instance: str, dbType: str):
        if self.__checkIfKeysForInstanceExists(instance):
            if self.__checkDbTypeForInstanceNotExists(instance, dbType):
                self.dbListDict[instance][dbType] = {}

    def addDbToDbType(self,instance: str, dbType: str, dbObj: dbObject ):
        if self.__checkIfKeysForInstanceExists(instance):
            if self.__checkDbTypeForInstanceNotExists(instance, dbType):
                self.dbListDict[instance][dbType] = asdict(dbObj)
