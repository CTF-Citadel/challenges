from lib.utils import validate_radius

def calculate_diameter(radius):
    validate_radius(radius)
    return 2 * radius
