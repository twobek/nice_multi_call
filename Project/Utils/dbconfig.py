import configparser
import os.path

dbConfigPath = os.path.dirname(__file__)
class DBCONFIGEXCEPTION(Exception):
    pass

class dbconfig():
    def __init__(self, configPath: str = os.path.join(dbConfigPath,'dbconfig.ini')) -> None:
        self.readConfig(configPath)


    def readConfig(self, configPath: str = os.path.join(dbConfigPath,'dbconfig.ini')) -> None:
        if os.path.exists(configPath):
            self.configpath = configPath
        else:
            raise DBCONFIGEXCEPTION(f'{configPath} not a valid path')
        self.config = configparser.ConfigParser()
        self.config.read(self.configpath)

    def addDbConfig(self, sectionName: str, user: str, pw: str, sid: str,
                    configPath: str = os.path.join(dbConfigPath,'dbconfig.ini'),
                    preSelected: bool = False) -> None:
        if configPath != self.configpath:
            self.readConfig(configPath)

        self.config.add_section(sectionName)
        self.config.set(sectionName, 'user', user)
        self.config.set(sectionName, 'pw', pw)
        self.config.set(sectionName, 'sid', sid)
        self.config.set(sectionName, 'preSelected', str(preSelected))


        with open(configPath, 'a') as fh:
            self.config.write(fh)

    def getSectionsList(self) -> list:
        retList = list()
        for section in self.config.sections():
            retList.append(section)
        return retList

    def getSectionData(self, type: str = None) -> list:
        retList = list()
        for section in self.config.sections():
            if type:
                pType = section.split('_', 1)
                if len(pType) == 2:
                    if type == pType[1]:
                        retList.append(dict(self.config.items(section)))
            else:
                retList.append(dict(self.config.items(section)))

        return retList