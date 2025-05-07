from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

class ViewEntryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Header with back button
        header = BoxLayout(size_hint_y=None, height=dp(50))
        back_btn = Button(text='Back', size_hint_x=0.2)
        title = Label(text='View Entry', font_size=dp(24))
        back_btn.bind(on_press=self.on_back)
        header.add_widget(back_btn)
        header.add_widget(title)

        # Scrollable content
        scroll_view = ScrollView()
        content = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # Entry content
        self.entry_text = Label(
            text='',
            size_hint_y=None,
            text_size=(self.width - dp(20), None),
            halign='left',
            valign='top'
        )
        self.entry_text.bind(texture_size=lambda instance, size: setattr(instance, 'height', size[1]))

        # Metadata section
        metadata = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(400))
        
        # Location
        metadata.add_widget(Label(text='Location:'))
        self.location_label = Label(text='Not set')
        metadata.add_widget(self.location_label)

        # Weather
        metadata.add_widget(Label(text='Weather:'))
        self.weather_label = Label(text='Not set')
        metadata.add_widget(self.weather_label)

        # Environment Photo
        metadata.add_widget(Label(text='Environment Photo:'))
        self.env_photo = Image(source='', size_hint_y=None, height=dp(150))
        metadata.add_widget(self.env_photo)

        # Selfie
        metadata.add_widget(Label(text='Selfie:'))
        self.selfie = Image(source='', size_hint_y=None, height=dp(150))
        metadata.add_widget(self.selfie)

        # Song of the Day
        metadata.add_widget(Label(text='Song:'))
        self.song_label = Label(text='Not set')
        metadata.add_widget(self.song_label)

        # Bottom buttons
        bottom_buttons = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        edit_btn = Button(text='Edit', size_hint_x=0.5)
        delete_btn = Button(text='Delete', size_hint_x=0.5)
        
        edit_btn.bind(on_press=self.on_edit)
        delete_btn.bind(on_press=self.on_delete)
        
        bottom_buttons.add_widget(edit_btn)
        bottom_buttons.add_widget(delete_btn)

        # Add all widgets to content
        content.add_widget(self.entry_text)
        content.add_widget(metadata)
        scroll_view.add_widget(content)

        # Add all sections to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(scroll_view)
        main_layout.add_widget(bottom_buttons)

        self.add_widget(main_layout)

    def on_back(self, instance):
        self.manager.current = 'main'

    def on_edit(self, instance):
        # TODO: Implement edit functionality
        self.manager.current = 'editor'

    def on_delete(self, instance):
        # TODO: Implement delete functionality with confirmation
        self.manager.current = 'main'

    def load_entry(self, entry_id):
        # TODO: Load entry data and populate UI
        pass 