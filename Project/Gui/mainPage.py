from Project.Gui import themes
from nicegui import ui

from Project.Gui.Pages.dblistPage import dblistpage

def create() -> None:
    @ui.page('/')
    def homePage():
        with themes.frame('multi_call'):
            with ui.element('div').classes('grid grid-cols-5 gap-3'):
                with ui.element('div').classes('col-span-1'):
                    ui.label('hier könnte ihre Werbung stehn')
                with ui.element('div').classes('col-span-4'):
                    with ui.element('div').classes('row-span-2'):
                        ui.textarea(label='Sql Statement', on_change=lambda e: result.set_text('you typed:\n' + e.value)).props('clearable')
                    with ui.element('div').classes('row-span-2'):
                        result = ui.label()

    @ui.page('/settings')
    def settingsPage():
        with themes.frame('Settings'):
            None

    @ui.page('/dblist')
    def dbListPage():
        dblistpage().create()




