import time
import numpy as np
from scipy.fft import fft, fftfreq
from sklearn import linear_model


class Device():

    def __init__(self, device, query_delay=0.3):
        self.device = device
        self.query_delay = query_delay

        print(self.identify())

    def identify(self):
        return self.__class__.__name__ + " " + self.device.query("*IDN?")

    def read(self):
        status = -1
        status = self.device.read()
        return status

    def write(self, command):
        data = self.device.write(command)
        return data

    def query(self, command):
        return self.device.query(command)


class Oscilloscope(Device):

    def __init__(self, device):
        super().__init__(device)

    def set_timebase(self, timebase):
        status = self.device.write("TIMebase:SCALe {}".format(timebase))
        return status

    def get_data(self, channel=1):
        self.write("CHAN{}:WAV1:DATA?".format(channel))
        time.sleep(self.query_delay)
        data = self.device.read()
        data = self.postprocess(data)
        return data

    def postprocess(self, data):
        data = data.split(",")
        data = list(map(float, data))
        return data


class Generator(Device):

    def __init__(self, device):
        super().__init__(device)

    def set_signal(self, signal="sin"):
        status = self.device.write("FUNC {}".format(signal))
        return status

    def set_freq(self, freq):
        status = self.device.write(f"FREQ {freq}")
        return status


def to_dB(val):
    return 20 * np.log10(val)


def frequency_sweep(start_freq, end_freq, steps):
    """
    Builds logarithmic generator yielding frequency

    Args:
        start_freq (float): Start frequency
        end_freq (float): End frequency
        steps (int): Steps between start and end frequencies

    Yields:
        float: Actual frequency in the sweep
    """
    sweep = np.logspace(np.log10(start_freq), np.log10(end_freq), steps)
    for freq in sweep:
        yield freq


def calculate_thd(y, base_frequency, sampling_frequency, ret_viz=False):
    """
    Calculate THD of the signal y

    Args:
        y (list[float]): List filled by ampltiude values
        base_frequency (float): Base frequency for thd calculations
        sampling_frequency (float): Sampling frequency of the y data
        ret_viz (bool, optional): Return x, y lists for visualization. Defaults to False.

    Returns:
        float: THD value
    """
    assert len(y) != 0, "Data length cannot be equal to 0"
    assert base_frequency > 0, "Base_frequency should be a positive value"
    assert sampling_frequency > 0, "Sampling frequency should be a postitive value"

    N = len(y)
    T = 1 / sampling_frequency

    yf = fft(y)
    xf = fftfreq(N, T)[:N // 2]
    yfft = 2.0 / N * np.abs(yf[0:N // 2])

    thd = 0.0

    for frequency in np.arange(2 * base_frequency, 5 * base_frequency,
                               base_frequency):
        closest_frequency_index = np.argmin(np.abs(xf - frequency))
        thd += np.power(yfft[closest_frequency_index], 2)

    thd = np.sqrt(thd)

    if ret_viz:
        return thd, xf, yfft

    return thd


def calculate_thd_n(y, base_frequency, sampling_frequency, ret_viz=False):
    """
    Calculate THD+N of the signal y

    Args:
        y (list[float]): List filled by ampltiude values
        base_frequency (float): Base frequency for thd calculations
        sampling_frequency (float): Sampling frequency of the y data
        ret_viz (bool, optional): Return x, y lists for visualization. Defaults to False.

    Returns:
        float: THD+N value
    """
    assert len(y) != 0, "Data length cannot be equal to 0"
    assert base_frequency > 0, "Base_frequency should be a positive value"
    assert sampling_frequency > 0, "Sampling frequency should be a postitive value"

    N = len(y)
    T = 1 / sampling_frequency

    yf = fft(y)
    xf = fftfreq(N, T)[:N // 2]
    yfft = 2.0 / N * np.abs(yf[0:N // 2])

    thd_n = 0.0
    reg = linear_model.Lasso(alpha=0.1).fit(xf.reshape(-1, 1), 1 / yfft)
    noise_level = 3 / reg.intercept_  # 3 - Hacky fix

    for frequency in np.arange(2 * base_frequency, 5 * base_frequency,
                               base_frequency):
        closest_frequency_index = np.argmin(np.abs(xf - frequency))
        thd_n += np.power(yfft[closest_frequency_index], 2)

    thd_n += np.power(noise_level, 2)
    thd_n = np.sqrt(thd_n)

    if ret_viz:
        return thd_n, xf, yfft, noise_level

    return thd_n


def analize(f_start, f_end, steps, generator, oscilloscope):
    for freq in frequency_sweep(f_start, f_end, steps):
        generator.set_freq(freq)
        timebase = 0.5 / freq
        oscilloscope.set_timebase(timebase)
        sampling_frequency = 1000 / (timebase)

        time.sleep(1)
        data = oscilloscope.get_data()
        data2 = oscilloscope.get_data(channel=2)
        thd = calculate_thd(data, freq, sampling_frequency)
        thd_n = calculate_thd_n(data, freq, sampling_frequency)
        amplitude1 = max(data)
        amplitude2 = max(data2)
        yield freq, thd, thd_n, amplitude1, amplitude2
