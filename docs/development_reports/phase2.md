# Phase 2 Development Report: Core Functionality - Data Management

## Implementation Details

This report details the implementation of Phase 2 of the multi-platform diary app development, focusing on data management.

### Data Modeling

A Python class `DiaryEntry` was created in `src/diary_kivy_app/core_logic/data_model.py` to model individual diary entries. The class includes attributes for:

*   `entry_id`: A unique identifier generated using `uuid.uuid4().hex`.
*   `timestamp_created`: Records the creation time in ISO format.
*   `timestamp_modified`: Records the last modification time in ISO format.
*   `text_content`: Stores the main diary text.
*   `location_data`: A dictionary to hold latitude, longitude, and altitude.
*   `weather_data`: A dictionary for temperature, humidity, and description.
*   `environment_photo_path`: Stores the relative path to the environment photo.
*   `selfie_photo_path`: Stores the relative path to the selfie photo.
*   `song_of_the_day`: A dictionary for the song title and artist.

The `DiaryEntry` class includes `to_dict()` and `from_dict()` methods to facilitate serialization and deserialization to and from dictionary representations, which is essential for JSON storage.

### Storage Mechanism

JSON files were chosen as the local storage solution for diary entries. Each diary entry is stored as a separate JSON file.

The storage logic is implemented in `src/diary_kivy_app/core_logic/storage_manager.py`. The following directory structure is used at the project root:

*   `data/`: The main directory for all application data.
*   `data/diary_entries/`: Stores individual diary entry JSON files, named using the `entry_id` (e.g., `<entry_id>.json`).
*   `data/media/photos/`: Designated for storing associated photo files.

The `storage_manager.py` module provides the following CRUD operations:

*   `create_entry(diary_data)`: Creates a new `DiaryEntry` object, generates a unique ID, and saves it as a JSON file.
*   `read_entry(entry_id)`: Reads and deserializes a diary entry from its JSON file based on the provided ID.
*   `update_entry(entry_id, updated_data)`: Reads an existing entry, updates its attributes, and saves the modified entry back to its JSON file. The `timestamp_modified` is updated automatically.
*   `delete_entry(entry_id)`: Deletes the JSON file corresponding to the given `entry_id`. (Note: Associated media files are not deleted in this phase).
*   `list_entries()`: Scans the `data/diary_entries/` directory, reads all JSON files, and returns a list of `DiaryEntry` objects, sorted by creation timestamp in descending order.

A helper function `_ensure_dirs_exist()` was added to ensure the necessary data directories (`data/diary_entries/` and `data/media/photos/`) are created if they do not exist.

### Media File Management Strategy

While the actual photo capture and saving will be implemented in Phase 4, the strategy for managing media files was defined in this phase. Photos will be stored in the `data/media/photos/` directory. Filenames will be structured to link them to their respective diary entries using the `entry_id` (e.g., `<entry_id>_environment.jpg`, `<entry_id>_selfie.jpg`). The relative paths to these files are stored in the `environment_photo_path` and `selfie_photo_path` attributes of the `DiaryEntry` class.

## Files Created/Modified

*   `src/diary_kivy_app/core_logic/data_model.py`: New file containing the `DiaryEntry` class.
*   `src/diary_kivy_app/core_logic/storage_manager.py`: New file containing the storage logic and CRUD operations.
*   `docs/development_reports/phase2.md`: This report file.

## Next Steps

Phase 3 will focus on the User Interface (UI) development using Kivy, as outlined in `docs/phases.md`. This will involve creating the necessary Kivy language (`.kv`) files and Python classes to display and interact with the diary entries managed in Phase 2.
