from utils import calculate_thd
from scipy.fft import fft, fftfreq
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
    return thd, x, y

if __name__ == "__main__":
    test_thd()
    print("Everything passed")
