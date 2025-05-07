from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.metrics import dp

class EditorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Header with back button
        header = BoxLayout(size_hint_y=None, height=dp(50))
        back_btn = Button(text='Back', size_hint_x=0.2)
        title = Label(text='New Entry', font_size=dp(24))
        back_btn.bind(on_press=self.on_back)
        header.add_widget(back_btn)
        header.add_widget(title)

        # Scrollable content
        content = BoxLayout(orientation='vertical', spacing=dp(10))

        # Text input area
        self.text_input = TextInput(
            multiline=True,
            hint_text='Write your diary entry here...',
            size_hint_y=None,
            height=dp(200)
        )

        # Metadata section
        metadata = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(300))
        
        # Location
        location_btn = Button(text='Get Location')
        location_btn.bind(on_press=self.on_get_location)
        metadata.add_widget(Label(text='Location:'))
        metadata.add_widget(location_btn)

        # Weather
        weather_btn = Button(text='Get Weather')
        weather_btn.bind(on_press=self.on_get_weather)
        metadata.add_widget(Label(text='Weather:'))
        metadata.add_widget(weather_btn)

        # Environment Photo
        env_photo_btn = Button(text='Take Environment Photo')
        env_photo_btn.bind(on_press=self.on_take_env_photo)
        self.env_photo = Image(source='', size_hint_y=None, height=dp(100))
        metadata.add_widget(Label(text='Environment Photo:'))
        metadata.add_widget(BoxLayout(orientation='vertical'))
        metadata.add_widget(env_photo_btn)
        metadata.add_widget(self.env_photo)

        # Selfie
        selfie_btn = Button(text='Take Selfie')
        selfie_btn.bind(on_press=self.on_take_selfie)
        self.selfie = Image(source='', size_hint_y=None, height=dp(100))
        metadata.add_widget(Label(text='Selfie:'))
        metadata.add_widget(BoxLayout(orientation='vertical'))
        metadata.add_widget(selfie_btn)
        metadata.add_widget(self.selfie)

        # Song of the Day
        metadata.add_widget(Label(text='Song Title:'))
        self.song_title = TextInput(multiline=False)
        metadata.add_widget(self.song_title)
        
        metadata.add_widget(Label(text='Artist:'))
        self.song_artist = TextInput(multiline=False)
        metadata.add_widget(self.song_artist)

        # Bottom buttons
        bottom_buttons = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        save_btn = Button(text='Save Entry', size_hint_x=0.7)
        cancel_btn = Button(text='Cancel', size_hint_x=0.3)
        
        save_btn.bind(on_press=self.on_save)
        cancel_btn.bind(on_press=self.on_cancel)
        
        bottom_buttons.add_widget(save_btn)
        bottom_buttons.add_widget(cancel_btn)

        # Add all widgets to content
        content.add_widget(self.text_input)
        content.add_widget(metadata)

        # Add all sections to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(content)
        main_layout.add_widget(bottom_buttons)

        self.add_widget(main_layout)

    def on_back(self, instance):
        self.manager.current = 'main'

    def on_get_location(self, instance):
        # TODO: Implement location fetching
        pass

    def on_get_weather(self, instance):
        # TODO: Implement weather fetching
        pass

    def on_take_env_photo(self, instance):
        # TODO: Implement environment photo capture
        pass

    def on_take_selfie(self, instance):
        # TODO: Implement selfie capture
        pass

    def on_save(self, instance):
        # TODO: Implement save functionality
        self.manager.current = 'main'

    def on_cancel(self, instance):
        self.manager.current = 'main' 