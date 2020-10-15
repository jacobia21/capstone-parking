""" This module defines the enum types used within the app module """
import enum


class CameraStatus(enum.Enum):
    """Defines all possible options for a camera's status."""

    ON = "ON"
    OFF = "OFF"


class SpaceAvailability(enum.Enum):
    """Defines all possible options for a space's availability."""

    AVAILABLE = "Available"
    NOT_AVAILABLE = "Not Available"
    RESERVED = "Reserved"


class LogStatus(enum.Enum):
    """Defines all possible options for an error log's status."""

    OPEN = "OPEN"
    RESOLVED = "RESOLVED"


class LogType(enum.Enum):
    """Defines all possible options for an error log's type."""

    WEBSITE = "WEBSITE"
    DATABASE = "DATABASE"
    HARDWARE = "HARDWARE"


class Groups(enum.Enum):
    """Defines all possible options for an administrator's group or type."""

    REGULAR = "Regular"
    SUPER = "Super"
