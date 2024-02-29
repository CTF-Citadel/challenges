from lib.circle import calculate_area as circle_area, calculate_circumference, calculate_diameter_and_area
from lib.shapes import calculate_square_area, calculate_square_perimeter
from lib.security import check_password

def main():
    try:
        if not check_password():
            print("Incorrect password. Exiting.")
            return

        print("Select a shape:")
        print("1. Circle")
        print("2. Square")

        choice = input("Enter your choice (1 or 2): ")

        if choice == "1":
            radius = float(input("Enter the radius of the circle: "))

            if 0 < radius <= 1000:  # Example: Valid range 0 < radius <= 1000
                area = circle_area(radius)
                circumference = calculate_circumference(radius)
                diameter, _ = calculate_diameter_and_area(radius)

                print(f"Area of the circle: {area:.2f}")
                print(f"Circumference of the circle: {circumference:.2f}")
                print(f"Diameter of the circle: {diameter:.2f}")
            else:
                print("Error: Radius must be within the range (0, 1000].")

        elif choice == "2":
            side_length = float(input("Enter the side length of the square: "))
            area = calculate_square_area(side_length)
            perimeter = calculate_square_perimeter(side_length)

            print(f"Area of the square: {area:.2f}")
            print(f"Perimeter of the square: {perimeter:.2f}")

        else:
            print("Invalid choice. Please enter either 1 or 2.")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
