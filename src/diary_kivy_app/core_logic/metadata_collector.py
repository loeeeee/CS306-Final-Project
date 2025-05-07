from plyer import gps, camera, filechooser
import os
from datetime import datetime
from .storage_manager import PHOTOS_DIR
import platform

class MetadataCollector:
    def __init__(self):
        self.gps = gps
        self.camera = camera
        self.filechooser = filechooser
        self.current_location = None
        self._setup_gps()

    def _setup_gps(self):
        """Configure GPS settings."""
        try:
            self.gps.configure(on_location=self._on_location)
        except NotImplementedError:
            print("GPS not available on this platform")
            self.gps_available = False
        else:
            self.gps_available = True

    def _on_location(self, **kwargs):
        """Callback for GPS location updates."""
        self.current_location = {
            'latitude': kwargs.get('lat'),
            'longitude': kwargs.get('lon'),
            'altitude': kwargs.get('altitude'),
            'timestamp': datetime.now().isoformat()
        }

    def start_location_tracking(self):
        """Start GPS location tracking."""
        if not self.gps_available:
            return False
        try:
            self.gps.start(minTime=1000, minDistance=1)
            return True
        except NotImplementedError:
            return False

    def stop_location_tracking(self):
        """Stop GPS location tracking."""
        if not self.gps_available:
            return False
        try:
            self.gps.stop()
            return True
        except NotImplementedError:
            return False

    def get_current_location(self):
        """Get the current location data."""
        if not self.gps_available:
            return {
                'latitude': None,
                'longitude': None,
                'altitude': None,
                'timestamp': datetime.now().isoformat(),
                'error': 'GPS not available on this platform'
            }
        return self.current_location

    def take_photo(self, callback, source='camera'):
        """Take a photo using camera or select from gallery."""
        if source == 'camera':
            try:
                self.camera.take_picture(
                    filename=os.path.join(PHOTOS_DIR, f'temp_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'),
                    on_complete=callback
                )
            except NotImplementedError:
                print("Camera not available on this platform")
                return False
        else:  # gallery
            try:
                self.filechooser.open_file(
                    on_selection=callback,
                    filters=['*.jpg', '*.jpeg', '*.png']
                )
            except NotImplementedError:
                print("File chooser not available on this platform")
                return False
        return True

    def get_weather_data(self):
        """
        Get weather data from device sensors.
        Note: This is a placeholder as most devices don't have weather sensors.
        In a real implementation, you might want to use a weather API instead.
        """
        # TODO: Implement actual weather sensor reading if available
        return {
            'temperature': None,
            'humidity': None,
            'description': 'Weather data not available from sensors',
            'platform': platform.system()
        } 