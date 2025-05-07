from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Header with back button
        header = BoxLayout(size_hint_y=None, height=dp(50))
        back_btn = Button(text='Back', size_hint_x=0.2)
        title = Label(text='Settings', font_size=dp(24))
        back_btn.bind(on_press=self.on_back)
        header.add_widget(back_btn)
        header.add_widget(title)

        # Content
        content = BoxLayout(orientation='vertical', spacing=dp(20))

        # Export section
        export_label = Label(
            text='Export your diary entries to a file',
            size_hint_y=None,
            height=dp(30)
        )
        export_btn = Button(
            text='Export Diary',
            size_hint_y=None,
            height=dp(50)
        )
        export_btn.bind(on_press=self.on_export)

        # Add widgets to content
        content.add_widget(export_label)
        content.add_widget(export_btn)

        # Add all sections to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(content)

        self.add_widget(main_layout)

    def on_back(self, instance):
        self.manager.current = 'main'

    def on_export(self, instance):
        # TODO: Implement export functionality
        pass 