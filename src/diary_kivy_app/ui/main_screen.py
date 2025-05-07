from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Header
        header = BoxLayout(size_hint_y=None, height=dp(50))
        title = Label(text='My Diary', font_size=dp(24))
        header.add_widget(title)

        # Scrollable list of entries
        scroll_view = ScrollView()
        self.entries_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        self.entries_layout.bind(minimum_height=self.entries_layout.setter('height'))
        scroll_view.add_widget(self.entries_layout)

        # Bottom buttons
        bottom_buttons = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        add_entry_btn = Button(text='Add New Entry', size_hint_x=0.7)
        settings_btn = Button(text='Settings', size_hint_x=0.3)
        
        add_entry_btn.bind(on_press=self.on_add_entry)
        settings_btn.bind(on_press=self.on_settings)
        
        bottom_buttons.add_widget(add_entry_btn)
        bottom_buttons.add_widget(settings_btn)

        # Add all widgets to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(scroll_view)
        main_layout.add_widget(bottom_buttons)

        self.add_widget(main_layout)

    def on_add_entry(self, instance):
        self.manager.current = 'editor'

    def on_settings(self, instance):
        self.manager.current = 'settings'

    def view_entry(self, entry_id):
        view_screen = self.manager.get_screen('view')
        view_screen.load_entry(entry_id)
        self.manager.current = 'view'

    def load_entries(self):
        """Load entries from storage and populate entries_layout."""
        from ..core_logic.storage_manager import list_entries
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.metrics import dp

        # Clear previous entries
        self.entries_layout.clear_widgets()
        entries = list_entries()
        if not entries:
            self.entries_layout.add_widget(Label(text="No diary entries yet.", size_hint_y=None, height=dp(40)))
            return
        for entry in entries:
            entry_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(10))
            entry_label = Label(text=entry.text_content[:40] + ("..." if len(entry.text_content) > 40 else ""), halign='left', valign='middle')
            view_btn = Button(text="View", size_hint_x=0.2)
            view_btn.bind(on_press=lambda inst, eid=entry.entry_id: self.view_entry(eid))
            entry_box.add_widget(entry_label)
            entry_box.add_widget(view_btn)
            self.entries_layout.add_widget(entry_box)

    def on_pre_enter(self, *args):
        self.load_entries() 