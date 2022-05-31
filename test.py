from utils import calculate_thd, calculate_thd_n, to_dB
import numpy as np


def test_thd():
    f = 73.12
    fs = 20 * f
    N = 6000
    T = 1.0 / (fs)
    t = np.linspace(0, N * T, N, endpoint=False)
    y = 0

    for i in range(1, 10):
        y += 1 / i**4 * np.sin(t * 2 * np.pi * f * i)

    thd, x, y = calculate_thd(y, f, fs, ret_viz=True)
    assert thd == 0.06385402301549004, "THD calculation failed"
    assert (y >= 0).all(), "Negative FFT value"


def test_thd_n():
    f = 73.12
    fs = 20 * f
    N = 6000
    T = 1.0 / (fs)
    t = np.linspace(0, N * T, N, endpoint=False)
    y = 0

    for i in range(1, 10):
        y += 1 / i**4 * np.sin(t * 2 * np.pi * f * i)

    rng = np.random.default_rng(0)
    noise_level = 0
    noise = 10**(noise_level / 20) * rng.random(6000)
    y += noise

    thd = calculate_thd(y, f, fs)
    thd_n, x, y, n = calculate_thd_n(y, f, fs, True)
    assert thd == 0.06168333361611456, "THD calculation failed"
    assert thd_n == 0.06292998187759988, "THD calculation failed"
    assert (y >= 0).all(), "Negative FFT value"
    assert thd_n >= thd, "THD+N must be bigger or equal to THD"


if __name__ == "__main__":
    test_thd()
    test_thd_n()
    print("Everything passed")
