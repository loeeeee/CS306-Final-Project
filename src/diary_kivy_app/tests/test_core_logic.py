import unittest
import os
import json
from datetime import datetime
from diary_kivy_app.core_logic.diary_entry import DiaryEntry
from diary_kivy_app.core_logic.storage import Storage, StorageError, EntryNotFoundError, StorageCorruptionError

class TestDiaryEntry(unittest.TestCase):
    def setUp(self):
        self.entry = DiaryEntry(
            text_content="Test entry",
            location_data={"latitude": 40.7128, "longitude": -74.0060},
            weather_data={"temperature": 25, "humidity": 60, "description": "Sunny"},
            environment_photo_path="test_env.jpg",
            selfie_photo_path="test_selfie.jpg",
            song_of_the_day={"title": "Test Song", "artist": "Test Artist"}
        )

    def test_entry_creation(self):
        self.assertEqual(self.entry.text_content, "Test entry")
        self.assertEqual(self.entry.location_data["latitude"], 40.7128)
        self.assertEqual(self.entry.weather_data["temperature"], 25)
        self.assertEqual(self.entry.song_of_the_day["title"], "Test Song")

    def test_entry_modification(self):
        self.entry.text_content = "Modified entry"
        self.assertEqual(self.entry.text_content, "Modified entry")
        self.assertIsNotNone(self.entry.timestamp_modified)

    def test_entry_serialization(self):
        # Test to_dict
        entry_dict = self.entry.to_dict()
        self.assertEqual(entry_dict['text_content'], "Test entry")
        self.assertEqual(entry_dict['location_data']['latitude'], 40.7128)
        
        # Test from_dict
        new_entry = DiaryEntry.from_dict(entry_dict)
        self.assertEqual(new_entry.text_content, self.entry.text_content)
        self.assertEqual(new_entry.location_data, self.entry.location_data)
        self.assertEqual(new_entry.entry_id, self.entry.entry_id)

    def test_entry_update_method(self):
        original_modified = self.entry.timestamp_modified
        self.entry.update(
            text_content="Updated content",
            location_data={"latitude": 41.0, "longitude": -75.0}
        )
        self.assertEqual(self.entry.text_content, "Updated content")
        self.assertEqual(self.entry.location_data["latitude"], 41.0)
        self.assertGreater(self.entry.timestamp_modified, original_modified)

    def test_entry_empty_metadata(self):
        entry = DiaryEntry("Simple entry")
        self.assertEqual(entry.location_data, {})
        self.assertEqual(entry.weather_data, {})
        self.assertEqual(entry.song_of_the_day, {})
        self.assertIsNone(entry.environment_photo_path)
        self.assertIsNone(entry.selfie_photo_path)

class TestStorage(unittest.TestCase):
    def setUp(self):
        # Use a temporary directory for testing
        self.test_dir = os.path.join(os.path.dirname(__file__), 'test_data')
        os.makedirs(self.test_dir, exist_ok=True)
        self.storage = Storage(data_dir=self.test_dir)
        self.test_entry = DiaryEntry(
            text_content="Test entry",
            location_data={"latitude": 40.7128, "longitude": -74.0060},
            weather_data={"temperature": 25, "humidity": 60, "description": "Sunny"},
            environment_photo_path="test_env.jpg",
            selfie_photo_path="test_selfie.jpg",
            song_of_the_day={"title": "Test Song", "artist": "Test Artist"}
        )

    def tearDown(self):
        # Clean up test data
        import shutil
        shutil.rmtree(self.test_dir)

    def test_save_and_load_entry(self):
        # Save entry
        entry_id = self.storage.save_entry(self.test_entry)
        self.assertIsNotNone(entry_id)

        # Load entry
        loaded_entry = self.storage.load_entry(entry_id)
        self.assertEqual(loaded_entry.text_content, self.test_entry.text_content)
        self.assertEqual(loaded_entry.location_data, self.test_entry.location_data)

    def test_delete_entry(self):
        entry_id = self.storage.save_entry(self.test_entry)
        self.storage.delete_entry(entry_id)
        with self.assertRaises(EntryNotFoundError):
            self.storage.load_entry(entry_id)

    def test_list_entries(self):
        # Create multiple entries
        entry1 = DiaryEntry("Entry 1")
        entry2 = DiaryEntry("Entry 2")
        entry3 = DiaryEntry("Entry 3")
        
        id1 = self.storage.save_entry(entry1)
        id2 = self.storage.save_entry(entry2)
        id3 = self.storage.save_entry(entry3)
        
        entries = self.storage.list_entries()
        self.assertEqual(len(entries), 3)
        self.assertIn(id1, entries)
        self.assertIn(id2, entries)
        self.assertIn(id3, entries)

    def test_media_file_handling(self):
        # Test media path creation
        media_path = self.storage.get_media_path("test.jpg")
        self.assertTrue(str(media_path).endswith("test.jpg"))
        
        # Test media file cleanup on entry deletion
        entry_id = self.storage.save_entry(self.test_entry)
        self.storage.delete_entry(entry_id)
        # Verify media files are deleted (or at least attempted to be deleted)
        self.assertFalse(os.path.exists(self.storage.get_media_path("test_env.jpg")))
        self.assertFalse(os.path.exists(self.storage.get_media_path("test_selfie.jpg")))

    def test_corrupted_entries_file(self):
        # Create a corrupted entries file
        with open(self.storage.entries_file, 'w') as f:
            f.write("invalid json content")
        
        # Should raise StorageCorruptionError
        with self.assertRaises(StorageCorruptionError):
            self.storage._load_entries()

    def test_nonexistent_entry(self):
        with self.assertRaises(EntryNotFoundError):
            self.storage.load_entry("nonexistent_id")

if __name__ == '__main__':
    unittest.main() 