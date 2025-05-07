"""
Core logic package for the diary app.
Contains data models and storage functionality.
"""

from .diary_entry import DiaryEntry
from .storage import Storage

__all__ = ['DiaryEntry', 'Storage'] 