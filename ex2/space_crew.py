"""Space Crew Management Validation - Exercise 2.

This module demonstrates nested Pydantic models and complex validation
rules for managing space mission crews.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    """Possible ranks for a crew member."""

    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    """Pydantic model representing a single crew member."""

    # Internal identifier of the crew member
    member_id: str = Field(..., min_length=3, max_length=10)
    # Full display name of the crew member
    name: str = Field(..., min_length=2, max_length=50)
    # Hierarchical rank in the crew
    rank: Rank
    # Age of the crew member in years
    age: int = Field(..., ge=18, le=80)
    # Job specialization on board (e.g. Navigation, Engineering)
    specialization: str = Field(..., min_length=3, max_length=30)
    # Years of professional experience
    years_experience: int = Field(..., ge=0, le=50)
    # Whether the crew member is currently in active service
    is_active: bool = True


class SpaceMission(BaseModel):
    """Pydantic model representing a space mission with its crew."""

    # Mission identifier, must start with "M"
    mission_id: str = Field(..., min_length=5, max_length=15)
    # Display name of the mission
    mission_name: str = Field(..., min_length=3, max_length=100)
    # Destination of the mission (e.g. Mars, Moon, Europa)
    destination: str = Field(..., min_length=3, max_length=50)
    # Scheduled launch date and time
    launch_date: datetime
    # Mission duration in days (max 10 years)
    duration_days: int = Field(..., ge=1, le=3650)
    # List of crew members assigned to the mission
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    # Current status of the mission (planned, active, completed...)
    mission_status: str = "planned"
    # Mission budget in millions of dollars
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_safety_rules(self) -> "SpaceMission":
        """Apply mission safety rules after field validation."""
        # Rule 1: mission ID must start with "M"
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        # Rule 2: must have at least one Commander or Captain
        has_command = any(
            member.rank in (Rank.COMMANDER, Rank.CAPTAIN)
            for member in self.crew
        )
        if not has_command:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        # Rule 3: all crew members must be active
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        # Rule 4: long missions need 50% experienced crew (5+ years)
        if self.duration_days > 365:
            experienced = sum(
                1 for member in self.crew if member.years_experience >= 5
            )
            if experienced * 2 < len(self.crew):
                raise ValueError(
                    "Long missions (> 365 days) need 50% experienced "
                    "crew (5+ years)"
                )

        return self


def display_mission(mission: SpaceMission) -> None:
    """Print a space mission and its crew in the expected format."""
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(
            f"- {member.name} ({member.rank.value}) "
            f"- {member.specialization}"
        )


def build_valid_crew() -> list[CrewMember]:
    """Build the crew used by the valid mission demonstration."""
    return [
        CrewMember(
            member_id="CM001",
            name="Carole Vilbois",
            rank=Rank.COMMANDER,
            age=50,
            specialization="Mission Photography",
            years_experience=12,
            is_active=True,
        ),
        CrewMember(
            member_id="CM002",
            name="Stefan Cizmar",
            rank=Rank.CAPTAIN,
            age=55,
            specialization="Mission Command",
            years_experience=15,
            is_active=True,
        ),
        CrewMember(
            member_id="CM003",
            name="Patrick Baeken",
            rank=Rank.LIEUTENANT,
            age=35,
            specialization="Navigation",
            years_experience=8,
            is_active=True,
        ),
        CrewMember(
            member_id="CM004",
            name="Gilbert Vilbois",
            rank=Rank.OFFICER,
            age=38,
            specialization="Engineering",
            years_experience=6,
            is_active=True,
        ),
    ]


def build_invalid_crew() -> list[CrewMember]:
    """Build a crew without any Commander or Captain."""
    return [
        CrewMember(
            member_id="CM010",
            name="Test Lieutenant",
            rank=Rank.LIEUTENANT,
            age=32,
            specialization="Navigation",
            years_experience=6,
            is_active=True,
        ),
        CrewMember(
            member_id="CM011",
            name="Test Officer",
            rank=Rank.OFFICER,
            age=28,
            specialization="Engineering",
            years_experience=5,
            is_active=True,
        ),
        CrewMember(
            member_id="CM012",
            name="Test Cadet",
            rank=Rank.CADET,
            age=22,
            specialization="Maintenance",
            years_experience=1,
            is_active=True,
        ),
    ]


def main() -> None:
    """Demonstrate valid and invalid mission creation."""
    print("Space Mission Crew Validation")
    print("=" * 41)

    # Build a valid mission with a balanced and experienced crew
    try:
        valid_mission = SpaceMission(
            mission_id="MLUX_MARS01",
            mission_name="Luxembourg Mars Photographic Survey",
            destination="Mars",
            launch_date=datetime(2027, 4, 15, 9, 30, 0),
            duration_days=900,
            crew=build_valid_crew(),
            mission_status="planned",
            budget_millions=2500.0,
        )
        display_mission(valid_mission)
    except ValidationError as exc:
        # Should not happen with valid data, but stay defensive
        print(f"Unexpected error on valid mission: {exc}")

    print()
    print("=" * 41)
    print("Expected validation error:")

    # Try an invalid mission: no Commander or Captain in the crew
    try:
        SpaceMission(
            mission_id="MLUX_MARS02",
            mission_name="Headless Mission Test",
            destination="Mars",
            launch_date=datetime(2027, 6, 1, 10, 0, 0),
            duration_days=200,
            crew=build_invalid_crew(),
            mission_status="planned",
            budget_millions=1500.0,
        )
    except ValidationError as exc:
        # Strip Pydantic's "Value error, " prefix from the raw message
        first_error = exc.errors()[0]
        msg = first_error["msg"].removeprefix("Value error, ")
        print(msg)


if __name__ == "__main__":
    main()
