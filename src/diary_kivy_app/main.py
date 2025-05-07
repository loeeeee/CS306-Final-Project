from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window

from .ui.main_screen import MainScreen
from .ui.editor_screen import EditorScreen
from .ui.view_entry_screen import ViewEntryScreen
from .ui.settings_screen import SettingsScreen

class DiaryApp(App):
    def build(self):
        Window.size = (900, 900)
        # Load KV files
        Builder.load_file('src/diary_kivy_app/ui/main_screen.kv')
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(EditorScreen(name='editor'))
        sm.add_widget(ViewEntryScreen(name='view'))
        sm.add_widget(SettingsScreen(name='settings'))
        
        return sm

if __name__ == '__main__':
    DiaryApp().run()
