"""Email utilities for sending confirmation codes."""

import smtplib
import ssl
import random
from email.message import EmailMessage


class EmailManager:
    """Manages email operations for account verification."""

    SENDER_EMAIL = "nhom11.test@gmail.com"
    SENDER_PASSWORD = "kptb tagm qjle pjyw"
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 465

    @classmethod
    def send_confirmation_code(cls, recipient_email: str) -> str:
        """
        Send a confirmation code to the specified email.

        Args:
            recipient_email: Email address to send code to

        Returns:
            The generated confirmation code as a string
        """
        confirm_code = random.randint(100000, 999999)

        message = EmailMessage()
        message["From"] = cls.SENDER_EMAIL
        message["To"] = recipient_email
        message["Subject"] = "Confirm your account"
        message.set_content(f"Your code confirmation is: {confirm_code}")

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL(
                cls.SMTP_SERVER, cls.SMTP_PORT, context=context
            ) as server:
                server.login(cls.SENDER_EMAIL, cls.SENDER_PASSWORD)
                server.sendmail(cls.SENDER_EMAIL, recipient_email, message.as_string())
        except Exception as e:
            print(f"Error sending email: {e}")
            raise

        return str(confirm_code)

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.

        Args:
            email: Email address to validate

        Returns:
            True if valid, False otherwise
        """
        if len(email) < 10:
            return False
        if email[0] == "@":
            return False
        if not email.endswith("@gmail.com"):
            return False
        return True


# Convenience function for backwards compatibility
def send_confirm_email(email: str) -> str:
    """
    Send confirmation email with code.

    Args:
        email: Email address to send to

    Returns:
        Generated confirmation code as string
    """
    return EmailManager.send_confirmation_code(email)
