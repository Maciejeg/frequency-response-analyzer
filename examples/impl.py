import matplotlib.pyplot as plt
import numpy as np
import tqdm
import pyvisa
import time
from utils import Generator, Oscilloscope, to_dB
from utils import frequency_sweep
from utils import calculate_thd, calculate_thd_n

rm = pyvisa.ResourceManager()

generator = Generator(rm.open_resource('GPIB0::4::INSTR'))
oscilloscope = Oscilloscope(
    rm.open_resource('TCPIP0::10.42.14.214::inst0::INSTR'))

f_start = 10
f_end = 100_000
steps = 10
data_points = []
data_points2 = []
thd = []
thd_n = []

for freq in tqdm.tqdm(frequency_sweep(f_start, f_end, steps)):
    generator.set_freq(freq)
    timebase = 0.5 / freq
    oscilloscope.set_timebase(timebase)
    sampling_frequency = 1000 / (timebase)

    time.sleep(1)
    data = oscilloscope.get_data()
    data2 = oscilloscope.get_data(channel=2)
    thd.append(calculate_thd(data, freq, sampling_frequency))
    thd_n.append(calculate_thd_n(data, freq, sampling_frequency))
    data_points.append([freq, max(data)])
    data_points2.append([freq, max(data2)])

data_points = np.array(data_points)
data_points2 = np.array(data_points2)

x = data_points[:, 0]
y = data_points[:, 1]
y = to_dB(y)
thd = to_dB(thd)
thd_n = to_dB(thd_n)

plt.figure(figsize=(20, 10))
plt.subplot(2, 1, 1)
plt.plot(x, y, label='Amplifier')
plt.plot(data_points2[:, 0], data_points2[:, 1], label='generator')
plt.legend()
plt.xscale('log')
plt.ylim([-np.abs(4*max(y)), np.abs(4*max(y))])
plt.xlabel("Frequency [Hz]")
plt.ylabel("Gain [dB]")
plt.title("Frequency response")
plt.grid(True, which="both", ls="-")
plt.subplot(2, 1, 2)
plt.plot(x, thd, label='THD')
plt.xscale('log')
plt.title("THD & THD+N")
plt.plot(x, thd_n, label='THD+N')
plt.grid(True, which="both", ls="-")
plt.legend()
plt.show()
