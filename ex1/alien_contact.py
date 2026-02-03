from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime


class ContactType(Enum):
    radio = 0
    visual = 1
    physical = 2
    telepathic = 3


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime = Field()
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType = Field()
    signal_strength: float = Field(ge=0, le=10)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(max_length=500, default=None)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def validate(self):
        if (self.contact_id[:2] != "AC"):
            raise ValueError(
                "Contact_ID must start with AC (Alien Contact)")
        if (self.contact_type == ContactType.physical
                and not self.is_verified):
            raise ValueError("Physical contact must be verified")
        if (self.contact_type == ContactType.telepathic
                and self.witness_count < 3):
            raise ValueError(
                "Telepathic contact must have at least 3 witnesses")
        if (self.signal_strength > 7.0 and self.message_received is None):
            raise ValueError(
                "Strong signal contact must includes the received message")
        return (self)


def main():
    print("Alien Contact Log Validation")
    print("======================================")
    contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime.now(),
        location="Area 51, Nevada",
        contact_type=ContactType.radio,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli"
    )
    print("Valid contact report:")
    print("ID:", contact.contact_id)
    print("Type:", contact.contact_type.name)
    print("Location:", contact.location)
    print(f"Signal: {contact.signal_strength}/10")
    print("Duration:", contact.duration_minutes, "minutes")
    print("Witnesses:", contact.witness_count)
    print(f"Message: '{contact.message_received}'")
    print("\n======================================")
    print("Expected validation error:")
    try:
        contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type=ContactType.telepathic,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received="Greetings from Zeta Reticuli"
        )
    except ValidationError as e:
        print(e.errors()[0]["msg"])


if (__name__ == "__main__"):
    main()
