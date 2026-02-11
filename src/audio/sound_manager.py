"""Sound manager for handling game audio."""

import pygame
from typing import Dict, Optional
from config.paths import SOUND_FILES


class SoundManager:
    """Manages game sounds and music."""

    def __init__(self):
        """Initialize sound manager."""
        pygame.mixer.init()
        self._sounds: Dict[str, pygame.mixer.Sound] = {}
        self._volume = 0  # 0 = off, 1 = on
        self._load_sounds()

    def _load_sounds(self) -> None:
        """Load all game sounds."""
        for name, path in SOUND_FILES.items():
            try:
                self._sounds[name] = pygame.mixer.Sound(path)
            except Exception as e:
                print(f"Could not load sound {name}: {e}")

    def play(self, sound_name: str, loops: int = 0) -> None:
        """
        Play a sound.

        Args:
            sound_name: Name of the sound to play
            loops: Number of times to loop (-1 for infinite)
        """
        if sound_name in self._sounds and self._volume > 0:
            self._sounds[sound_name].play(loops=loops)

    def stop(self, sound_name: str) -> None:
        """
        Stop a sound.

        Args:
            sound_name: Name of the sound to stop
        """
        if sound_name in self._sounds:
            self._sounds[sound_name].stop()

    def stop_all(self) -> None:
        """Stop all sounds."""
        pygame.mixer.stop()

    def set_volume(self, volume: int) -> None:
        """
        Set global volume.

        Args:
            volume: 0 for off, 1 for on
        """
        self._volume = volume
        if volume == 0:
            self.stop_all()

    def get_volume(self) -> int:
        """Get current volume setting."""
        return self._volume

    def set_sound_volume(self, sound_name: str, volume: float) -> None:
        """
        Set volume for a specific sound.

        Args:
            sound_name: Name of the sound
            volume: Volume level (0.0 to 1.0)
        """
        if sound_name in self._sounds:
            self._sounds[sound_name].set_volume(volume)
