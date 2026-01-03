from main import tsukamoto


def test_example_ringan_rendah():
    # (2.0, 20.0) expected 750 based on membership calculations
    rpm = tsukamoto(2.0, 20.0)
    assert abs(rpm - 750.0) < 1e-6


def test_example_berat_tinggi():
    # (6.0, 70.0) expected ~800 based on membership calculations
    rpm = tsukamoto(6.0, 70.0)
    assert abs(rpm - 800.0) < 1e-6
