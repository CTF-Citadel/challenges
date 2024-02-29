from lib.utils import validate_radius, get_pi
from lib.geometry import calculate_diameter

def calculate_area(radius):
    validate_radius(radius)
    return get_pi() * radius**2

def calculate_circumference(radius):
    validate_radius(radius)
    return 2 * get_pi() * radius

def calculate_diameter_and_area(radius):
    diameter = calculate_diameter(radius)
    area = calculate_area(radius)
    return diameter, area
