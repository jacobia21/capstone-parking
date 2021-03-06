from app.enums import CameraStatus, SpaceAvailability, LogStatus, LogType, Groups


def test_camera_status():
    assert CameraStatus.ON.value == "ON"
    assert CameraStatus.OFF.value == "OFF"


def test_space_availability():
    assert SpaceAvailability.AVAILABLE.value == "AVAILABLE"
    assert SpaceAvailability.NOT_AVAILABLE.value == "NOT_AVAILABLE"
    assert SpaceAvailability.RESERVED.value == "RESERVED"


def test_log_status():
    assert LogStatus.OPEN.value == "OPEN"
    assert LogStatus.RESOLVED.value == "RESOLVED"


def test_log_type():
    assert LogType.HARDWARE.value == "HARDWARE"
    assert LogType.DATABASE.value == "DATABASE"
    assert LogType.WEBSITE.value == "WEBSITE"


def test_groups():
    assert Groups.SUPER.value == "Super"
    assert Groups.REGULAR.value == "Regular"
