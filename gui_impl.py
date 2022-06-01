import time
import matplotlib.pyplot as plt
import streamlit as st
import math
from test import test_thd
import numpy as np

placeholder = st.empty()
st.sidebar.markdown("## Panel użytkownika")

if st.sidebar.button('Start'):
    st.sidebar.write('Program działa')
else:
    st.sidebar.write('Program nie działa')
_, x, y = test_thd()

min_f = st.sidebar.number_input('Podaj wartość minimalną częstotliwości')
st.sidebar.write('Podana wartość to ', min_f)

max_f = st.sidebar.number_input('Podaj wartość maksymalną częstotliwości')
st.sidebar.write('Podana wartość to ', max_f)

ste1 = st.sidebar.number_input('Podaj liczbę kroków')
st.sidebar.write('Podana wartość to ', ste1)

with placeholder.container():
    st.markdown("## Badanie wzmacniacza")
    fig1, fig2 = st.columns(2)
    y = np.random.random((len(y)))
    with fig1:
        st.markdown("### Wykres 1")
        fig, ax = plt.subplots()
        plt.plot(x, y)
        plt.xlabel("Average Pulse")
        plt.ylabel("Calorie Burnage")
        st.pyplot(fig)

    with fig2:
        st.markdown("### Wykres 2")
        fig, ax = plt.subplots()
        plt.plot(
            x,
            y,
        )
        plt.xlabel("Average Pulse")
        plt.ylabel("Calorie Burnage")
        st.pyplot(fig, )

    fig3, fig4 = st.columns(2)
    with fig3:
        st.markdown("### Wykres 3")
        fig, ax = plt.subplots()
        plt.plot(x, y)
        plt.xlabel("Average Pulse")
        plt.ylabel("Calorie Burnage")
        st.pyplot(fig)

    with fig4:
        st.markdown("### Wykres 4")
        fig, ax = plt.subplots()
        plt.plot(x, y)
        plt.xlabel("Average Pulse")
        plt.ylabel("Calorie Burnage")
        st.pyplot(fig)
    time.sleep(1)
col1, col2 = st.sidebar.columns(2)
col1.metric("THD", "70 °F", "1.2 °F")
col2.metric("THD+N", "9 mph", "-8%")
