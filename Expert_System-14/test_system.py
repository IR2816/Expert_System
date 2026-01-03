import main

def test_cases():
    test_data = [
        (2, 20, "Ringan-Rendah"),
        (2, 80, "Ringan-Tinggi"),
        (6, 20, "Berat-Rendah"),
        (6, 80, "Berat-Tinggi"),
        (0, 0, "Minimum"),
        (10, 100, "Maksimum"),
    ]

    print("Running tests...")
    for berat, kotoran, desc in test_data:
        rpm = main.tsukamoto(berat, kotoran)
        print(f"{desc}: {berat}kg, {kotoran}% -> RPM: {rpm:.2f}")


if __name__ == "__main__":
    test_cases()
