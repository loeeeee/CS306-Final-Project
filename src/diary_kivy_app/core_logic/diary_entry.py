from datetime import datetime
import uuid

class DiaryEntry:
    def __init__(self, text_content, location_data=None, weather_data=None,
                 environment_photo_path=None, selfie_photo_path=None,
                 song_of_the_day=None):
        self.entry_id = str(uuid.uuid4())
        self.timestamp_created = datetime.now()
        self.timestamp_modified = self.timestamp_created
        self.text_content = text_content
        self.location_data = location_data or {}
        self.weather_data = weather_data or {}
        self.environment_photo_path = environment_photo_path
        self.selfie_photo_path = selfie_photo_path
        self.song_of_the_day = song_of_the_day or {}

    def update(self, **kwargs):
        """Update entry fields and set modification timestamp."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.timestamp_modified = datetime.now()

    def to_dict(self):
        """Convert entry to dictionary format for storage."""
        return {
            'entry_id': self.entry_id,
            'timestamp_created': self.timestamp_created.isoformat(),
            'timestamp_modified': self.timestamp_modified.isoformat(),
            'text_content': self.text_content,
            'location_data': self.location_data,
            'weather_data': self.weather_data,
            'environment_photo_path': self.environment_photo_path,
            'selfie_photo_path': self.selfie_photo_path,
            'song_of_the_day': self.song_of_the_day
        }

    @classmethod
    def from_dict(cls, data):
        """Create entry from dictionary format."""
        entry = cls(
            text_content=data['text_content'],
            location_data=data.get('location_data'),
            weather_data=data.get('weather_data'),
            environment_photo_path=data.get('environment_photo_path'),
            selfie_photo_path=data.get('selfie_photo_path'),
            song_of_the_day=data.get('song_of_the_day')
        )
        entry.entry_id = data['entry_id']
        entry.timestamp_created = datetime.fromisoformat(data['timestamp_created'])
        entry.timestamp_modified = datetime.fromisoformat(data['timestamp_modified'])
        return entry 