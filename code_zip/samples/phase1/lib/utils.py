import math

def validate_radius(radius):
    if radius <= 0:
        raise ValueError("Radius must be a positive number")

def get_pi():
    return math.pi
