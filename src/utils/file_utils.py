"""File management utilities."""

import os
import shutil
from utils.storage_manager import StorageManager


class FileManager:
    """Manages file operations."""

    def __init__(self):
        """Initialize file manager with storage manager."""
        self.storage = StorageManager()

    @staticmethod
    def delete_files_in_directory(directory_path: str) -> None:
        """
        Delete all files in a directory.

        Args:
            directory_path: Path to directory
        """
        if not os.path.exists(directory_path):
            return

        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    @staticmethod
    def copy_directory(src: str, dst: str) -> None:
        """
        Copy directory from source to destination.

        Args:
            src: Source directory path
            dst: Destination directory path
        """
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    def save_game_history(self, username: str, game_number: int,
                         rank_file: str, screenshot_file: str) -> None:
        """
        Save game history files to Supabase Storage.

        Args:
            username: Username
            game_number: Game number
            rank_file: Path to rank text file
            screenshot_file: Path to screenshot image file
        """
        try:
            # Read rank file content
            with open(rank_file, 'r', encoding='utf-8') as f:
                rank_content = f.read()

            # Upload rank file to storage
            self.storage.upload_game_history(username, game_number, rank_content)

            # Read screenshot file
            with open(screenshot_file, 'rb') as f:
                screenshot_data = f.read()

            # Upload screenshot to storage
            self.storage.upload_screenshot(username, game_number, screenshot_data)

        except Exception as e:
            print(f"Error saving game history: {e}")

    @staticmethod
    def ensure_directory_exists(directory_path: str) -> None:
        """
        Ensure directory exists, create if it doesn't.

        Args:
            directory_path: Path to directory
        """
        os.makedirs(directory_path, exist_ok=True)
