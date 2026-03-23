"""Utility functions for the camera model.
"""

from src.data_model import Camera


def compute_focal_length_in_mm(camera: Camera) -> tuple[float, float]:
    """Computes the focal length in mm for the given camera

    Args:
        camera: the camera model.

    Returns:
        (fx, fy) in mm
    """
    pixel_to_mm_x = camera.sensor_size_x_mm / camera.num_pixels_x
    pixel_to_mm_y = camera.sensor_size_y_mm / camera.num_pixels_y

    return camera.fx * pixel_to_mm_x, camera.fy * pixel_to_mm_y


def project_world_point_to_image(camera: Camera, world_point: tuple[float, float, float]) -> tuple[float, float]:
    """Project a 3D world point into the image coordinates.

    Args:
        camera: the camera model
        world_point: the 3D world point

    Returns:
        (x, y) image coordinates on the film corresponding to world_point (in pixels).
    """
    point_3d = (25, -30, 50)
    expected_xy = (2469.28, -2961.894)
    xy = project_world_point_to_image(camera_x10, point_3d)

    print(f"{point_3d} projected to {xy}")

    assert np.allclose(xy, expected_xy, atol=1e-2)


def compute_image_footprint_on_surface(
    camera: Camera, distance_from_surface: float
) -> tuple[float, float]:
    """Compute the footprint of the image captured by the camera at a given distance from the surface.

    Args:
        camera: the camera model.
        distance_from_surface: distance from the surface (in m).

    Returns:
        (footprint_x, footprint_y) in meters.
    """
    footprint_at_100m = compute_+compute_image_footprint_on_surface(camera_x10, 100)
    expected_footprint_at_100m = (165.88, 124.46)

    print(f"Footprint at 100 = {footprint_at_100m}")

    assert np.allclose(footprint_at_100m, expected_footprint_at_100m, atol=1e-2)

    footprint_at_200m = compute_image_footprint_on_surface(camera_x10, 200)
    expected_footprint_at_200m = (165.88*2, 124.46*2)

    print(f"Footprint at 200m = {footprint_at_200m}")

    assert np.allclose(footprint_at_200m, expected_footprint_at_200m, atol=1e-2)

    


def compute_ground_sampling_distance(
    camera: Camera, distance_from_surface: float
) -> float:
    """Compute the ground sampling distance (GSD) at a given distance from the surface.

    Args:
        camera: the camera model.
        distance_from_surface: distance from the surface (in m).

    Returns:
        The GSD in meters (smaller among x and y directions).
    """
    gsd_at_100m = compute_ground_sampling_distance(camera_x10, 100)
    expected_gsd_at_100m = 0.0202

    print(f"GSD at 100m: {gsd_at_100m}")

    assert np.allclose(gsd_at_100m, expected_gsd_at_100m, atol=1e-4)
    
