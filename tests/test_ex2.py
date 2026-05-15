"""Batch validation test for the SpaceMission model.

Loads JSON files produced by ../tools/data_exporter.py and feeds each
record through the SpaceMission model to count valid and invalid ones.

Note: the data exporter only generates valid missions, so this test
shows that the nested CrewMember validation works on real data.

Usage:
    cd ex2
    source venv/bin/activate
    python3 ../tests/test_ex2.py
"""
import json
import sys
from pathlib import Path
from typing import Any

from pydantic import ValidationError

# Allow importing space_crew.py from the ex2 sibling directory
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ex2"))

from space_crew import SpaceMission  # noqa: E402


def load_json(path: Path) -> list[dict[str, Any]]:
    """Read a JSON file and return its parsed content."""
    with path.open(encoding="utf-8") as handle:
        data: list[dict[str, Any]] = json.load(handle)
    return data


def validate_batch(records: list[dict[str, Any]], label: str) -> None:
    """Try to validate every record and print a summary."""
    print(f"\n{label} ({len(records)} records)")
    print("-" * 50)
    valid = 0
    invalid = 0
    for raw in records:
        mission_id = raw.get("mission_id", "???")
        crew_count = len(raw.get("crew", []))
        try:
            mission = SpaceMission(**raw)
            valid += 1
            print(
                f"  OK   {mission_id}  "
                f"({crew_count} crew, {mission.duration_days} days)"
            )
        except ValidationError as exc:
            invalid += 1
            first_msg = exc.errors()[0]["msg"]
            # Clean up Pydantic's custom-validator prefix if present
            first_msg = first_msg.removeprefix("Value error, ")
            print(f"  FAIL {mission_id}  -> {first_msg}")
    print(f"\nResult: {valid} valid / {invalid} invalid")


def main() -> None:
    """Run validation on the generated mission dataset."""
    data_dir = HERE.parent / "tools" / "generated_data"

    missions = load_json(data_dir / "space_missions.json")

    print("=" * 50)
    print("SpaceMission model - batch validation")
    print("=" * 50)

    validate_batch(missions, "Generated mission dataset")


if __name__ == "__main__":
    main()
