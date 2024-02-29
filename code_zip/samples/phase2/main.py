from lib.circle import calculate_area, calculate_circumference
from lib.security import check_password

def main():
    if not check_password():
        print("Incorrect password. Exiting.")
        return

    try:
        radius = float(input("Enter the radius of the circle: "))
        area = calculate_area(radius)
        circumference = calculate_circumference(radius)

        print(f"Area of the circle: {area:.2f}")
        print(f"Circumference of the circle: {circumference:.2f}")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
