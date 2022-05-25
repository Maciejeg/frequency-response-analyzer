import matplotlib.pyplot as plt
import numpy as np
import tqdm
import pyvisa
import time
from utils import Generator, Oscilloscope, to_dB


rm = pyvisa.ResourceManager()

generator = Generator(rm.open_resource('GPIB0::4::INSTR'))
oscilloscope = Oscilloscope(
    rm.open_resource('TCPIP0::10.42.14.214::inst0::INSTR'))

f_start = 10
f_end = 100_000
freqs = np.logspace(1, 5, 200)
data_points = []

for freq in tqdm.tqdm(freqs):
    generator.set_freq(freq)
    oscilloscope.set_timebase(0.2 / freq)
    time.sleep(1)
    data = oscilloscope.get_data()
    data_points.append((freq, max(data)))

x = np.array([p[0] for p in data_points])
y = np.array([p[1] for p in data_points])

y = to_dB(y)

plt.figure(figsize=(20, 10))
plt.plot(x, y)
plt.xscale('log')
plt.show()
