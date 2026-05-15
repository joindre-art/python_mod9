"""Batch validation test for the SpaceStation model.

Loads JSON files produced by ../tools/data_exporter.py and feeds each
record through the SpaceStation model to count valid and invalid ones.

Usage:
    cd ex0
    source venv/bin/activate
    python3 ../tests/test_ex0.py
"""
import json
import sys
from pathlib import Path
from typing import Any

from pydantic import ValidationError

# Allow importing space_station.py from the ex0 sibling directory
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ex0"))

from space_station import SpaceStation  # noqa: E402


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
        try:
            SpaceStation(**raw)
            valid += 1
            print(f"  OK   {raw.get('station_id', '???')}")
        except ValidationError as exc:
            invalid += 1
            first_msg = exc.errors()[0]["msg"]
            print(f"  FAIL {raw.get('station_id', '???')}  -> {first_msg}")
    print(f"\nResult: {valid} valid / {invalid} invalid")


def main() -> None:
    """Run validation on both valid and invalid generated datasets."""
    data_dir = HERE.parent / "tools" / "generated_data"

    valid_data = load_json(data_dir / "space_stations.json")
    invalid_data = load_json(data_dir / "invalid_stations.json")

    print("=" * 50)
    print("SpaceStation model - batch validation")
    print("=" * 50)

    validate_batch(valid_data, "Generated 'valid' dataset")
    validate_batch(invalid_data, "Generated 'invalid' dataset")


if __name__ == "__main__":
    main()
