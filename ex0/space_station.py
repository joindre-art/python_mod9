"""Space Station Data Validation - Exercise 0.

This module demonstrates basic Pydantic model creation with BaseModel
and Field validation for monitoring space station data.
"""
from datetime import datetime

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    """Pydantic model representing a space station with validated fields."""

    # Short technical identifier of the station
    station_id: str = Field(..., min_length=3, max_length=10)
    # Human-readable name of the station
    name: str = Field(..., min_length=1, max_length=50)
    # Number of crew members currently on board
    crew_size: int = Field(..., ge=1, le=20)
    # Battery / solar power level as a percentage
    power_level: float = Field(..., ge=0.0, le=100.0)
    # Breathable oxygen ratio as a percentage
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    # Date of the last technical maintenance
    last_maintenance: datetime
    # Whether the station is currently in service
    is_operational: bool = True
    # Optional free-text notes (alerts, observations)
    notes: str | None = Field(default=None, max_length=200)


def display_station(station: SpaceStation) -> None:
    """Print a space station's information in the expected format."""
    status = "Operational" if station.is_operational else "Offline"
    print("Valid station created:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(f"Status: {status}")


def main() -> None:
    """Demonstrate valid and invalid space station creation."""
    print("Space Station Data Validation")
    print("=" * 40)

    # Build a valid station instance
    try:
        valid_station = SpaceStation(
            station_id="XSANTI01",
            name="Xsanti Deep Space Photo Lab",
            crew_size=4,
            power_level=95.8,
            oxygen_level=96.1,
            last_maintenance=datetime(2026, 3, 10, 14, 0, 0),
            is_operational=True,
            notes=(
                "Laboratoire d'astrophotographie longue exposition "
                "- Maitre Photo C. Vilbois"
            ),
        )
        display_station(valid_station)
    except ValidationError as exc:
        # Should not happen with valid data, but stay defensive
        print(f"Unexpected error on valid station: {exc}")

    print()
    print("=" * 40)
    print("Expected validation error:")

    # Try to build an invalid station: crew_size exceeds max of 20
    try:
        SpaceStation(
            station_id="XSANTI02",
            name="Overcrowded Test Station",
            crew_size=25,  # Invalid: exceeds maximum of 20
            power_level=80.0,
            oxygen_level=90.0,
            last_maintenance=datetime(2026, 3, 10, 14, 0, 0),
        )
    except ValidationError as exc:
        # Pydantic returns a list of error dicts; show only the message
        first_error = exc.errors()[0]
        print(first_error["msg"])


if __name__ == "__main__":
    main()
