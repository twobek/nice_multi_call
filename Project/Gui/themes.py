from contextlib import contextmanager
from nicegui import ui
@contextmanager
def frame(navtitle: str):
    #ui.colors
    with ui.header().classes('justify-between text-white'):
        with ui.row().classes('w-full items-center'):
            with ui.button(icon='menu').classes('text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800'):
                with ui.menu().classes('py-2 text-sm text-gray-700 dark:text-gray-200'):
                    ui.link('home', '/').classes('block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white')
                    ui.link('settings', '/settings').classes('block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white')
                    ui.link('datenbank list', '/dblist').classes('block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white')
                    #ui.link('home','/')
                    #ui.link('settings','/settings')
            ui.label(navtitle)
            ui.label('cdk').classes('font-bold')

    yield