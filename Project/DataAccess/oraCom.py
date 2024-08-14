import oracledb
import platform
import os
from Project.Utils.settings import mcsettings

"""
TODO add Section Oracle and key oracle_home to config.ini
"""

"""
getting information for settings file
"""
settings = mcsettings()
d = None

if platform.system() == 'Windows':
    d = settings.getStringForSectionKey('Oracle', 'oracle_home')
"""
tnsnames string: 
SW02_ORI =
  (DESCRIPTION =
    (ADDRESS_LIST =
      (ADDRESS =
        (COMMUNITY = BILLA_TCP)
        (PROTOCOL = TCP)
        (HOST = autdbtest02)
        (PORT = 1920)
      )
    )
    (CONNECT_DATA =
      (SID = SW02)
    )
  )

dsn = f'{username}/{userpwd}@{host}:{port}/{service_name}'
usernmae     ... kuda_test
userpwd      ... test
host         ... HOST
port         ... PORT
service_name ... SID
f'kuda_test/test@autdbtest02:1920/SW02'
"""
def callSqlStmt(dsn: str, stmt: str) -> dict:
    with oracledb.connect(dsn) as con:
        with con.cursor() as cursor:
            try:
                cursor.execute(stmt)
            except Exception as e:
                con.rollback()
                raise Exception(e)

            columns = [col[0] for col in cursor.description]
            cursor.rowfactory = lambda *args: dict(zip(columns, args))
            return cursor.fetchall()


