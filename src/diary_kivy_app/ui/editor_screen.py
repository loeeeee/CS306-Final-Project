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
from kivy.clock import Clock
from ..core_logic.metadata_collector import MetadataCollector
import os
from datetime import datetime
import platform
from ..core_logic.data_model import DiaryEntry
from ..core_logic.diary_exporter import DiaryExporter
import uuid

class EditorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.metadata_collector = MetadataCollector()
        self.current_entry = None
        self.env_photo_path = None
        self.selfie_photo_path = None
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
        self.location_label = Label(text='Not set', size_hint_y=None, height=dp(20), size_hint_x=1)
        metadata.add_widget(self.location_label)
        location_btn = Button(text='Get Location', size_hint_y=None, height=dp(40), size_hint_x=1)
        location_btn.bind(on_press=self.on_get_location)
        metadata.add_widget(location_btn)

        # Weather
        metadata.add_widget(Label(text='Weather', font_size=dp(15), halign='left', size_hint_y=None, height=dp(22), size_hint_x=1))
        self.weather_label = Label(text='Not set', size_hint_y=None, height=dp(20), size_hint_x=1)
        metadata.add_widget(self.weather_label)
        weather_btn = Button(text='Get Weather', size_hint_y=None, height=dp(40), size_hint_x=1)
        weather_btn.bind(on_press=self.on_get_weather)
        metadata.add_widget(weather_btn)

        # Environment Photo
        metadata.add_widget(Label(text='Environment Photo', font_size=dp(15), halign='left', size_hint_y=None, height=dp(22), size_hint_x=1))
        self.env_photo_label = Label(text='Not set', size_hint_y=None, height=dp(20), size_hint_x=1)
        metadata.add_widget(self.env_photo_label)
        env_photo_btn = Button(text='Take Environment Photo', size_hint_y=None, height=dp(40), size_hint_x=1)
        env_photo_btn.bind(on_press=self.on_take_env_photo)
        metadata.add_widget(env_photo_btn)

        # Selfie
        metadata.add_widget(Label(text='Selfie', font_size=dp(15), halign='left', size_hint_y=None, height=dp(22), size_hint_x=1))
        self.selfie_label = Label(text='Not set', size_hint_y=None, height=dp(20), size_hint_x=1)
        metadata.add_widget(self.selfie_label)
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
        """Handle location button press."""
        if self.metadata_collector.start_location_tracking():
            self.location_label.text = "Getting location..."
            # Check for location updates every second
            Clock.schedule_interval(self._check_location, 1)
        else:
            self.location_label.text = "Location service not available on this platform"

    def _check_location(self, dt):
        """Check if location has been updated."""
        location = self.metadata_collector.get_current_location()
        if location.get('error'):
            self.location_label.text = location['error']
            return False
        if location.get('latitude') is not None:
            self.location_label.text = f"Lat: {location['latitude']:.4f}, Lon: {location['longitude']:.4f}"
            self.metadata_collector.stop_location_tracking()
            return False  # Stop checking
        return True  # Keep checking

    def on_get_weather(self, instance):
        """Handle weather button press."""
        weather_data = self.metadata_collector.get_weather_data()
        if weather_data['temperature'] is not None:
            self.weather_label.text = f"{weather_data['temperature']}°C, {weather_data['humidity']}% humidity"
        else:
            self.weather_label.text = f"{weather_data['description']} ({weather_data['platform']})"

    def on_take_env_photo(self, instance):
        """Handle environment photo button press."""
        if not self.metadata_collector.take_photo(self._on_env_photo_taken):
            self.env_photo_label.text = "Camera not available on this platform"

    def _on_env_photo_taken(self, path):
        """Handle environment photo capture completion."""
        if isinstance(path, list):  # File chooser returns a list
            path = path[0]
        if path:
            self.env_photo_path = path
            self.env_photo_label.text = "Photo taken"
        else:
            self.env_photo_label.text = "Failed to take photo"

    def on_take_selfie(self, instance):
        """Handle selfie button press."""
        if not self.metadata_collector.take_photo(self._on_selfie_taken):
            self.selfie_label.text = "Camera not available on this platform"

    def _on_selfie_taken(self, path):
        """Handle selfie capture completion."""
        if isinstance(path, list):  # File chooser returns a list
            path = path[0]
        if path:
            self.selfie_photo_path = path
            self.selfie_label.text = "Selfie taken"
        else:
            self.selfie_label.text = "Failed to take selfie"

    def on_save(self, instance):
        """Handle save button press."""
        # Collect entry data from UI
        text_content = self.text_input.text.strip()
        if not text_content:
            print("Diary entry text is required.")
            return

        # Compose metadata
        location = self.metadata_collector.get_current_location()
        weather = self.metadata_collector.get_weather_data()
        song = {
            "title": self.song_title.text.strip(),
            "artist": self.song_artist.text.strip()
        }

        # If editing, use the original entry_id and timestamp_created
        if self.current_entry:
            entry_id = self.current_entry.entry_id
            timestamp_created = self.current_entry.timestamp_created
        else:
            entry_id = uuid.uuid4().hex
            timestamp_created = datetime.now().isoformat()
        now = datetime.now().isoformat()
        entry = DiaryEntry(
            entry_id=entry_id,
            timestamp_created=timestamp_created,
            timestamp_modified=now,
            text_content=text_content,
            location_data=location,
            weather_data=weather,
            environment_photo_path=self.env_photo_path,
            selfie_photo_path=self.selfie_photo_path,
            song_of_the_day=song
        )

        # Save entry using DiaryExporter
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../../data')
        entries_dir = os.path.join(data_dir, 'diary_entries')
        media_dir = os.path.join(data_dir, 'media')
        exporter = DiaryExporter(entries_dir, media_dir)
        success = exporter.save_entry(entry.to_dict())
        if success:
            print("Entry saved successfully.")
            # Refresh main screen entries before switching
            main_screen = self.manager.get_screen('main')
            main_screen.load_entries()
            self.manager.current = 'main'
            self.current_entry = None  # Reset after save
        else:
            print("Failed to save entry.")

    def on_cancel(self, instance):
        """Handle cancel button press."""
        self.manager.current = 'main'

    def on_leave(self):
        """Clean up when leaving the screen."""
        self.metadata_collector.stop_location_tracking() 