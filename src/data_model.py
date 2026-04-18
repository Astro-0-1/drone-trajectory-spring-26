"""Data models for the camera and user specification."""

from dataclasses import dataclass

@dataclass
class DatasetSpec:

    overlap: float
    sidelap: float
    height: float
    scan_dimension_x: float
    scan_dimension_y: float
    exposure_time_ms: float

@dataclass
class Camera:
    """
    Data model for a simple pinhole camera.

    References:
    - https://github.com/colmap/colmap/blob/3f75f71310fdec803ab06be84a16cee5032d8e0d/src/colmap/sensor/models.h#L220
    - https://en.wikipedia.org/wiki/Pinhole_camera_model
    """
    # Define the parameters for Skydio VT300L - Wide camera

    fx: float
    fy: float
    sensor_size_x_mm: float
    sensor_size_y_mm: float
    num_pixels_x: int
    num_pixels_y: int


class Waypoint:
    """
    Waypoints are positions where the drone should fly to and capture a photo.
    """
    pass
