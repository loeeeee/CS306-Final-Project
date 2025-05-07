from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, RoundedRectangle

class EditorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Outer layout to center the card
        outer = AnchorLayout(anchor_x='center', anchor_y='center')

        # Card panel with background, rounded corners
        card_width = dp(600)
        card_height = dp(750)
        card = BoxLayout(orientation='vertical', size_hint=(None, None), width=card_width, height=card_height, padding=dp(24), spacing=dp(18))
        with card.canvas.before:
            Color(1, 1, 1, 1)  # White card background
            self.bg_rect = RoundedRectangle(radius=[dp(18)], pos=card.pos, size=card.size)
        card.bind(pos=lambda inst, val: setattr(self.bg_rect, 'pos', val))
        card.bind(size=lambda inst, val: setattr(self.bg_rect, 'size', val))

        # Scrollable content area
        scroll_height = card_height - dp(120)  # leave space for bottom buttons
        scroll_view = ScrollView(size_hint=(1, None), height=scroll_height)
        content = BoxLayout(orientation='vertical', spacing=dp(14), size_hint_y=None, padding=[0,0,0,0])
        content.bind(minimum_height=content.setter('height'))

        # Back button (full width, at the top)
        back_btn = Button(text='Back', size_hint_x=1, size_hint_y=None, height=dp(40))
        back_btn.bind(on_press=self.on_back)
        content.add_widget(back_btn)
        # Add a little space below the back button
        content.add_widget(Widget(size_hint_y=None, height=dp(6)))

        # Title (centered)
        title = Label(text='New Entry', font_size=dp(28), bold=True, halign='center', valign='middle', size_hint_y=None, height=dp(40))
        content.add_widget(title)

        # Text input area with label above
        content.add_widget(Label(text='Diary Entry', font_size=dp(16), bold=True, halign='left', size_hint_y=None, height=dp(24), size_hint_x=1))
        self.text_input = TextInput(
            multiline=True,
            hint_text='Write your diary entry here...',
            size_hint_y=None,
            height=dp(120),
            font_size=dp(18),
            padding=[dp(10), dp(10), dp(10), dp(10)],
            size_hint_x=1
        )
        content.add_widget(self.text_input)

        # Metadata section (labels above fields)
        metadata = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        metadata.bind(minimum_height=metadata.setter('height'))

        # Location
        metadata.add_widget(Label(text='Location', font_size=dp(15), halign='left', size_hint_y=None, height=dp(22), size_hint_x=1))
        location_btn = Button(text='Get Location', size_hint_y=None, height=dp(40), size_hint_x=1)
        location_btn.bind(on_press=self.on_get_location)
        metadata.add_widget(location_btn)

        # Weather
        metadata.add_widget(Label(text='Weather', font_size=dp(15), halign='left', size_hint_y=None, height=dp(22), size_hint_x=1))
        weather_btn = Button(text='Get Weather', size_hint_y=None, height=dp(40), size_hint_x=1)
        weather_btn.bind(on_press=self.on_get_weather)
        metadata.add_widget(weather_btn)

        # Environment Photo
        metadata.add_widget(Label(text='Environment Photo', font_size=dp(15), halign='left', size_hint_y=None, height=dp(22), size_hint_x=1))
        env_photo_btn = Button(text='Take Environment Photo', size_hint_y=None, height=dp(40), size_hint_x=1)
        env_photo_btn.bind(on_press=self.on_take_env_photo)
        metadata.add_widget(env_photo_btn)

        # Selfie
        metadata.add_widget(Label(text='Selfie', font_size=dp(15), halign='left', size_hint_y=None, height=dp(22), size_hint_x=1))
        selfie_btn = Button(text='Take Selfie', size_hint_y=None, height=dp(40), size_hint_x=1)
        selfie_btn.bind(on_press=self.on_take_selfie)
        metadata.add_widget(selfie_btn)

        # Song of the Day
        metadata.add_widget(Label(text='Song Title', font_size=dp(15), halign='left', size_hint_y=None, height=dp(22), size_hint_x=1))
        self.song_title = TextInput(multiline=False, size_hint_y=None, height=dp(36), font_size=dp(16), size_hint_x=1)
        metadata.add_widget(self.song_title)
        metadata.add_widget(Label(text='Artist', font_size=dp(15), halign='left', size_hint_y=None, height=dp(22), size_hint_x=1))
        self.song_artist = TextInput(multiline=False, size_hint_y=None, height=dp(36), font_size=dp(16), size_hint_x=1)
        metadata.add_widget(self.song_artist)

        content.add_widget(metadata)
        scroll_view.add_widget(content)
        card.add_widget(scroll_view)

        # Bottom buttons (always visible)
        bottom_buttons = BoxLayout(size_hint_y=None, height=dp(56), spacing=dp(18), padding=[0,0,0,0])
        save_btn = Button(text='Save Entry', size_hint_x=0.6, height=dp(48))
        cancel_btn = Button(text='Cancel', size_hint_x=0.4, height=dp(48))
        save_btn.bind(on_press=self.on_save)
        cancel_btn.bind(on_press=self.on_cancel)
        bottom_buttons.add_widget(save_btn)
        bottom_buttons.add_widget(cancel_btn)
        card.add_widget(bottom_buttons)

        outer.add_widget(card)
        self.add_widget(outer)

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