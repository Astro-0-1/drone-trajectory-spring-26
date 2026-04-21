import typing as T
import math


from src.data_model import Camera, DatasetSpec, Waypoint
from src.camera_utils import (
    compute_image_footprint_on_surface,
    compute_ground_sampling_distance,
)


def compute_distance_between_images(
    camera: Camera, dataset_spec: DatasetSpec
) -> tuple[float, float]:
    """Compute the distance between images in the horizontal and vertical directions for specified overlap and sidelap.

    Args:
        camera: Camera model used for image capture.
        dataset_spec: user specification for the dataset.

    Returns:
        The horizontal and vertical distance between images (in meters).
    """

    footprint_x, footprint_y = compute_image_footprint_on_surface(camera, dataset_spec.height)
    distance_x = footprint_x * (1 - dataset_spec.overlap)
    distance_y = footprint_y * (1 - dataset_spec.sidelap)

    return distance_x, distance_y


def compute_speed_during_photo_capture(
    camera: Camera, dataset_spec: DatasetSpec, allowed_movement_px: float = 1
) -> float:
    """Compute the speed of drone during an active photo capture to prevent more than 1px of motion blur.

    Args:
        camera: Camera model used for image capture.
        dataset_spec: user specification for the dataset.
        allowed_movement_px: The maximum allowed movement in pixels. Defaults to 1 px.

    Returns:
        The speed at which the drone should move during photo capture.
    """
    gsd = compute_ground_sampling_distance(camera, dataset_spec.height)
    allowed_movement_m = allowed_movement_px * gsd
    speed = allowed_movement_m / (dataset_spec.exposure_time_ms / 1000)
    
    return speed


def generate_photo_plan_on_grid(
    camera: Camera, dataset_spec: DatasetSpec
) -> T.List[Waypoint]:
    """Generate the complete photo plan as a list of waypoints in a lawn-mower pattern.

    Args:
        camera: Camera model used for image capture.
        dataset_spec: user specification for the dataset.

    Returns:
        Scan plan as a list of waypoints.

    """
    distance_x, distance_y = compute_distance_between_images(camera, dataset_spec)
    speed = compute_speed_during_photo_capture(camera, dataset_spec)

    n_x = math.floor(dataset_spec.scan_dimension_x / distance_x) + 1
    n_y = math.floor(dataset_spec.scan_dimension_y / distance_y) + 1

    start_x = (dataset_spec.scan_dimension_x - (n_x - 1) * distance_x) / 2
    start_y = (dataset_spec.scan_dimension_y - (n_y - 1) * distance_y) / 2

    waypoints = []
    for row in range(n_y):
        y = start_y + row * distance_y
        cols = range(n_x) if row % 2 == 0 else range(n_x - 1, -1, -1)
        for col in cols:
            x = start_x + col * distance_x
            waypoints.append(Waypoint(x=x, y=y, z=dataset_spec.height, speed=speed))

    return waypoints


def generate_photo_plan_zigzag(
    camera: Camera, dataset_spec: DatasetSpec
) -> T.List[Waypoint]:
    """Generate the complete photo plan as a list of waypoints in a diagonal zigzag pattern.

    Traverses the grid along anti-diagonals (45° stripes), alternating direction each stripe.

    Args:
        camera: Camera model used for image capture.
        dataset_spec: user specification for the dataset.

    Returns:
        Scan plan as a list of waypoints.
    """
    distance_x, distance_y = compute_distance_between_images(camera, dataset_spec)
    speed = compute_speed_during_photo_capture(camera, dataset_spec)

    n_x = math.floor(dataset_spec.scan_dimension_x / distance_x) + 1
    n_y = math.floor(dataset_spec.scan_dimension_y / distance_y) + 1

    start_x = (dataset_spec.scan_dimension_x - (n_x - 1) * distance_x) / 2
    start_y = (dataset_spec.scan_dimension_y - (n_y - 1) * distance_y) / 2

    waypoints = []

    # Each anti-diagonal has col + row = k
    for k in range(n_x + n_y - 1):
        col_min = max(0, k - (n_y - 1))
        col_max = min(k, n_x - 1)
        cols = range(col_min, col_max + 1)
        if k % 2 == 1:
            cols = reversed(cols)
        for col in cols:
            row = k - col
            x = start_x + col * distance_x
            y = start_y + row * distance_y
            waypoints.append(Waypoint(x=x, y=y, z=dataset_spec.height, speed=speed))

    return waypoints


def generate_photo_plan_spiral(
    camera: Camera, dataset_spec: DatasetSpec
) -> T.List[Waypoint]:
    """Generate the complete photo plan as a list of waypoints in a spiral pattern (outside to inside).

    Args:
        camera: Camera model used for image capture.
        dataset_spec: user specification for the dataset.

    Returns:
        Scan plan as a list of waypoints.
    """
    distance_x, distance_y = compute_distance_between_images(camera, dataset_spec)
    speed = compute_speed_during_photo_capture(camera, dataset_spec)

    n_x = math.floor(dataset_spec.scan_dimension_x / distance_x) + 1
    n_y = math.floor(dataset_spec.scan_dimension_y / distance_y) + 1

    start_x = (dataset_spec.scan_dimension_x - (n_x - 1) * distance_x) / 2
    start_y = (dataset_spec.scan_dimension_y - (n_y - 1) * distance_y) / 2

    # Build full grid of (x, y) positions
    grid = [
        [
            (start_x + col * distance_x, start_y + row * distance_y)
            for col in range(n_x)
        ]
        for row in range(n_y)
    ]

    # Spiral traversal: peel the grid layer by layer from outside to inside
    waypoints = []
    top, bottom, left, right = n_y - 1, 0, 0, n_x - 1

    while top >= bottom and right >= left:
        # Top row: left → right
        for col in range(left, right + 1):
            x, y = grid[top][col]
            waypoints.append(Waypoint(x=x, y=y, z=dataset_spec.height, speed=speed))
        top -= 1

        # Right column: top → bottom
        for row in range(top, bottom - 1, -1):
            x, y = grid[row][right]
            waypoints.append(Waypoint(x=x, y=y, z=dataset_spec.height, speed=speed))
        right -= 1

        # Bottom row: right → left (only if there are still rows left)
        if top >= bottom:
            for col in range(right, left - 1, -1):
                x, y = grid[bottom][col]
                waypoints.append(Waypoint(x=x, y=y, z=dataset_spec.height, speed=speed))
            bottom += 1

        # Left column: bottom → top (only if there are still columns left)
        if right >= left:
            for row in range(bottom, top + 1):
                x, y = grid[row][left]
                waypoints.append(Waypoint(x=x, y=y, z=dataset_spec.height, speed=speed))
            left += 1

    return waypoints
