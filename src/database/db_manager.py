"""Database manager for handling user data with Supabase."""

import os
from typing import Optional, Tuple, List
from supabase import create_client, Client
from models.user import User
from config.settings import INITIAL_MONEY
from config.supabase_config import SUPABASE_URL, SUPABASE_ANON_KEY


class DatabaseManager:
    """Manages database operations for user accounts using Supabase."""

    def __init__(self):
        """Initialize database manager with Supabase client."""
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        self._current_user_id: Optional[str] = None

    def check_account_exists(
        self, username: str, password: str = "", email: str = ""
    ) -> Tuple[int, Optional[str]]:
        """
        Check if account exists and verify credentials.

        Args:
            username: Username to check
            password: Password to verify (uses Supabase Auth)
            email: Email to check

        Returns:
            Tuple of (status, user_id) where:
            - status: -1 (not exist), 0 (wrong password), 1 (correct), 2 (email exists)
            - user_id: Supabase user UUID or None
        """
        try:
            # Check if username exists
            result = (
                self.supabase.table("users")
                .select("id, username")
                .eq("username", username)
                .execute()
            )

            if result.data:
                user_id = result.data[0]["id"]

                if password:
                    # Verify password using Supabase Auth
                    try:
                        auth_result = self.supabase.auth.sign_in_with_password(
                            {
                                "email": (
                                    email if email else f"{username}@luckyrace.local"
                                ),
                                "password": password,
                            }
                        )
                        if auth_result.user:
                            self._current_user_id = auth_result.user.id
                            return 1, user_id
                        else:
                            return 0, user_id
                    except Exception:
                        return 0, user_id
                else:
                    return 1, user_id

            # Check if email exists
            if email:
                email_result = self.supabase.auth.admin.list_users()
                # Note: This requires service role key for full functionality
                return 2, None

            return -1, None

        except Exception as e:
            print(f"Error checking account: {e}")
            return -1, None

    def create_user(self, username: str, password: str, email: str) -> User:
        """
        Create a new user account in Supabase.
        Supabase will automatically send confirmation email.

        Args:
            username: Username for new account
            password: Password for new account
            email: Email for new account

        Returns:
            Newly created User object
        """
        try:
            # Create user in Supabase Auth
            # Supabase automatically sends confirmation email
            auth_result = self.supabase.auth.sign_up(
                {"email": email, "password": password}
            )

            if not auth_result.user:
                raise Exception("Failed to create auth user")

            user_id = auth_result.user.id

            # Note: User won't be able to login until they confirm email
            # The trigger will create the profile when they confirm

            # Create and return user object
            return User(
                username=username,
                money=INITIAL_MONEY,
                email=email,
                user_id=user_id,
                num_item=0,
                count_item=0,
                num_race=0,
            )

        except Exception as e:
            print(f"Error creating user: {e}")
            raise

    def load_user(self, user_id: str) -> User:
        """
        Load user data from Supabase.

        Args:
            user_id: Supabase user UUID

        Returns:
            User object with loaded data
        """
        try:
            result = (
                self.supabase.table("users").select("*").eq("id", user_id).execute()
            )

            if not result.data:
                raise Exception(f"User {user_id} not found")

            user_data = result.data[0]

            # Count game runs for num_race
            runs_result = (
                self.supabase.table("game_runs")
                .select("id", count="exact")
                .eq("user_id", user_id)
                .execute()
            )
            num_race = runs_result.count if runs_result.count else 0

            return User(
                username=user_data["username"],
                money=user_data.get("money", 0),
                email="",  # Email is stored in auth, not users table
                user_id=user_id,
                num_item=user_data.get("num_item", 0),
                count_item=user_data.get("count_item", 0),
                num_race=num_race,
            )

        except Exception as e:
            print(f"Error loading user: {e}")
            raise

    def save_user(self, user: User) -> None:
        """
        Save user data to Supabase.

        Args:
            user: User object to save
        """
        if not user.user_id:
            raise ValueError("User has no user_id")

        try:
            update_data = {
                "money": int(user.money),
                "num_item": int(user.num_item),
                "count_item": int(user.count_item),
            }

            self.supabase.table("users").update(update_data).eq(
                "id", user.user_id
            ).execute()

        except Exception as e:
            print(f"Error saving user: {e}")
            raise

    def save_bet(self, user: User, bet_money: int, won: bool) -> None:
        """
        Save bet result to game history.

        Args:
            user: User who placed the bet
            bet_money: Bet amount
            won: Whether the user won
        """
        if not user.user_id:
            raise ValueError("User has no user_id")

        try:
            # Create a new game run
            run_data = {"user_id": user.user_id, "run_index": user.num_race}

            run_result = self.supabase.table("game_runs").insert(run_data).execute()

            if run_result.data:
                run_id = run_result.data[0]["id"]

                # Save the score
                score_data = {
                    "run_id": run_id,
                    "score": bet_money if won else -bet_money,
                }

                self.supabase.table("game_scores").insert(score_data).execute()

        except Exception as e:
            print(f"Error saving bet: {e}")
            raise

    def change_password(self, user_id: str, new_password: str) -> None:
        """
        Change user password in Supabase Auth.

        Args:
            user_id: Supabase user UUID
            new_password: New password
        """
        try:
            self.supabase.auth.update_user({"password": new_password})
        except Exception as e:
            print(f"Error changing password: {e}")
            raise

    def update_password(self, user_id: str, new_password: str) -> bool:
        """
        Update user password for password recovery flow.

        Args:
            user_id: Supabase user UUID
            new_password: New password

        Returns:
            True if successful, False otherwise
        """
        try:
            # For password reset, we need to use the admin update
            # This requires service_role key, but for now we'll use the auth update
            self.supabase.auth.update_user({"password": new_password})
            return True
        except Exception as e:
            print(f"Error updating password: {e}")
            return False

    def get_user_history(self, user: User) -> List[dict]:
        """
        Get game history for a user.

        Args:
            user: User to get history for

        Returns:
            List of game run records with scores
        """
        if not user.user_id:
            return []

        try:
            # Get all game runs with their scores
            result = (
                self.supabase.table("game_runs")
                .select("*, game_scores(*)")
                .eq("user_id", user.user_id)
                .order("run_index")
                .execute()
            )

            return result.data if result.data else []

        except Exception as e:
            print(f"Error getting user history: {e}")
            return []

    def logout(self) -> None:
        """Logout current user."""
        try:
            self.supabase.auth.sign_out()
            self._current_user_id = None
        except Exception as e:
            print(f"Error logging out: {e}")
