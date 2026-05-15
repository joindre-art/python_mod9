"""Alien Contact Logs Validation - Exercise 1.

This module demonstrates custom validation logic using @model_validator
for complex business rules on alien contact reports.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    """Possible types of alien contact."""

    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    """Pydantic model representing an alien contact report."""

    # Unique contact ID, must start with "AC"
    contact_id: str = Field(..., min_length=5, max_length=15)
    # When the contact occurred
    timestamp: datetime
    # Where the contact happened
    location: str = Field(..., min_length=3, max_length=100)
    # Communication type (radio, visual, physical, telepathic)
    contact_type: ContactType
    # Signal strength on a 0-10 scale
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    # Duration of the contact in minutes (max 24 hours)
    duration_minutes: int = Field(..., ge=1, le=1440)
    # Number of human witnesses present
    witness_count: int = Field(..., ge=1, le=100)
    # Optional message received from the alien entity
    message_received: str | None = Field(default=None, max_length=500)
    # Whether the report has been officially verified
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_business_rules(self) -> "AlienContact":
        """Apply custom business rules after field validation."""
        # Rule 1: contact ID must start with "AC" (Alien Contact)
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        # Rule 2: physical contact reports must be verified
        if (
            self.contact_type == ContactType.PHYSICAL
            and not self.is_verified
        ):
            raise ValueError("Physical contact reports must be verified")
        # Rule 3: telepathic contact requires at least 3 witnesses
        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        # Rule 4: strong signals (> 7.0) should include received messages
        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
            )
        return self


def display_contact(contact: AlienContact) -> None:
    """Print an alien contact report in the expected format."""
    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    print(f"Message: '{contact.message_received}'")


def main() -> None:
    """Demonstrate valid and invalid alien contact reports."""
    print("Alien Contact Log Validation")
    print("=" * 38)

    # Build a valid contact report (radio, strong signal with message)
    try:
        valid_contact = AlienContact(
            contact_id="AC_LUX_001",
            timestamp=datetime(2026, 4, 28, 22, 15, 0),
            location="Bourscheid Castle, Luxembourg",
            contact_type=ContactType.RADIO,
            signal_strength=8.7,
            duration_minutes=45,
            witness_count=5,
            message_received=(
                "Greetings from Tau Ceti - we observe your photography"
            ),
            is_verified=True,
        )
        display_contact(valid_contact)
    except ValidationError as exc:
        # Should not happen with valid data, but stay defensive
        print(f"Unexpected error on valid contact: {exc}")

    print()
    print("=" * 38)
    print("Expected validation error:")

    # Try an invalid contact: telepathic with only 2 witnesses
    try:
        AlienContact(
            contact_id="AC_LUX_002",
            timestamp=datetime(2026, 4, 30, 3, 0, 0),
            location="Mullerthal Forest, Luxembourg",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=5.0,
            duration_minutes=10,
            witness_count=2,  # Invalid: telepathic needs at least 3
            message_received="Faint signal received",
            is_verified=False,
        )
    except ValidationError as exc:
        # Strip Pydantic's "Value error, " prefix from the raw message
        first_error = exc.errors()[0]
        msg = first_error["msg"].removeprefix("Value error, ")
        print(msg)


if __name__ == "__main__":
    main()
