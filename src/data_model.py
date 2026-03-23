"""Data models for the camera and user specification."""

class DatasetSpec:

    overlap = 0.7
    sidelap = 0.7
    height = 30.48 # 100 ft
    scan_dimension_x = 150
    scan_dimension_y = 150
    exposure_time_ms = 2 # 1/500 exposure time

    dataset_spec = DatasetSpec(overlap, sidelap, height, scan_dimension_x, scan_dimension_y, exposure_time_ms)

    print(f"Nominal specs: {dataset_spec}")


class Camera:
    """
    Data model for a simple pinhole camera.

    References:
    - https://github.com/colmap/colmap/blob/3f75f71310fdec803ab06be84a16cee5032d8e0d/src/colmap/sensor/models.h#L220
    - https://en.wikipedia.org/wiki/Pinhole_camera_model
    """
    # Define the parameters for Skydio VT300L - Wide camera

    fx = 4938.56 # px
    fy = 4936.49 # px
    sensor_size_x_mm = 13.107 # single pixel size * number of pixels in X dimension
    sensor_size_y_mm = 9.830 # single pixel size * number of pixels in Y dimenison
    num_pixels_x = 8192
    num_pixels_y = 6144

    camera_x10 = Camera(fx, fy, sensor_size_x_mm, sensor_size_y_mm, num_pixels_x, num_pixels_y)

    print(f"X10 camerica model: {camera_x10}")


class Waypoint:
    """
    Waypoints are positions where the drone should fly to and capture a photo.
    """
    pass
