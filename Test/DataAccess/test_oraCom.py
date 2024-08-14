import unittest
from Project.DataAccess.oraCom import callSqlStmt

class test_oraCom(unittest.TestCase):
    def setUp(self):
        self.testDns = f'kuda_test/test@autdbtest02:1920/SW02'

    def tearDown(self):
        None

    def test_callSqlStmt(self):
        sql = f"select 'werner' as Vorname, 'Beinhart' as Nachname from dual"
        retDict = callSqlStmt(self.testDns, sql)
        print(retDict)