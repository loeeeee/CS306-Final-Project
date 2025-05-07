import os
import json
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

class DiaryExporter:
    """Handles the export of diary entries and associated media files into a bundle."""
    
    def __init__(self, entries_dir: str, media_dir: str):
        """
        Initialize the DiaryExporter.
        
        Args:
            entries_dir: Directory containing diary entries
            media_dir: Directory containing media files
        """
        self.entries_dir = Path(entries_dir)
        self.media_dir = Path(media_dir)
        
        # Ensure directories exist
        self.entries_dir.mkdir(parents=True, exist_ok=True)
        self.media_dir.mkdir(parents=True, exist_ok=True)
    
    def save_entry(self, entry_data: Dict[str, Any]) -> bool:
        """
        Save a diary entry to the entries directory.
        
        Args:
            entry_data: Dictionary containing the entry data
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            # Ensure entry has required fields
            if not all(key in entry_data for key in ['entry_id', 'timestamp_created', 'timestamp_modified', 'text_content']):
                raise ValueError("Entry data missing required fields")
            
            # Create filename from entry_id
            filename = f"entry_{entry_data['entry_id']}.json"
            file_path = self.entries_dir / filename
            
            # Add save timestamp
            entry_data['timestamp_saved'] = datetime.now().isoformat()
            
            # Write entry to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(entry_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving entry: {str(e)}")
            return False
    
    def create_export_bundle(self, output_path: str) -> bool:
        """
        Create a ZIP bundle containing all diary entries and media files.
        
        Args:
            output_path: Path where the export bundle should be saved
            
        Returns:
            bool: True if export was successful, False otherwise
        """
        try:
            # Create a timestamp for the export
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            bundle_path = Path(output_path) / f"diary_export_{timestamp}.zip"
            
            with zipfile.ZipFile(bundle_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Create and add manifest
                manifest = self._create_manifest()
                zipf.writestr('manifest.json', json.dumps(manifest, indent=2))
                
                # Add all diary entries
                for entry_file in self.entries_dir.glob('*.json'):
                    zipf.write(entry_file, f"entries/{entry_file.name}")
                
                # Add all media files
                for media_file in self.media_dir.glob('*'):
                    if media_file.is_file():
                        zipf.write(media_file, f"media/{media_file.name}")
            
            return True
            
        except Exception as e:
            print(f"Error creating export bundle: {str(e)}")
            return False
    
    def _create_manifest(self) -> Dict[str, Any]:
        """
        Create a manifest file containing metadata about the export.
        
        Returns:
            Dict containing manifest information
        """
        manifest = {
            "export_date": datetime.now().isoformat(),
            "version": "1.0",
            "entries": [],
            "media_files": []
        }
        
        # Add entry information
        for entry_file in self.entries_dir.glob('*.json'):
            try:
                with open(entry_file, 'r') as f:
                    entry_data = json.load(f)
                    manifest["entries"].append({
                        "id": entry_data.get("entry_id"),
                        "created": entry_data.get("timestamp_created"),
                        "modified": entry_data.get("timestamp_modified"),
                        "file": entry_file.name
                    })
            except Exception as e:
                print(f"Error processing entry {entry_file}: {str(e)}")
        
        # Add media file information
        for media_file in self.media_dir.glob('*'):
            if media_file.is_file():
                manifest["media_files"].append({
                    "name": media_file.name,
                    "size": media_file.stat().st_size,
                    "type": media_file.suffix[1:].lower()
                })
        
        return manifest 