import uuid
from datetime import datetime

class DiaryEntry:
    def __init__(self, entry_id=None, timestamp_created=None, timestamp_modified=None,
                 text_content="", location_data=None, weather_data=None,
                 environment_photo_path=None, selfie_photo_path=None, song_of_the_day=None):
        self.entry_id = entry_id if entry_id is not None else uuid.uuid4().hex
        self.timestamp_created = timestamp_created if timestamp_created is not None else datetime.now().isoformat()
        self.timestamp_modified = timestamp_modified if timestamp_modified is not None else datetime.now().isoformat()
        self.text_content = text_content
        self.location_data = location_data if location_data is not None else {}
        self.weather_data = weather_data if weather_data is not None else {}
        self.environment_photo_path = environment_photo_path
        self.selfie_photo_path = selfie_photo_path
        self.song_of_the_day = song_of_the_day if song_of_the_day is not None else {}

    def to_dict(self):
        return {
            "entry_id": self.entry_id,
            "timestamp_created": self.timestamp_created,
            "timestamp_modified": self.timestamp_modified,
            "text_content": self.text_content,
            "location_data": self.location_data,
            "weather_data": self.weather_data,
            "environment_photo_path": self.environment_photo_path,
            "selfie_photo_path": self.selfie_photo_path,
            "song_of_the_day": self.song_of_the_day,
        }

    @staticmethod
    def from_dict(data):
        return DiaryEntry(
            entry_id=data.get("entry_id"),
            timestamp_created=data.get("timestamp_created"),
            timestamp_modified=data.get("timestamp_modified"),
            text_content=data.get("text_content", ""),
            location_data=data.get("location_data", {}),
            weather_data=data.get("weather_data", {}),
            environment_photo_path=data.get("environment_photo_path"),
            selfie_photo_path=data.get("selfie_photo_path"),
            song_of_the_day=data.get("song_of_the_day", {}),
        )
