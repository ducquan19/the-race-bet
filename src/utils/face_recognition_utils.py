"""Face recognition utilities."""

import cv2
import face_recognition
import numpy as np
import os
from typing import Optional
from config.paths import FACE_CASCADE
from utils.storage_manager import StorageManager


class FaceIDManager:
    """Manages face recognition operations."""

    def __init__(self):
        """Initialize face ID manager."""
        self.cascade_path = FACE_CASCADE
        self.storage = StorageManager()

    def setup_face_id(self, username: str) -> tuple[bool, Optional[str]]:
        """
        Setup face ID for a user by capturing face images.

        Args:
            username: Username to setup face ID for

        Returns:
            Tuple of (success, error_message)
        """
        video = cv2.VideoCapture(0)
        face_detect = cv2.CascadeClassifier(self.cascade_path)
        count = 0

        # Check if face ID already exists
        if self.storage.face_id_exists(username):
            video.release()
            cv2.destroyAllWindows()
            return False, "ALREADY_EXISTS"

        captured_images = []

        try:
            while True:
                ret, frame = video.read()
                if not ret:
                    break

                faces = face_detect.detectMultiScale(frame, 1.3, 5)
                count_faces = 0

                for (x, y, w, h) in faces:
                    count_faces += 1
                    count += 1

                    # Save face image to memory
                    face_img = frame[y:y+h, x:x+w]
                    captured_images.append((count, face_img))

                    # Draw rectangle
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

                cv2.imshow('Face ID Setup', frame)

                # Check for quit
                if cv2.waitKey(1) == ord("q"):
                    break

                # Multiple faces detected
                if count_faces > 1:
                    video.release()
                    cv2.destroyAllWindows()
                    return False, "MULTIPLE_FACES"

                # Enough images captured
                if count > 39:
                    break

            video.release()
            cv2.destroyAllWindows()

            # Upload all captured images to Supabase Storage
            for img_number, face_img in captured_images:
                # Convert image to bytes
                _, img_encoded = cv2.imencode('.jpg', face_img)
                img_bytes = img_encoded.tobytes()

                # Upload to storage
                success = self.storage.upload_face_image(username, img_bytes, img_number)
                if not success:
                    print(f"Warning: Failed to upload image {img_number}")

            return True, None

        except Exception as e:
            video.release()
            cv2.destroyAllWindows()
            print(f"Error setting up face ID: {e}")
            return False, "ERROR"

    def verify_face_id(self, username: str) -> bool:
        """
        Verify face ID for login.

        Args:
            username: Username to verify

        Returns:
            True if face matches, False otherwise
        """
        # Check if face ID exists
        if not self.storage.face_id_exists(username):
            return False

        # Download face images from Supabase Storage
        image_bytes_list = self.storage.download_face_images(username)

        if not image_bytes_list:
            return False

        # Convert bytes to images
        images = []
        for img_bytes in image_bytes_list:
            # Convert bytes to numpy array
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is not None:
                images.append(img)

        if not images:
            return False

        # Encode known faces
        encoded_faces = self._encode_faces(images)

        # Start capture
        cap = cv2.VideoCapture(0)
        verified = False

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Resize for faster processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                # Find faces in frame
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                for face_encoding, face_location in zip(face_encodings, face_locations):
                    # Compare with known faces
                    matches = face_recognition.compare_faces(encoded_faces, face_encoding)
                    face_distances = face_recognition.face_distance(encoded_faces, face_encoding)

                    if len(face_distances) > 0:
                        best_match_index = np.argmin(face_distances)

                        if face_distances[best_match_index] < 0.50:
                            verified = True

                        # Draw rectangle
                        y1, x2, y2, x1 = face_location
                        y1, x2, y2, x1 = y1*2, x2*2, y2*2, x1*2
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                cv2.imshow('Face ID Verification', frame)

                if cv2.waitKey(1) == ord("q") or verified:
                    break

            cap.release()
            cv2.destroyAllWindows()
            return verified

        except Exception as e:
            cap.release()
            cv2.destroyAllWindows()
            print(f"Error verifying face ID: {e}")
            return False

    def _encode_faces(self, images: list) -> list:
        """Encode list of face images."""
        encoded_list = []
        for img in images:
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_img)
            if encodings:
                encoded_list.append(encodings[0])
        return encoded_list
