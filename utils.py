import time
import numpy as np


class Device():

    def __init__(self, device, query_delay=0.3):
        self.device = device
        self.query_delay = query_delay

        print(self.identify())

    def identify(self):
        return self.device.query("*IDN?")

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
        status = self.device.write("TIMebase:SCALe ".format(timebase))
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
