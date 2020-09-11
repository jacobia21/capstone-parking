import enum

class CameraStatus(enum.Enum):
    ON = "ON"
    OFF = "OFF"

class SpaceAvailability(enum.Enum):
    AVAILABLE = "Available"
    NOT_AVAILABLE = "Not Available"
    RESERVED = "Reserved"

class LogStatus(enum.Enum):
    OPEN = "OPEN"
    RESOLVED ="RESOLVED"

class LogType(enum.Enum):
    WEBSITE = "WEBSITE"
    DATBASE = "DATABASE"
    HARDWARE = "HARDWARE"

class Groups(enum.Enum):
    REGULAR = "Regular"
    SUPER = "Super"