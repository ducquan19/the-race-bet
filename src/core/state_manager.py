"""State manager for handling game states."""

from enum import Enum
from typing import Optional, Dict, Type


class GameState(Enum):
    """Enumeration of all possible game states."""

    LOGIN = "login"
    SIGNUP = "signup"
    FORGOT_PASSWORD = "forgot_password"
    CHANGE_PASSWORD = "change_password"
    MAIN_MENU = "main_menu"
    SETTINGS = "settings"
    HELP = "help"
    SHOP = "shop"
    HISTORY = "history"
    SELECT_SET = "select_set"
    SELECT_CAR = "select_car"
    BET = "bet"
    SELECT_RACE_SIZE = "select_race_size"
    RACING = "racing"
    RESULT = "result"
    MINIGAME = "minigame"
    QUIT = "quit"


class StateManager:
    """Manages transitions between game states."""

    def __init__(self):
        """Initialize state manager."""
        self._current_state: Optional[GameState] = None
        self._previous_state: Optional[GameState] = None
        self._state_data: Dict = {}

    def change_state(self, new_state: GameState, **kwargs) -> None:
        """
        Change to a new state.

        Args:
            new_state: The state to transition to
            **kwargs: Additional data to pass to the new state
        """
        self._previous_state = self._current_state
        self._current_state = new_state
        self._state_data = kwargs

    def get_current_state(self) -> Optional[GameState]:
        """Get the current game state."""
        return self._current_state

    def get_previous_state(self) -> Optional[GameState]:
        """Get the previous game state."""
        return self._previous_state

    def get_state_data(self) -> Dict:
        """Get data associated with current state."""
        return self._state_data

    def go_back(self) -> None:
        """Return to the previous state."""
        if self._previous_state:
            temp = self._current_state
            self._current_state = self._previous_state
            self._previous_state = temp
            self._state_data = {}

    def reset(self) -> None:
        """Reset state manager to initial state."""
        self._current_state = GameState.LOGIN
        self._previous_state = None
        self._state_data = {}
