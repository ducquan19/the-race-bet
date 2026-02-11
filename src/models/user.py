"""User model representing a player in the game."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Represents a player user."""

    username: str
    money: int
    email: str = ""
    user_id: Optional[str] = None  # Supabase Auth UUID
    num_item: int = 0
    count_item: int = 0
    num_race: int = 0
    bet: int = 0

    def can_afford(self, amount: int) -> bool:
        """Check if user can afford an amount."""
        return self.money >= amount

    def add_money(self, amount: int) -> None:
        """Add money to user account."""
        self.money += amount

    def deduct_money(self, amount: int) -> bool:
        """Deduct money from user account. Returns True if successful."""
        if self.can_afford(amount):
            self.money -= amount
            return True
        return False

    def buy_item(self, item_id: int, price: int) -> bool:
        """
        Buy an item if user can afford it and doesn't have max items.
        Returns True if successful.
        """
        if self.count_item >= 1:
            return False
        if not self.can_afford(price):
            return False

        self.num_item = item_id
        self.count_item += 1
        self.money -= price
        return True

    def use_item(self) -> bool:
        """
        Use an item if available. Returns True if successful.
        """
        if self.count_item > 0:
            self.num_item = 0
            self.count_item -= 1
            return True
        return False

    def increment_race_count(self) -> None:
        """Increment the number of races played."""
        self.num_race += 1

    def set_bet(self, amount: int) -> bool:
        """Set bet amount if valid. Returns True if successful."""
        if amount >= 200 and self.can_afford(amount):
            self.bet = amount
            return True
        return False

    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        return {
            'username': self.username,
            'money': self.money,
            'email': self.email,
            'user_id': self.user_id,
            'num_item': self.num_item,
            'count_item': self.count_item,
            'num_race': self.num_race,
            'bet': self.bet
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user from dictionary."""
        return cls(
            username=data.get('username', ''),
            money=data.get('money', 0),
            email=data.get('email', ''),
            user_id=data.get('id') or data.get('user_id'),
            num_item=data.get('num_item', 0),
            count_item=data.get('count_item', 0),
            num_race=data.get('num_race', 0),
            bet=data.get('bet', 0)
        )
