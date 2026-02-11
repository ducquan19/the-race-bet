"""Supabase Storage manager for handling file uploads and downloads."""

import io
import os
from typing import Optional, List
from supabase import create_client, Client
from config.supabase_config import SUPABASE_URL, SUPABASE_ANON_KEY


class StorageManager:
    """Manages file storage operations with Supabase Storage."""

    # Storage bucket names
    FACE_IMAGES_BUCKET = "face-images"
    GAME_HISTORY_BUCKET = "game-history"
    SCREENSHOTS_BUCKET = "game-screenshots"

    def __init__(self):
        """Initialize storage manager with Supabase client."""
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        self._ensure_buckets_exist()

    def _ensure_buckets_exist(self) -> None:
        """Ensure all required storage buckets exist."""
        try:
            # Get list of existing buckets
            buckets = self.supabase.storage.list_buckets()
            existing_bucket_names = [bucket.name for bucket in buckets]

            # Create buckets if they don't exist
            required_buckets = [
                (self.FACE_IMAGES_BUCKET, False),  # Private bucket
                (self.GAME_HISTORY_BUCKET, False),  # Private bucket
                (self.SCREENSHOTS_BUCKET, False)    # Private bucket
            ]

            for bucket_name, is_public in required_buckets:
                if bucket_name not in existing_bucket_names:
                    try:
                        self.supabase.storage.create_bucket(
                            bucket_name,
                            options={"public": is_public}
                        )
                        print(f"Created bucket: {bucket_name}")
                    except Exception as e:
                        # Bucket might already exist
                        print(f"Note: Bucket {bucket_name} might already exist: {e}")

        except Exception as e:
            print(f"Error ensuring buckets exist: {e}")

    def upload_face_image(self, username: str, image_data: bytes,
                         image_number: int) -> bool:
        """
        Upload a face image to Supabase Storage.

        Args:
            username: Username for face ID
            image_data: Image data as bytes
            image_number: Image number (1-40)

        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = f"{username}/{image_number}.jpg"

            self.supabase.storage.from_(self.FACE_IMAGES_BUCKET).upload(
                file_path,
                image_data,
                {"content-type": "image/jpeg"}
            )
            return True

        except Exception as e:
            print(f"Error uploading face image: {e}")
            return False

    def download_face_images(self, username: str) -> List[bytes]:
        """
        Download all face images for a user.

        Args:
            username: Username to download images for

        Returns:
            List of image data as bytes
        """
        try:
            # List all files for user
            files = self.supabase.storage.from_(self.FACE_IMAGES_BUCKET).list(username)

            images = []
            for file in files:
                file_path = f"{username}/{file['name']}"
                data = self.supabase.storage.from_(self.FACE_IMAGES_BUCKET).download(file_path)
                if data:
                    images.append(data)

            return images

        except Exception as e:
            print(f"Error downloading face images: {e}")
            return []

    def face_id_exists(self, username: str) -> bool:
        """
        Check if face ID exists for a user.

        Args:
            username: Username to check

        Returns:
            True if face ID exists, False otherwise
        """
        try:
            files = self.supabase.storage.from_(self.FACE_IMAGES_BUCKET).list(username)
            return len(files) > 0
        except:
            return False

    def delete_face_images(self, username: str) -> bool:
        """
        Delete all face images for a user.

        Args:
            username: Username to delete images for

        Returns:
            True if successful, False otherwise
        """
        try:
            # List all files
            files = self.supabase.storage.from_(self.FACE_IMAGES_BUCKET).list(username)

            # Delete each file
            file_paths = [f"{username}/{file['name']}" for file in files]
            if file_paths:
                self.supabase.storage.from_(self.FACE_IMAGES_BUCKET).remove(file_paths)

            return True

        except Exception as e:
            print(f"Error deleting face images: {e}")
            return False

    def upload_game_history(self, username: str, game_number: int,
                           content: str) -> bool:
        """
        Upload game history text file.

        Args:
            username: Username
            game_number: Game number
            content: Text content to save

        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = f"{username}/Game_{game_number}.txt"

            self.supabase.storage.from_(self.GAME_HISTORY_BUCKET).upload(
                file_path,
                content.encode('utf-8'),
                {"content-type": "text/plain"}
            )
            return True

        except Exception as e:
            print(f"Error uploading game history: {e}")
            return False

    def upload_screenshot(self, username: str, game_number: int,
                         image_data: bytes) -> bool:
        """
        Upload game screenshot.

        Args:
            username: Username
            game_number: Game number
            image_data: PNG image data as bytes

        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = f"{username}/Game_{game_number}.png"

            self.supabase.storage.from_(self.SCREENSHOTS_BUCKET).upload(
                file_path,
                image_data,
                {"content-type": "image/png"}
            )
            return True

        except Exception as e:
            print(f"Error uploading screenshot: {e}")
            return False

    def download_screenshot(self, username: str, game_number: int) -> Optional[bytes]:
        """
        Download game screenshot.

        Args:
            username: Username
            game_number: Game number

        Returns:
            Image data as bytes or None if not found
        """
        try:
            file_path = f"{username}/Game_{game_number}.png"
            data = self.supabase.storage.from_(self.SCREENSHOTS_BUCKET).download(file_path)
            return data

        except Exception as e:
            print(f"Error downloading screenshot: {e}")
            return None

    def download_game_history(self, username: str, game_number: int) -> Optional[str]:
        """
        Download game history text file.

        Args:
            username: Username
            game_number: Game number

        Returns:
            Text content or None if not found
        """
        try:
            file_path = f"{username}/Game_{game_number}.txt"
            data = self.supabase.storage.from_(self.GAME_HISTORY_BUCKET).download(file_path)

            if data:
                return data.decode('utf-8')
            return None

        except Exception as e:
            print(f"Error downloading game history: {e}")
            return None

    def list_user_game_history(self, username: str) -> List[dict]:
        """
        List all game history files for a user.

        Args:
            username: Username

        Returns:
            List of file information dictionaries
        """
        try:
            files = self.supabase.storage.from_(self.GAME_HISTORY_BUCKET).list(username)
            return files

        except Exception as e:
            print(f"Error listing game history: {e}")
            return []

    def list_user_screenshots(self, username: str) -> List[dict]:
        """
        List all screenshot files for a user.

        Args:
            username: Username

        Returns:
            List of file information dictionaries
        """
        try:
            files = self.supabase.storage.from_(self.SCREENSHOTS_BUCKET).list(username)
            return files

        except Exception as e:
            print(f"Error listing screenshots: {e}")
            return []

    def get_screenshot_url(self, username: str, game_number: int,
                          expires_in: int = 3600) -> Optional[str]:
        """
        Get a signed URL for a screenshot.

        Args:
            username: Username
            game_number: Game number
            expires_in: URL expiration time in seconds (default: 1 hour)

        Returns:
            Signed URL or None if error
        """
        try:
            file_path = f"{username}/Game_{game_number}.png"
            result = self.supabase.storage.from_(self.SCREENSHOTS_BUCKET).create_signed_url(
                file_path,
                expires_in
            )

            if result and 'signedURL' in result:
                return result['signedURL']
            return None

        except Exception as e:
            print(f"Error getting signed URL: {e}")
            return None
