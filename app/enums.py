import enum

class CameraStatus(enum.Enum):
    ON = "ON"
    OFF = "OFF"

class SpaceAvailability(enum.Enum):
    AVAILABLE = "Available"
    NOT_AVAILABLE = "Not Available"
    RESERVED = "Reserved"