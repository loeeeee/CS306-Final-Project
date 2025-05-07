from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle

class ViewEntryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_entry_id = None
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

        # Header with back button
        header = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        back_btn = Button(text='Back', size_hint_x=0.2, height=dp(40))
        title = Label(text='View Entry', font_size=dp(28), bold=True, halign='center', valign='middle')
        back_btn.bind(on_press=self.on_back)
        header.add_widget(back_btn)
        header.add_widget(title)
        card.add_widget(header)

        # Scrollable content area
        scroll_height = card_height - dp(160)  # leave space for bottom buttons and header
        scroll_view = ScrollView(size_hint=(1, None), height=scroll_height)
        content = BoxLayout(orientation='vertical', spacing=dp(18), size_hint_y=None, padding=[0,0,0,0])
        content.bind(minimum_height=content.setter('height'))

        # Main entry text
        content.add_widget(Label(text='Diary Entry', font_size=dp(18), bold=True, halign='left', size_hint_y=None, height=dp(28)))
        self.entry_text = Label(
            text='',
            font_size=dp(16),
            size_hint_y=None,
            text_size=(card_width - dp(60), None),
            halign='left',
            valign='top',
            color=(0,0,0,1)
        )
        self.entry_text.bind(texture_size=lambda instance, size: setattr(instance, 'height', size[1]))
        content.add_widget(self.entry_text)
        content.add_widget(Widget(size_hint_y=None, height=dp(8)))

        # Metadata section
        meta_title = Label(text='Metadata', font_size=dp(18), bold=True, halign='left', size_hint_y=None, height=dp(28))
        content.add_widget(meta_title)
        metadata = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(200))
        # Location
        metadata.add_widget(Label(text='Location:', font_size=dp(15), halign='left', size_hint_y=None, height=dp(24)))
        self.location_label = Label(text='Not set', font_size=dp(15), size_hint_y=None, height=dp(24))
        metadata.add_widget(self.location_label)
        # Weather
        metadata.add_widget(Label(text='Weather:', font_size=dp(15), halign='left', size_hint_y=None, height=dp(24)))
        self.weather_label = Label(text='Not set', font_size=dp(15), size_hint_y=None, height=dp(24))
        metadata.add_widget(self.weather_label)
        # Song of the Day
        metadata.add_widget(Label(text='Song:', font_size=dp(15), halign='left', size_hint_y=None, height=dp(24)))
        self.song_label = Label(text='Not set', font_size=dp(15), size_hint_y=None, height=dp(24))
        metadata.add_widget(self.song_label)
        content.add_widget(metadata)
        content.add_widget(Widget(size_hint_y=None, height=dp(8)))

        # Photos section
        photos_title = Label(text='Photos', font_size=dp(18), bold=True, halign='left', size_hint_y=None, height=dp(28))
        content.add_widget(photos_title)
        photos = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(170))
        # Environment Photo
        photos.add_widget(Label(text='Environment Photo:', font_size=dp(15), halign='left', size_hint_y=None, height=dp(24)))
        self.env_photo = Image(source='', size_hint_y=None, height=dp(150))
        photos.add_widget(self.env_photo)
        # Selfie
        photos.add_widget(Label(text='Selfie:', font_size=dp(15), halign='left', size_hint_y=None, height=dp(24)))
        self.selfie = Image(source='', size_hint_y=None, height=dp(150))
        photos.add_widget(self.selfie)
        content.add_widget(photos)

        scroll_view.add_widget(content)
        card.add_widget(scroll_view)

        # Bottom buttons (always visible)
        bottom_buttons = BoxLayout(size_hint_y=None, height=dp(56), spacing=dp(18), padding=[0,0,0,0])
        edit_btn = Button(text='Edit', size_hint_x=0.5, height=dp(48))
        delete_btn = Button(text='Delete', size_hint_x=0.5, height=dp(48))
        edit_btn.bind(on_press=self.on_edit)
        delete_btn.bind(on_press=self.on_delete)
        bottom_buttons.add_widget(edit_btn)
        bottom_buttons.add_widget(delete_btn)
        card.add_widget(bottom_buttons)

        outer.add_widget(card)
        self.add_widget(outer)

    def on_back(self, instance):
        self.manager.current = 'main'

    def on_edit(self, instance):
        # Load the entry into the editor screen for editing
        from ..core_logic.storage_manager import read_entry
        entry = read_entry(self.current_entry_id)
        if not entry:
            return
        editor_screen = self.manager.get_screen('editor')
        # Set fields in the editor screen
        editor_screen.text_input.text = entry.text_content
        editor_screen.env_photo_path = entry.environment_photo_path
        editor_screen.selfie_photo_path = entry.selfie_photo_path
        editor_screen.song_title.text = entry.song_of_the_day.get('title', '') if entry.song_of_the_day else ''
        editor_screen.song_artist.text = entry.song_of_the_day.get('artist', '') if entry.song_of_the_day else ''
        # Set location and weather labels (for display only)
        if entry.location_data and entry.location_data.get('latitude') is not None:
            editor_screen.location_label.text = f"Lat: {entry.location_data.get('latitude')}, Lon: {entry.location_data.get('longitude')}"
        else:
            editor_screen.location_label.text = "Not set"
        if entry.weather_data and entry.weather_data.get('temperature') is not None:
            editor_screen.weather_label.text = f"{entry.weather_data.get('temperature')}°C, {entry.weather_data.get('humidity')}% humidity"
        else:
            editor_screen.weather_label.text = "Not set"
        if entry.environment_photo_path:
            editor_screen.env_photo_label.text = "Photo taken"
        else:
            editor_screen.env_photo_label.text = "Not set"
        if entry.selfie_photo_path:
            editor_screen.selfie_label.text = "Selfie taken"
        else:
            editor_screen.selfie_label.text = "Not set"
        # Store the entry being edited
        editor_screen.current_entry = entry
        self.manager.current = 'editor'

    def on_delete(self, instance):
        # Delete the entry and return to main screen
        from ..core_logic.storage_manager import delete_entry
        delete_entry(self.current_entry_id)
        main_screen = self.manager.get_screen('main')
        main_screen.load_entries()
        self.manager.current = 'main'

    def load_entry(self, entry_id):
        from ..core_logic.storage_manager import read_entry
        self.current_entry_id = entry_id
        entry = read_entry(entry_id)
        if not entry:
            self.entry_text.text = "Entry not found."
            self.location_label.text = "Not set"
            self.weather_label.text = "Not set"
            self.env_photo.source = ''
            self.selfie.source = ''
            self.song_label.text = "Not set"
            return
        self.entry_text.text = entry.text_content
        # Location
        loc = entry.location_data
        if loc and loc.get('latitude') is not None:
            self.location_label.text = f"Lat: {loc.get('latitude')}, Lon: {loc.get('longitude')}"
        else:
            self.location_label.text = "Not set"
        # Weather
        weather = entry.weather_data
        if weather and weather.get('temperature') is not None:
            self.weather_label.text = f"{weather.get('temperature')}°C, {weather.get('humidity')}% humidity"
        else:
            self.weather_label.text = "Not set"
        # Environment Photo
        self.env_photo.source = entry.environment_photo_path or ''
        # Selfie
        self.selfie.source = entry.selfie_photo_path or ''
        # Song
        song = entry.song_of_the_day
        if song and (song.get('title') or song.get('artist')):
            self.song_label.text = f"{song.get('title', '')} - {song.get('artist', '')}"
        else:
            self.song_label.text = "Not set" 