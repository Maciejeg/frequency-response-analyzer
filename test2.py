from utils import analize
import matplotlib.pyplot as plt
import numpy as np
import tqdm
import pyvisa
import time
from utils import Generator, Oscilloscope, to_dB
from utils import frequency_sweep
from utils import calculate_thd, calculate_thd_n
import time
import matplotlib.pyplot as plt
import streamlit as st
import math
from test import test_thd
import numpy as np



stop = False


col1, col2 = st.sidebar.columns(2)
col1.metric("THD", "70 °F", "1.2 °F")
col2.metric("THD+N", "9 mph", "-8%")

def work():
    freqs = []
    thds = []
    thdns = []
    amplitudes1 = []
    amplitudes2 = []
    rm = pyvisa.ResourceManager()

    generator = Generator(rm.open_resource('GPIB0::4::INSTR'))
    oscilloscope = Oscilloscope(
        rm.open_resource('TCPIP0::10.42.14.214::inst0::INSTR'))

    f_start = 10
    f_stop = 100_000
    steps = 100
    for freq, thd, thd_n, amplitude1, amplitude2 in analize(f_start, f_stop, steps, generator, oscilloscope):
        if stop:
            exit()
        freqs.append(freq)
        thds.append(thd)
        thdns.append(thd_n)
        amplitudes1.append(amplitude1)
        amplitudes2.append(amplitude2)

        with placeholder.container():
            st.markdown("## Badanie wzmacniacza")
            fig1, fig2 = st.columns(2)
            with fig1:
                st.markdown("### Chrakterystyka przenoszenia wzmacniacza")
                fig, ax = plt.subplots()
                plt.plot(freqs,  to_dB(amplitudes1))
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("Gain [dB]")
                plt.title("Frequency response")
                plt.xscale('log')
                plt.grid(True, which="both", ls="-")
                st.pyplot(fig)

            with fig2:
                st.markdown("### Chrakterystyka przenoszenia generatora")
                fig, ax = plt.subplots()
                plt.plot(freqs, to_dB(amplitudes2))
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("Gain [dB]")
                plt.title("Frequency response")
                plt.xscale('log')
                plt.grid(True, which="both", ls="-")
                st.pyplot(fig)

            fig3, fig4 = st.columns(2)
            with fig3:
                st.markdown("### THD / THD+N")
                fig, ax = plt.subplots()
                plt.plot(freqs,to_dB(thds), label='THD')
                plt.plot(freqs, to_dB(thdns), label='THD+N')
                plt.xscale('log')
                plt.title("THD & THD+N")
                plt.grid(True, which="both", ls="-")
                plt.legend()
                st.pyplot(fig, )

            with fig4:
                st.markdown("### Wykres 4")
                fig, ax = plt.subplots()
                plt.plot(freqs, to_dB(amplitudes1), label='Amplifier')
                plt.plot(freqs, to_dB(amplitudes2), label='Generator')
                plt.legend()
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("Gain [dB]")
                plt.title("Frequency response")
                plt.xscale('log')
                st.pyplot(fig)

            




placeholder = st.empty()
st.sidebar.markdown("## Panel użytkownika")

if st.sidebar.button('Start'):
    st.sidebar.write('Program działa')
    stop = False
    work()

else:
    st.sidebar.write('Program nie działa')
    stop = True

min_f = st.sidebar.number_input('Podaj wartość minimalną częstotliwości')
st.sidebar.write('Podana wartość to ', min_f)

max_f = st.sidebar.number_input('Podaj wartość maksymalną częstotliwości')
st.sidebar.write('Podana wartość to ', max_f)

ste1 = st.sidebar.number_input('Podaj liczbę kroków')
st.sidebar.write('Podana wartość to ', ste1)











