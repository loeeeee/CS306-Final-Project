import json
import os
from datetime import datetime
from .data_model import DiaryEntry

DATA_DIR = "data"
ENTRIES_DIR = os.path.join(DATA_DIR, "diary_entries")
MEDIA_DIR = os.path.join(DATA_DIR, "media")
PHOTOS_DIR = os.path.join(MEDIA_DIR, "photos")

def _ensure_dirs_exist():
    """Ensures the necessary data directories exist."""
    os.makedirs(ENTRIES_DIR, exist_ok=True)
    os.makedirs(PHOTOS_DIR, exist_ok=True)

def create_entry(diary_data):
    """Creates a new diary entry."""
    _ensure_dirs_exist()
    entry = DiaryEntry(**diary_data)
    entry_file_path = os.path.join(ENTRIES_DIR, f"{entry.entry_id}.json")
    with open(entry_file_path, "w") as f:
        json.dump(entry.to_dict(), f, indent=4)
    return entry

def read_entry(entry_id):
    """Reads a diary entry by its ID."""
    entry_file_path = os.path.join(ENTRIES_DIR, f"{entry_id}.json")
    if not os.path.exists(entry_file_path):
        return None
    with open(entry_file_path, "r") as f:
        data = json.load(f)
    return DiaryEntry.from_dict(data)

def update_entry(entry_id, updated_data):
    """Updates an existing diary entry."""
    entry = read_entry(entry_id)
    if entry is None:
        return None

    for key, value in updated_data.items():
        if hasattr(entry, key):
            setattr(entry, key, value)

    entry.timestamp_modified = datetime.now().isoformat()
    entry_file_path = os.path.join(ENTRIES_DIR, f"{entry.entry_id}.json")
    with open(entry_file_path, "w") as f:
        json.dump(entry.to_dict(), f, indent=4)
    return entry

def delete_entry(entry_id):
    """Deletes a diary entry by its ID."""
    entry_file_path = os.path.join(ENTRIES_DIR, f"{entry_id}.json")
    if os.path.exists(entry_file_path):
        os.remove(entry_file_path)
        return True
    return False

def list_entries():
    """Lists all diary entries."""
    _ensure_dirs_exist()
    entries = []
    for filename in os.listdir(ENTRIES_DIR):
        if filename.endswith(".json"):
            entry_id = os.path.splitext(filename)[0]
            entry = read_entry(entry_id)
            if entry:
                entries.append(entry)
    # Sort entries by creation timestamp, newest first
    entries.sort(key=lambda x: x.timestamp_created, reverse=True)
    return entries
