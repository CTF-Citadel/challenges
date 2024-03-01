from lib.circle import calculate_area, calculate_circumference, calculate_diameter_and_area
from lib.security import check_password

def main():
    try:
        if not check_password():
            print("Incorrect password. Exiting.")
            return

        radius = float(input("Enter the radius of the circle: "))

        if 0 < radius <= 1000:
            area = calculate_area(radius)
            circumference = calculate_circumference(radius)
            diameter, _ = calculate_diameter_and_area(radius)

            print(f"Area of the circle: {area:.2f}")
            print(f"Circumference of the circle: {circumference:.2f}")
            print(f"Diameter of the circle: {diameter:.2f}")
        else:
            print("Error: Radius must be within the range (0, 1000].")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
