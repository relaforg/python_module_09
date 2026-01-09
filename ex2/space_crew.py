from enum import Enum
from pydantic import BaseModel, Field, model_validator
from datetime import datetime


class Rank(Enum):
    cadet = 0
    officer = 1
    lieutenant = 2
    captain = 3
    commander = 4


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank = Field()
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime = Field()
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def mission_validation(self):
        if (self.mission_id[0] != "M"):
            raise ValueError("Mission_ID must starts with 'M'")
        if (not len([c for c in self.crew
                     if c.rank in [Rank.captain, Rank.commander]])):
            raise ValueError(
                "Mission must have at least one captain or commander")
        if (self.duration_days > 365):
            exp_crew = [c for c in self.crew if c.years_experience >= 5]
            if (len(exp_crew) < len(self.crew) / 2):
                raise ValueError("Long missions requires 5+ years of"
                                 "experience for at least half of the crew")
        for c in self.crew:
            if (not c.is_active):
                raise ValueError("All the crew must be active")
        return (self)


def main():
    print("Space Mission Crew Validation")
    print("=========================================")
    S = CrewMember(
        member_id="conor",
        name="Sarah Connor",
        rank=Rank.commander,
        age=50,
        specialization="Mission Command",
        years_experience="25",
    )
    J = CrewMember(
        member_id="smith",
        name="John Smith",
        rank=Rank.lieutenant,
        age=30,
        specialization="Navigation",
        years_experience="11",
    )
    A = CrewMember(
        member_id="johnson",
        name="Alice Johnson",
        rank=Rank.officer,
        age=23,
        specialization="Engineering",
        years_experience="5",
    )
    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime.now(),
        duration_days=900,
        crew=[S, J, A],
        budget_millions=2500.0
    )
    print("Valid mission created:")
    print("Mission:", mission.mission_name)
    print("ID:", mission.mission_id)
    print("Destination:", mission.destination)
    print("Duration:", mission.duration_days, "days")
    print(f"Budget: ${mission.budget_millions}M")
    print("Crew size:", len(mission.crew))
    print("Crew members:")
    for c in mission.crew:
        print(f"- {c.name} ({c.rank.name}) - {c.specialization}")
    print("\n=========================================")
    print("Expected validation error:")
    try:
        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            crew=[J, A],
            budget_millions=2500.0
        )
    except ValueError as e:
        print(e)


main()
