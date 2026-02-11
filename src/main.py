"""
Lucky Race Game - Refactored Version

Entry point for the game application.
"""

from core.game import Game


def main():
    """Main entry point."""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
