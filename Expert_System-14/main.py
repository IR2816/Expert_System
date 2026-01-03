# Sistem Pakar Mesin Cuci - Metode Tsukamoto
# Author: IR2816 (disesuaikan dari Task 2)

import sys
import argparse
from typing import Tuple

# --- Membership Function ---
def mf_ringan(x):
    """Fungsi keanggotaan untuk berat cucian RINGAN"""
    if x <= 0:
        return 1.0
    elif 0 < x < 4:
        return (4 - x) / 4
    else:
        return 0.0

def mf_berat(x):
    """Fungsi keanggotaan untuk berat cucian BERAT"""
    if x <= 3:
        return 0.0
    elif 3 < x < 10:
        return (x - 3) / 7
    else:
        return 1.0

def mf_rendah(x):
    """Fungsi keanggotaan untuk tingkat kekotoran RENDAH"""
    if x <= 0:
        return 1.0
    elif 0 < x < 50:
        return (50 - x) / 50
    else:
        return 0.0

def mf_tinggi(x):
    """Fungsi keanggotaan untuk tingkat kekotoran TINGGI"""
    if x <= 30:
        return 0.0
    elif 30 < x < 100:
        return (x - 30) / 70
    else:
        return 1.0

# --- Output RPM (monoton sesuai Tsukamoto) ---
def rpm_lambat(alpha):
    """RPM menurun dari 1000 ke 500 (semakin lambat)"""
    return 1000 - alpha * (1000 - 500)

def rpm_cepat(alpha):
    """RPM meningkat dari 500 ke 1200 (semakin cepat)"""
    return 500 + alpha * (1200 - 500)

# --- Metode Tsukamoto ---
def tsukamoto(berat, kotoran, debug=False):
    """Menghitung RPM menggunakan metode Tsukamoto"""
    
    # Hitung membership input
    ringan_val = mf_ringan(berat)
    berat_val = mf_berat(berat)
    rendah_val = mf_rendah(kotoran)
    tinggi_val = mf_tinggi(kotoran)
    
    if debug:
        print("\n=== DEBUG INFO ===")
        print(f"Berat cucian: {berat} kg")
        print(f"  - μ_ringan: {ringan_val:.3f}")
        print(f"  - μ_berat: {berat_val:.3f}")
        print(f"Tingkat kekotoran: {kotoran}%")
        print(f"  - μ_rendah: {rendah_val:.3f}")
        print(f"  - μ_tinggi: {tinggi_val:.3f}")
        print("\n=== RULE EVALUATION ===")

    # Rule base
    rules = []
    
    # R1: Berat Ringan AND Kotoran Rendah -> RPM Lambat
    alpha1 = min(ringan_val, rendah_val)
    z1 = rpm_lambat(alpha1)
    rules.append((alpha1, z1))
    if debug:
        print(f"R1: min({ringan_val:.3f}, {rendah_val:.3f}) = {alpha1:.3f}, z = {z1:.2f} RPM")

    # R2: Berat Ringan AND Kotoran Tinggi -> RPM Cepat
    alpha2 = min(ringan_val, tinggi_val)
    z2 = rpm_cepat(alpha2)
    rules.append((alpha2, z2))
    if debug:
        print(f"R2: min({ringan_val:.3f}, {tinggi_val:.3f}) = {alpha2:.3f}, z = {z2:.2f} RPM")

    # R3: Berat Berat AND Kotoran Rendah -> RPM Cepat
    alpha3 = min(berat_val, rendah_val)
    z3 = rpm_cepat(alpha3)
    rules.append((alpha3, z3))
    if debug:
        print(f"R3: min({berat_val:.3f}, {rendah_val:.3f}) = {alpha3:.3f}, z = {z3:.2f} RPM")

    # R4: Berat Berat AND Kotoran Tinggi -> RPM Cepat
    alpha4 = min(berat_val, tinggi_val)
    z4 = rpm_cepat(alpha4)
    rules.append((alpha4, z4))
    if debug:
        print(f"R4: min({berat_val:.3f}, {tinggi_val:.3f}) = {alpha4:.3f}, z = {z4:.2f} RPM")

    # Defuzzifikasi Tsukamoto
    numerator = sum([a * z for a, z in rules])
    denominator = sum([a for a, _ in rules])
    
    if debug:
        print(f"\n=== DEFUZZIFICATION ===")
        print(f"Numerator (Σα*z): {numerator:.3f}")
        print(f"Denominator (Σα): {denominator:.3f}")
    
    if denominator != 0:
        result = numerator / denominator
    else:
        result = 0.0
        if debug:
            print("Peringatan: Denominator = 0, hasil diatur ke 0")
    
    return result

# --- Fungsi untuk contoh/test tanpa input manual ---
def run_examples() -> None:
    """Menjalankan beberapa contoh untuk testing"""
    examples = [
        (2.0, 20.0),   # Ringan, Rendah
        (2.0, 70.0),   # Ringan, Tinggi
        (6.0, 20.0),   # Berat, Rendah
        (6.0, 70.0),   # Berat, Tinggi
        (0.0, 0.0),    # Batas minimum
        (10.0, 100.0), # Batas maksimum
    ]
    
    print("\n=== CONTOH TEST (tanpa input) ===")
    for berat, kotoran in examples:
        rpm = tsukamoto(berat, kotoran, debug=False)
        print(f"Berat: {berat:4.1f} kg, Kotoran: {kotoran:5.1f}% → RPM: {rpm:7.2f}")

def validate_bounds(berat: float, kotoran: float) -> Tuple[float, float]:
    """Ensure berat and kotoran are within expected ranges.

    Clips to valid ranges and returns the (possibly adjusted) values.
    """
    if berat < 0:
        raise ValueError("Berat tidak boleh negatif")
    if kotoran < 0:
        raise ValueError("Tingkat kekotoran tidak boleh negatif")

    # Clip to upper bounds
    if berat > 10:
        berat = 10.0
    if kotoran > 100:
        kotoran = 100.0
    return berat, kotoran


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Sistem Pakar Mesin Cuci - Metode Tsukamoto")
    parser.add_argument("--debug", action="store_true", help="Aktifkan mode debug")
    parser.add_argument("--examples", action="store_true", help="Jalankan contoh/test tanpa interaksi")
    parser.add_argument("--berat", type=float, help="Berat cucian (kg) 0-10")
    parser.add_argument("--kotoran", type=float, help="Tingkat kekotoran (%%) 0-100")

    args = parser.parse_args(argv)

    print("=" * 50)
    print("SISTEM PAKAR MESIN CUCI - METODE TSUKAMOTO")
    print("=" * 50)

    if args.examples:
        run_examples()
        print("\n" + "=" * 50)
        print("Program selesai.")
        return

    if args.berat is not None and args.kotoran is not None:
        try:
            berat_val, kotoran_val = validate_bounds(args.berat, args.kotoran)
        except ValueError as exc:
            print(f"ERROR: {exc}")
            sys.exit(1)

        hasil_rpm = tsukamoto(berat_val, kotoran_val, debug=args.debug)
        print("\n" + "=" * 50)
        print("HASIL PERHITUNGAN")
        print("=" * 50)
        print(f"Berat cucian     : {berat_val:.2f} kg")
        print(f"Tingkat kekotoran: {kotoran_val:.2f}%")
        print(f"RPM mesin cuci   : {hasil_rpm:.2f}")

        print("\n" + "=" * 50)
        print("Program selesai.")
        return

    # Fallback ke mode interaktif bila tidak ada argumen non-interaktif
    try:
        debug_mode = input("Aktifkan mode debug? (y/n): ").strip().lower() == 'y'
        print("\nPilihan:")
        print("1. Input manual")
        print("2. Lihat contoh/test")
        pilihan = input("Pilih (1/2): ").strip()

        if pilihan == "2":
            run_examples()
        else:
            print("\n" + "-" * 30)
            berat_input = float(input("Masukkan berat cucian (kg) [0-10]: "))
            kotoran_input = float(input("Masukkan tingkat kekotoran (%) [0-100]: "))
            berat_input, kotoran_input = validate_bounds(berat_input, kotoran_input)
            hasil_rpm = tsukamoto(berat_input, kotoran_input, debug=debug_mode)

            print("\n" + "=" * 50)
            print("HASIL PERHITUNGAN")
            print("=" * 50)
            print(f"Berat cucian     : {berat_input:.2f} kg")
            print(f"Tingkat kekotoran: {kotoran_input:.2f}%")
            print(f"RPM mesin cuci   : {hasil_rpm:.2f}")

    except ValueError:
        print("\nERROR: Input harus berupa angka atau berada dalam rentang yang benar!")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh user.")
        sys.exit(0)


if __name__ == "__main__":
    main()