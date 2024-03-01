from lib.utils import validate_radius, get_pi

def calculate_area(radius):
    validate_radius(radius)
    return get_pi() * radius**2

def calculate_circumference(radius):
    validate_radius(radius)
    return 2 * get_pi() * radius
