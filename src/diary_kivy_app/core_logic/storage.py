import json
import os
import shutil
from pathlib import Path
from .diary_entry import DiaryEntry

class StorageError(Exception):
    """Base exception for storage-related errors."""
    pass

class EntryNotFoundError(StorageError):
    """Raised when a requested entry is not found."""
    pass

class StorageCorruptionError(StorageError):
    """Raised when storage data is corrupted."""
    pass

class Storage:
    def __init__(self, data_dir=None):
        """Initialize storage with optional custom data directory."""
        try:
            if data_dir is None:
                data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
            self.data_dir = Path(data_dir)
            self.entries_file = self.data_dir / 'entries.json'
            self.media_dir = self.data_dir / 'media'
            
            # Create necessary directories
            self.data_dir.mkdir(parents=True, exist_ok=True)
            self.media_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize entries file if it doesn't exist
            if not self.entries_file.exists():
                self._save_entries({})
        except (OSError, IOError) as e:
            raise StorageError(f"Failed to initialize storage: {str(e)}")

    def _load_entries(self):
        """Load all entries from storage."""
        try:
            with open(self.entries_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            raise StorageCorruptionError(f"Entries file is corrupted: {str(e)}")
        except (OSError, IOError) as e:
            raise StorageError(f"Failed to read entries file: {str(e)}")

    def _save_entries(self, entries):
        """Save all entries to storage."""
        try:
            # Create a backup of the current entries file if it exists
            if self.entries_file.exists():
                backup_file = self.entries_file.with_suffix('.json.bak')
                shutil.copy2(self.entries_file, backup_file)
            
            # Write new entries
            with open(self.entries_file, 'w') as f:
                json.dump(entries, f, indent=2)
            
            # Remove backup if save was successful
            if self.entries_file.exists():
                backup_file = self.entries_file.with_suffix('.json.bak')
                if backup_file.exists():
                    backup_file.unlink()
        except (OSError, IOError) as e:
            # Restore from backup if available
            backup_file = self.entries_file.with_suffix('.json.bak')
            if backup_file.exists():
                shutil.copy2(backup_file, self.entries_file)
            raise StorageError(f"Failed to save entries: {str(e)}")

    def save_entry(self, entry):
        """Save a diary entry and return its ID."""
        try:
            entries = self._load_entries()
            entries[entry.entry_id] = entry.to_dict()
            self._save_entries(entries)
            return entry.entry_id
        except Exception as e:
            raise StorageError(f"Failed to save entry: {str(e)}")

    def load_entry(self, entry_id):
        """Load a diary entry by ID."""
        entries = self._load_entries()
        if entry_id not in entries:
            raise EntryNotFoundError(f"Entry {entry_id} not found")
        try:
            return DiaryEntry.from_dict(entries[entry_id])
        except Exception as e:
            raise StorageError(f"Failed to load entry data: {str(e)}")

    def delete_entry(self, entry_id):
        """Delete a diary entry by ID."""
        entries = self._load_entries()
        if entry_id not in entries:
            raise EntryNotFoundError(f"Entry {entry_id} not found")
        
        try:
            # Delete associated media files
            entry = entries[entry_id]
            for photo_path in [entry.get('environment_photo_path'), entry.get('selfie_photo_path')]:
                if photo_path:
                    try:
                        os.remove(self.media_dir / photo_path)
                    except OSError:
                        pass  # Ignore if file doesn't exist
            
            del entries[entry_id]
            self._save_entries(entries)
        except Exception as e:
            raise StorageError(f"Failed to delete entry: {str(e)}")

    def list_entries(self):
        """List all entry IDs."""
        try:
            entries = self._load_entries()
            return list(entries.keys())
        except StorageCorruptionError:
            raise
        except Exception as e:
            raise StorageError(f"Failed to list entries: {str(e)}")

    def get_media_path(self, filename):
        """Get full path for a media file."""
        try:
            return self.media_dir / filename
        except Exception as e:
            raise StorageError(f"Failed to get media path: {str(e)}") 