# Diary Kivy App

A multi-platform diary application built with Python and Kivy that allows users to create rich diary entries with metadata including location, weather, photos, and music information.

## Features

- Create and manage diary entries with rich text content
- Automatically capture metadata:
  - Location data (GPS coordinates)
  - Local weather information from device sensors
  - Environment photos and selfies
  - Song of the day
- Export diary entries as a bundle
- Cross-platform support (Windows, macOS, Linux, Android, iOS)

## Requirements

- Python 3.12
- Kivy framework
- Additional dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/diary-kivy-app.git
cd diary-kivy-app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Development Mode
```bash
python src/diary_kivy_app/main.py
```

### Building for Distribution

#### Android
1. Install Buildozer:
```bash
pip install buildozer
```

2. Initialize buildozer:
```bash
buildozer init
```

3. Build the APK:
```bash
buildozer android debug
```

#### Desktop (Windows/macOS/Linux)
1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller --name diary_app --windowed src/diary_kivy_app/main.py
```

## Project Structure

```
diary_kivy_app/
├── core_logic/     # Core business logic and data models
├── ui/            # Kivy UI components and screens
├── utils/         # Utility functions and helpers
├── data/          # Data storage and management
├── tests/         # Unit tests
└── main.py        # Application entry point
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
