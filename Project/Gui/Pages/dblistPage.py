from nicegui import ui
from Project.Gui import themes
from Project.Utils.dbList import dbList

class dblistpage():

    def __init__(self):
        self.dblist = dbList()
        self.pickedEnv = self.dblist.getProdList()[0]
        self.pickedDbType = self.dblist.getKeysForInstanceList(self.pickedEnv)[0]
        self.data = []
        self.radioEnv = ui.radio(list(self.dblist.getProdList()), value=self.pickedEnv,
                                 on_change=lambda e: self.setPickedEnv(e)).props('inline')
        self.radioDbType = ui.radio(self.dblist.getKeysForInstanceList(self.pickedEnv), value=self.pickedDbType,
                                    on_change=lambda e: self.pickedDbType(e)).props('inline')
        self.columnDef = [
            {'headerName': 'DB-User', 'field': 'user'},
            {'headerName': 'DB-SID', 'field': 'sid'},
            {'headerName': 'picked', 'checkboxSelection': True}
        ]

        self.dbTable = ui.aggrid({
            'defaultColDef': {'flex': 1},
            'columnDefs': self.columnDef,
            'rowData': self.dblist.getDbTypeDict(self.pickedEnv, self.pickedDbType)
        })
        self.addDbName = ui.input(label='Database-Name', placeholder='enter DB-Name')
        self.addDbPw = ui.input(label='Password', placeholder='enter Password', password_toggle_button=True)
        self.addDbSid = ui.input(label='Sid', placeholder='enter Sid')
        self.addDbEnv = ui.radio(list(self.dblist.getProdList()), value=self.pickedEnv,
                                 on_change=lambda e: self.setPickedEnv(e)).props('inline')
        self.addDbType = ui.radio(self.dblist.getKeysForInstanceList(self.pickedEnv), value=self.pickedDbType,
                                    on_change=lambda e: self.pickedDbType(e)).props('inline')

    def create(self) -> None:
        #print(str(self.data))
        with themes.frame('Modify DB List'):
            with ui.element('div').classes('grid grid-cols-6 gap-3'):
                with ui.element('div').classes('col-start-2 col-span-4'):
                    self.radioEnv
                #with ui.element('div').classes('col-start-2 col-span-4'):
                #    ui.label().bind_text_from(self.radioEnv, 'value')
                with ui.element('div').classes('col-start-2 col-span-4'):
                    self.radioDbType
                #with ui.element('div').classes('col-start-2 col-span-4'):
                #    ui.label().bind_text_from(self.radioDbType, 'value')
                with ui.element('div').classes('col-start-1'):
                    self.dbTable
                with ui.element('div').classes('col-start-1'):
                    ui.button('refresh Table', on_click=self.refreshTable).props('inline')
                with ui.element('div').classes('col-start-2 col-span-4'):
                    ui.label('Add new Database Entry')
                    self.radioEnv
                    self.addDbType
                    self.makeFrameAddDb()

                with ui.element('div').classes('col-start-1'):
                    ui.button('add Entry', on_click=self.addDbEntry())
                #with ui.element('div').classes('col-start-1'):
                #    ui.button('add DB', on_click=lambda: self.)
                #with ui.aggrid({'columDefs': self.columnDef, 'rowData': [], 'rowSelection': 'multiple'}).classes(
                #    'col-start-1'
                #)
                #with ui.element('div').classes('col-start-1 col-span-6'):
                    #ui.table(columns=self.columns, pagination=10, rows=self.data, row_key='user')

    """
    @ui.refreshable
    def pickDBEnvironment(self):
        with ui.element('div').classes('col-start-2 col-span-4'):

            ui.label(f'Picked Environment')
            ui.radio(list(self.pickedProdModel.keys()),
                     # value=self.getFirstInstance(),
                     # on_change=lambda e:
                     on_change=lambda: ).props('inline')
    """

    def makeFrameAddDb(self):
        with ui.element('div').classes('grid grid-cols-4 gap-3'):
            with ui.element('div').classes('col-start-1'):
                self.addDbName.props('inline')
                self.addDbPw.props('inline')
                self.addDbSid.props('inline')

    def addDbEntry(self):
        if self.addDbName.value != None and self.addDbPw.value != None and self.addDbSid.value != None:
            self.dblist.
            print('werner')
    def refreshTable(self):
        self.dbTable.update()
    def setPickedEnv(self, env: str):
        self.pickedEnv = env

    def setPickedDbType(self, dbType: str):
        self.pickedDbType = dbType






