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
import os
import datetime


stop = False

work_dir = "C:\\Users\\awdm\\"

def work(min_f, max_f, steps):
    freqs = []
    thds = []
    thdns = []
    amplitudes1 = []
    amplitudes2 = []
    rm = pyvisa.ResourceManager()

    generator = Generator(rm.open_resource('GPIB0::4::INSTR'))
    oscilloscope = Oscilloscope(
        rm.open_resource('TCPIP0::10.42.14.214::inst0::INSTR'))

    step = 0
    for freq, thd, thd_n, amplitude1, amplitude2 in analize(min_f, max_f, steps, generator, oscilloscope):
        with placeholder.container():
            st.markdown("## Badanie rozpoczęto")
            st.progress(step/steps)
            col3, col4 = st.columns(2)
            col3.metric("THD", "{:.2f}%".format(thd*100))
            col4.metric("THD+N", "{:.2f}%".format(thd_n*100))
        step += 1
        if stop:
            exit()
        freqs.append(freq)
        thds.append(thd)
        thdns.append(thd_n)
        amplitudes1.append(amplitude1)
        amplitudes2.append(amplitude2)

    
    with placeholder.container():
        path = work_dir+str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
        os.mkdir(path)
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
            fig.savefig(path+"\\"+"frequency_response_amplifier.png")
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
            fig.savefig(path+"\\"+"frequency_response_generator.png")
            st.pyplot(fig)
            

        fig3, fig4 = st.columns(2)
        with fig3:
            st.markdown("### THD / THD+N")
            fig, ax = plt.subplots()
            plt.plot(freqs,to_dB([i/steps for i in thds]), label='THD')
            plt.plot(freqs, to_dB([i/steps for i in thdns]), label='THD+N')
            plt.xscale('log')
            plt.ylabel("Gain [dB]")
            plt.title("THD & THD+N")
            plt.grid(True, which="both", ls="-")
            plt.legend()
            fig.savefig(path+"\\"+"THD_THDN.png")
            st.pyplot(fig, )
            
    
        with fig4:
            st.markdown("### Porównanie")
            fig, ax = plt.subplots()
            plt.plot(freqs, to_dB(amplitudes1), label='Amplifier')
            plt.plot(freqs, to_dB(amplitudes2), label='Generator')
            plt.legend()
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("Gain [dB]")
            plt.title("Frequency response")
            plt.grid(True, which="both", ls="-")
            plt.xscale('log')
            fig.savefig(path+"\\"+"amplifier_vs_generator.png")
            st.pyplot(fig)
            

        col1, col2 = st.columns(2)
        col1.metric("THD", "{:.2f}%".format(np.mean(thds)/steps*100))
        col2.metric("THD+N", "{:.2f}%".format(np.mean(thdns)/steps*100))
        st.markdown("#### Zapisano tutaj: [{}]({})".format(path, r"file://"+path.replace("\\","/")))


placeholder = st.empty()
st.sidebar.markdown("## Panel użytkownika")

min_f = st.sidebar.number_input('Podaj wartość minimalną częstotliwości', step=1, min_value=1, max_value=10_000_000, value=10)
st.sidebar.write('Podana wartość to ', min_f)

max_f = st.sidebar.number_input('Podaj wartość maksymalną częstotliwości', step=1, min_value=1, max_value=10_000_000, value=100_000)
st.sidebar.write('Podana wartość to ', max_f)

ste1 = st.sidebar.number_input('Podaj liczbę kroków',step=1, min_value=1, max_value=1000, value=30)
st.sidebar.write('Szacowany czas trwania pomiaru to: {}s.'.format(ste1))


if st.sidebar.button('Start'):
    st.sidebar.write('Program działa')
    placeholder.empty()
    #stop = False
    work(min_f, max_f, int(ste1))

else:
    st.sidebar.write('Program nie działa')
    #stop = True