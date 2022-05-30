import matplotlib.pyplot as plt
import numpy as np
import tqdm
import pyvisa
import time
from utils import Generator, Oscilloscope, to_dB
from utils import frequency_sweep

rm = pyvisa.ResourceManager()

generator = Generator(rm.open_resource('GPIB0::4::INSTR'))
oscilloscope = Oscilloscope(
    rm.open_resource('TCPIP0::10.42.14.214::inst0::INSTR'))

f_start = 10
f_end = 100_000
steps = 1000
data_points = np.zeros((1, 2))

for freq in tqdm.tqdm(frequency_sweep(f_start, f_end, steps)):
    generator.set_freq(freq)
    oscilloscope.set_timebase(0.2 / freq)
    time.sleep(0.1)
    data = oscilloscope.get_data()
    data_points = np.concatenate((data_points, [[freq, np.max(data)]]))

x = data_points[:, 0]
y = data_points[:, 1]

y = to_dB(y)

plt.figure(figsize=(20, 10))
plt.plot(x, y)
plt.xscale('log')
plt.show()
