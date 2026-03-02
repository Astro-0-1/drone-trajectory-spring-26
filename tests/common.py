from src.data_model import Camera

fx = 700
fy = 700
sensor_size_x_mm = 10
sensor_size_y_mm = 10
num_pixels_x = 1000
num_pixels_y = 1000

TEST_CAMERA = Camera(
    fx,
    fy,
    sensor_size_x_mm,
    sensor_size_y_mm,
    num_pixels_x,
    num_pixels_y
)
