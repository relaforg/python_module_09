from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(gt=0, le=20)
    power_level: float = Field(ge=0, le=100)
    oxygen_level: float = Field(ge=0, le=100)
    last_maintenance: datetime = Field()
    is_operational: bool = Field(default=True)
    notes: str = Field(max_length=200, default="")


def main() -> None:
    print("========================================")
    station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime.now()
    )
    print("Valid station created:")
    print("ID:", station.station_id)
    print("Name:", station.name)
    print("Crew:", station.crew_size, "peoples")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print("Status: ", end="")
    if (station.is_operational):
        print("Operational")
    else:
        print("Non-Operational")
    print("\n========================================")
    print("Expected validation error:")
    try:
        station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=30,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.now()
        )
    except ValidationError as e:
        print(e.errors()[0]["msg"])


main()
