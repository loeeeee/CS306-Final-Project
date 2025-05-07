# Phases

## Detailed Development Plan

This plan outlines the steps for developing the multi-platform diary app using Python and Kivy, as described in `docs/goals.md`.

### Phase 1: Project Setup & Foundation
*   **Environment Configuration:**
    *   Verify Python 3.12 installation.
    *   Install Kivy framework and its dependencies.
    *   Identify and install necessary libraries for:
        *   Location services (e.g., `plyer`).
        *   Camera access (e.g., `plyer`).
        *   Sensor access (e.g., `plyer` for available device sensors like accelerometer, gyroscope; specific libraries if external sensors are implied).
        *   File system operations.
*   **Project Structure Refinement:**
    *   Current structure includes `src/app_with_story/`. Recommend creating a dedicated directory for the diary app, for example, `src/diary_kivy_app/`.
    *   Establish subdirectories within `src/diary_kivy_app/` for modules like `ui`, `core_logic`, `utils`, `assets`, `tests`.
*   **Version Control:**
    *   Ensure `.gitignore` is comprehensive for Python and Kivy development (e.g., `__pycache__`, `*.pyc`, build artifacts).
*   **Basic Application Shell:**
    *   Create a minimal Kivy application with a main window.
    *   Implement basic navigation structure if multiple screens are anticipated early on.

### Phase 2: Core Functionality - Data Management
*   **Data Modeling:**
    *   Define a Python class or data structure for a `DiaryEntry`.
    *   Attributes: `entry_id`, `timestamp_created`, `timestamp_modified`, `text_content`, `location_data` (latitude, longitude, altitude), `weather_data` (temperature, humidity, description - from sensors), `environment_photo_path`, `selfie_photo_path`, `song_of_the_day` (title, artist).
*   **Storage Mechanism:**
    *   Choose and implement a local storage solution. Options:
        *   SQLite database: Good for structured data and querying.
        *   JSON files: Simpler for smaller datasets, one file per entry or a main index.
    *   Implement CRUD operations (Create, Read, Update, Delete) for diary entries.
*   **Media File Management:**
    *   Define a strategy for storing photos (e.g., in a dedicated subdirectory, filenames linked to entry IDs).

### Phase 3: User Interface (UI) Development (Kivy)
*   **Main Screen (`MainScreen.kv` & `main_screen.py`):**
    *   Display a scrollable list of existing diary entries (e.g., showing title/date/thumbnail).
    *   "Add New Entry" button.
    *   Navigation to Settings/Export.
*   **Entry Creation/Editing Screen (`EditorScreen.kv` & `editor_screen.py`):**
    *   Large text input area for the diary note.
    *   Display fields/icons for metadata:
        *   Location (button to fetch/display).
        *   Weather (button to fetch/display).
        *   Environment Photo (button to capture/select, placeholder/thumbnail display).
        *   Selfie (button to capture/select, placeholder/thumbnail display).
        *   Song of the Day (text input fields for title/artist).
    *   "Save" and "Cancel/Back" buttons.
*   **Entry Viewing Screen (`ViewEntryScreen.kv` & `view_entry_screen.py`):**
    *   Display full text content of the selected entry.
    *   Display all associated metadata:
        *   Formatted location.
        *   Formatted weather.
        *   Display environment photo and selfie.
        *   Display song information.
    *   "Edit" and "Delete" buttons (with confirmation).
*   **Settings/Export Screen (`SettingsScreen.kv` & `settings_screen.py`):**
    *   "Export Diary" button.
    *   Potentially other app settings in the future.
*   **UI Styling and Theming:**
    *   Develop a consistent visual theme for the app.
    *   Ensure responsive design for different screen sizes if Kivy's capabilities are leveraged.

### Phase 4: Metadata Collection & Integration
*   **Location Services:**
    *   Integrate `plyer.gps` (or equivalent) to fetch current GPS coordinates.
    *   Handle permissions requests for location access.
    *   Provide fallback or manual input if GPS is unavailable.
*   **Weather Data from Sensors:**
    *   Investigate `plyer` or platform-specific libraries for accessing device sensors (e.g., thermometer, hygrometer if available). This is highly device-dependent.
    *   If direct sensor access is not feasible or reliable across platforms, consider an alternative like a weather API (requires internet) or manual input as a fallback. The requirement specifies "local weather based on sensors," so the primary effort should be on sensor integration.
    *   Handle permissions for sensor access if required.
*   **Photo Capture & Selection:**
    *   Integrate `plyer.camera` to capture photos using the device camera.
    *   Integrate `plyer.filechooser` to allow users to select existing photos from their gallery.
    *   Handle camera and storage permissions.
    *   Store captured/selected photos and link paths to the diary entry.
*   **Song of the Day:**
    *   Implement text input fields for song title and artist.
    *   (Optional Future Enhancement: Explore music identification SDKs or local music library access).

### Phase 5: Diary Export Functionality
*   **Export Format Definition:**
    *   Define the structure of the export bundle (e.g., a ZIP archive).
    *   Inside the ZIP:
        *   A manifest file (e.g., `manifest.json`) listing all entries and their metadata.
        *   Individual diary entries (e.g., as text or JSON files).
        *   A `media` subfolder containing all photos.
*   **Implementation:**
    *   Develop logic to gather all diary entries and associated media files.
    *   Implement packaging into the defined bundle format (e.g., using Python's `zipfile` module).
    *   Provide a mechanism for the user to choose a save location for the exported bundle (`plyer.filechooser` can be used here too).

### Phase 6: Integration, Testing & Quality Assurance
*   **Module Integration:**
    *   Ensure all components (UI, core logic, metadata collectors, export) work together seamlessly.
*   **Unit Testing:**
    *   Write unit tests for core logic functions (data models, storage operations, export logic, metadata parsing).
*   **UI/UX Testing:**
    *   Manual testing of all UI flows and interactions.
    *   Test on different screen sizes and orientations.
*   **Platform-Specific Testing:**
    *   If targeting multiple platforms (Android, iOS, Windows, macOS, Linux), test thoroughly on each. Pay special attention to `plyer` functionalities as they interact with native APIs.
*   **Error Handling & Logging:**
    *   Implement robust error handling throughout the app.
    *   Add logging for debugging and diagnostics.
*   **Performance Testing:**
    *   Assess app performance, especially with a large number of entries or large media files.

### Phase 7: Refinement, Documentation & Deployment Preparation
*   **Code Review & Refactoring:**
    *   Clean up code, improve readability, and optimize performance.
*   **User Documentation:**
    *   Create a simple user guide or in-app help.
*   **Developer Documentation:**
    *   Update `README.md` with build and run instructions.
    *   Add comments and docstrings to the code.
*   **Build & Packaging:**
    *   Prepare build scripts for creating distributable packages for target platforms (e.g., using Buildozer or PyInstaller).
