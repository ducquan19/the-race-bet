"""Main game class."""

import pygame
import sys
from typing import Optional
from config.settings import *
from config.paths import ICON_PATH
from database import DatabaseManager
from audio import SoundManager
from models import User
from core.state_manager import StateManager, GameState
from utils.drawing_utils import create_fonts


class Game:
    """Main game class that manages the game loop and state transitions."""

    def __init__(self):
        """Initialize the game."""
        pygame.init()
        pygame.font.init()

        # Setup display
        self.display = pygame.display.set_mode(WINDOWSIZE)
        pygame.display.set_caption(GAME_TITLE)

        # Load and set icon
        try:
            icon = pygame.image.load(ICON_PATH)
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"Could not load icon: {e}")

        # Initialize game components
        self.clock = pygame.time.Clock()
        self.fonts = create_fonts()
        self.sound_manager = SoundManager()
        self.db_manager = DatabaseManager()
        self.state_manager = StateManager()

        # Game state
        self.current_user: Optional[User] = None
        self.language = DEFAULT_LANGUAGE
        self.running = True

        # Initialize state
        self.state_manager.change_state(GameState.LOGIN)

    def run(self) -> None:
        """Main game loop."""
        while self.running:
            current_state = self.state_manager.get_current_state()

            if current_state == GameState.LOGIN:
                self._run_login_screen()
            elif current_state == GameState.SIGNUP:
                self._run_signup_screen()
            elif current_state == GameState.FORGOT_PASSWORD:
                self._run_forgot_password_screen()
            elif current_state == GameState.CHANGE_PASSWORD:
                self._run_change_password_screen()
            elif current_state == GameState.MAIN_MENU:
                self._run_main_menu()
            elif current_state == GameState.QUIT:
                self.running = False
            else:
                # Handle other states
                print(f"State {current_state} not implemented yet")
                self.state_manager.change_state(GameState.LOGIN)

        self.quit()

    def _run_login_screen(self) -> None:
        """Run login screen."""
        from screens.login_screen import LoginScreen

        screen = LoginScreen(
            self.display, self.clock, self.fonts, self.sound_manager, self.db_manager
        )
        screen.set_language(self.language)
        result = screen.run()

        if result:
            if result["action"] == "login_success":
                self.current_user = result["user"]
                self.state_manager.change_state(GameState.MAIN_MENU)
            elif result["action"] == "goto_signup":
                self.state_manager.change_state(GameState.SIGNUP)
            elif result["action"] == "goto_forgot":
                self.state_manager.change_state(GameState.FORGOT_PASSWORD)
            elif result["action"] == "setting":
                self.language = result.get("language", self.language)
                self.sound_manager.set_volume(result.get("volume", 0))
        else:
            self.running = False

    def _run_signup_screen(self) -> None:
        """Run signup screen."""
        from screens.signup_screen import SignupScreen

        screen = SignupScreen(
            self.display, self.clock, self.fonts, self.sound_manager, self.db_manager
        )
        screen.set_language(self.language)
        result = screen.run()

        if result and result.get("action") == "signup_success":
            self.current_user = result["user"]
            self.state_manager.change_state(GameState.MAIN_MENU)
        else:
            self.state_manager.change_state(GameState.LOGIN)

    def _run_forgot_password_screen(self) -> None:
        """Run forgot password screen."""
        from screens.forgot_password_screen import ForgotPasswordScreen

        screen = ForgotPasswordScreen(
            self.display, self.clock, self.fonts, self.sound_manager, self.db_manager
        )
        screen.set_language(self.language)
        result = screen.run()

        if result:
            if result.get("action") == "change_password":
                # Store user info for change password screen
                self.state_manager.change_state(
                    GameState.CHANGE_PASSWORD,
                    user_id=result["user_id"],
                    username=result["username"],
                )
            else:
                self.state_manager.change_state(GameState.LOGIN)
        else:
            self.state_manager.change_state(GameState.LOGIN)

    def _run_change_password_screen(self) -> None:
        """Run change password screen."""
        from screens.change_password_screen import ChangePasswordScreen

        # Get state data
        state_data = self.state_manager._state_data
        user_id = state_data.get("user_id")
        username = state_data.get("username")

        if not user_id or not username:
            self.state_manager.change_state(GameState.LOGIN)
            return

        screen = ChangePasswordScreen(
            self.display,
            self.clock,
            self.fonts,
            self.sound_manager,
            self.db_manager,
            user_id,
            username,
        )
        screen.set_language(self.language)
        result = screen.run()

        if result and result.get("action") == "goto_login":
            self.state_manager.change_state(GameState.LOGIN)
        else:
            self.state_manager.change_state(GameState.LOGIN)

    def _run_main_menu(self) -> None:
        """Run main menu screen."""
        from screens.main_menu_screen import MainMenuScreen

        if not self.current_user:
            self.state_manager.change_state(GameState.LOGIN)
            return

        screen = MainMenuScreen(
            self.display,
            self.clock,
            self.fonts,
            self.sound_manager,
            self.db_manager,
            self.current_user,
        )
        screen.set_language(self.language)
        result = screen.run()

        if result:
            action = result.get("action")
            if action == "logout":
                self.db_manager.save_user(self.current_user)
                self.current_user = None
                self.state_manager.change_state(GameState.LOGIN)
            elif action == "quit":
                self.db_manager.save_user(self.current_user)
                self.running = False
            elif action == "play":
                # Navigate to game selection
                self.state_manager.change_state(GameState.SELECT_SET)
            elif action == "shop":
                self.state_manager.change_state(GameState.SHOP)
            elif action == "history":
                self.state_manager.change_state(GameState.HISTORY)
            elif action == "help":
                self.state_manager.change_state(GameState.HELP)
            elif action == "minigame":
                self.state_manager.change_state(GameState.MINIGAME)
            elif action == "settings":
                self.language = result.get("language", self.language)
                self.sound_manager.set_volume(result.get("volume", 0))

    def quit(self) -> None:
        """Clean up and quit the game."""
        if self.current_user:
            self.db_manager.save_user(self.current_user)

        pygame.quit()
        sys.exit()
